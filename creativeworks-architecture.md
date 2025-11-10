# Creativeworks Architecture

## Application Overview
**Name:** Creativeworks
**Platform:** Kubernetes Microservices
**Architecture Pattern:** Event-driven with GraphQL Gateway

---

## External Access Layer

### API Gateway
- **GraphQL Gateway** - Single entry point for all external API calls
- All external API requests (from Integration & Partners) go through the GraphQL Gateway
- Gateway communicates directly with Auth-Service (synchronous)

### Web UI Access
- **Web UI** - Browser-based user interface
- Connects to Web Service (UI Backend), NOT directly to GraphQL Gateway
- Web Service acts as Backend-for-Frontend (BFF) pattern

### External Authentication
- **OAuth2.0** - Industry standard for authorization
- **SAML** - Enterprise SSO authentication
- **Okta** - Identity and access management platform
- All external auth providers integrate directly with KeyCloak

---

## Microservices

### Core Services

1. **GraphQL-Service**
   - Gateway service
   - Routes external requests
   - Direct connection to Auth-Service

2. **Auth-Service**
   - Authentication and user management
   - Direct connection from GraphQL Gateway (synchronous)
   - Integrates with KeyCloak for SSO and identity management
   - Sends notification messages via RabbitMQ

3. **Conductor Orchestration Service**
   - Processes application flow
   - Orchestrates between RabbitMQ and microservices
   - Central workflow coordinator

### Business Logic Services

4. **Notification-Service**
   - Email notifications
   - Connects via RabbitMQ

5. **Payment Service**
   - Payment processing
   - Connects via RabbitMQ

6. **Delivery Service**
   - File downloading
   - Image conversions
   - Connects via RabbitMQ

### Media Processing Services

7. **ImageMagick Service**
   - Thumbnail generation
   - Watermarking
   - Connects via RabbitMQ

8. **FFMPeg Service**
   - Video preview generation
   - Video processing
   - Connects via RabbitMQ

9. **ExifTool Service**
   - Read metadata from media files
   - Write metadata to media files
   - Connects via RabbitMQ

10. **Renditions Engine**
    - Creates variants of assets
    - Connects via RabbitMQ

### Document Processing Services

11. **OpenOffice Service**
    - Office document processing
    - Text extraction from office documents
    - Connects via RabbitMQ

12. **PDF Service**
    - PDF processing
    - Text extraction from PDFs
    - Connects via RabbitMQ

### Storage Services

13. **File System Service**
    - Unified file storage interface
    - Mounts and manages multiple storage backends:
      - **S3** - AWS S3 object storage
      - **Egnyte** - Cloud file sharing and collaboration
      - **LucidLink** - Cloud-native file system
    - Provides file operations (read, write, delete, move)
    - Handles file synchronization across storage backends
    - Connects via RabbitMQ

### Frontend Services

14. **Web Microservice**
    - Supports web UI (backend for frontend)
    - Makes API calls to GraphQL Gateway on behalf of Web UI
    - Serves as intermediary between browser and API

---

## Infrastructure Services (Run alongside microservices)

### Identity & Access
- **KeyCloak** - Identity and access management, SSO
  - Uses MySQL as backend database

### Databases
- **MySQL** - Relational database (primary data store, KeyCloak backend)
- **MongoDB** - Document database (flexible schema storage)
- **Redis** - In-memory cache and session store

### Messaging & Events
- **RabbitMQ** - Message queue for async communication between services

### Observability
- **ElasticSearch** - Log aggregation and search
- **Kibana** - Log visualization and analytics dashboard

---

## Communication Patterns

### Synchronous Communication
- **Integration & Partners → GraphQL Gateway → Auth-Service** (direct HTTP/GraphQL)
- **Web UI → Web Service → GraphQL Gateway** (BFF pattern - Web Service makes API calls on behalf of Web UI)
- **External Auth (OAuth2.0/SAML/Okta) → KeyCloak** (direct authentication)

### Asynchronous Communication (via RabbitMQ)
- **Auth-Service → RabbitMQ** (sends notification messages)
- **All other services** communicate through RabbitMQ queues
- **Conductor Service** orchestrates workflow between RabbitMQ and microservices
- Event-driven architecture for decoupling

---

## Architecture Flow

```
Integration & Partners → GraphQL Gateway → Auth-Service
                              ↓
                         Conductor ←→ RabbitMQ
                              ↓
                    [All microservices consume from queues]

Web UI → Web Service → GraphQL Gateway → Auth-Service

External Auth (OAuth2.0, SAML, Okta) → KeyCloak → Auth-Service
```

---

## Data Storage Strategy

- **MySQL**: Structured relational data (users, transactions, etc.)
- **MongoDB**: Flexible document storage (metadata, assets info, etc.)
- **Redis**: Caching, sessions, temporary data
- **File System Service**: Media assets and files stored across multiple backends
  - **S3**: Primary object storage for media assets
  - **Egnyte**: Collaborative file sharing and team storage
  - **LucidLink**: Cloud-native file system for high-performance access

---

## Questions / TBD

- [x] How does Web Microservice communicate with backend? **ANSWERED: Via GraphQL Gateway**
- [x] Authentication flow: Does KeyCloak integrate with Auth-Service? **ANSWERED: Yes, Auth-Service uses KeyCloak for SSO**
- [x] What database does KeyCloak use? **ANSWERED: MySQL**
- [x] File storage: Where are media assets stored? **ANSWERED: File System Service manages S3, Egnyte, and LucidLink**
- [ ] Scale requirements: Expected load, number of users?
- [ ] Deployment strategy: Rolling updates, blue-green, canary?
- [ ] Monitoring: Prometheus/Grafana in addition to ELK stack?
- [ ] Security: Service mesh (Istio/Linkerd)? mTLS between services?
- [ ] Cloud provider: AWS, Azure, GCP, on-premise?

---

## Next Steps

1. Create executive-level architecture diagram
2. Define RabbitMQ queue topology and exchange patterns
3. Define data models for MySQL and MongoDB
4. Design API contracts (GraphQL schema)
5. Security and authentication flow diagrams

---

**Last Updated:** 2025-11-10
**Version:** 0.4 - Updated External Clients flow (Web UI → Web Service), renamed to Integration & Partners, added External Auth block (OAuth2.0, SAML, Okta → KeyCloak)
