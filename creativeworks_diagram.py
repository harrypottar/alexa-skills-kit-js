from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.compute import Deployment
from diagrams.onprem.database import MariaDB, MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.monitoring import Grafana
from diagrams.elastic.elasticsearch import Elasticsearch, Kibana
from diagrams.saas.identity import Auth0
from diagrams.programming.framework import GraphQL, React
from diagrams.onprem.client import Users
from diagrams.aws.storage import S3

# Configure diagram attributes for executive presentation
graph_attr = {
    "fontsize": "18",
    "bgcolor": "white",
    "pad": "0.8",
    "splines": "ortho",
}

cluster_attr = {
    "fontsize": "15",
}

with Diagram(
    "Creativeworks Architecture",
    show=False,
    direction="TB",
    graph_attr=graph_attr,
    outformat="png",
    filename="creativeworks_architecture"
):

    # External Users
    with Cluster("External Clients", graph_attr={"bgcolor": "#E3F2FD"}):
        partners = Users("Integration & Partners")
        web_ui = React("Web UI")

    # External Authentication
    with Cluster("External Auth", graph_attr={"bgcolor": "#FFF3E0"}):
        oauth = Auth0("OAuth2.0")
        saml = Auth0("SAML")
        okta = Auth0("Okta")

    # Kubernetes Cluster
    with Cluster("Kubernetes Cluster", graph_attr={"bgcolor": "#E8F5E9"}):

        # API Gateway Layer
        with Cluster("Gateway Layer", graph_attr={"bgcolor": "#C8E6C9"}):
            graphql_gateway = GraphQL("GraphQL Gateway\n(Entry Point)")
            auth_service = Deployment("Auth Service\n(User Mgmt)")

        # Web Frontend
        web_service = Deployment("Web Service\n(UI Backend)")

        # Orchestration
        with Cluster("Orchestration", graph_attr={"bgcolor": "#FFF9C4"}):
            conductor = Deployment("Conductor\n(Workflow Engine)")
            rabbitmq = RabbitMQ("RabbitMQ\n(Message Queue)")

        # Business Services
        with Cluster("Business Services", graph_attr={"bgcolor": "#BBDEFB"}):
            notification = Deployment("Notification\n(Email)")
            payment = Deployment("Payment\n(Processing)")
            delivery = Deployment("Delivery\n(Downloads)")

        # Media Processing Services
        with Cluster("Media Processing", graph_attr={"bgcolor": "#D1C4E9"}):
            imagemagick = Deployment("ImageMagick\n(Thumbnails)")
            ffmpeg = Deployment("FFMpeg\n(Video)")
            exiftool = Deployment("ExifTool\n(Metadata)")
            renditions = Deployment("Renditions\n(Variants)")

        # Document Processing Services
        with Cluster("Document Processing", graph_attr={"bgcolor": "#B2DFDB"}):
            openoffice = Deployment("OpenOffice\n(Docs)")
            pdf_service = Deployment("PDF Service\n(PDF/Text)")

        # Storage Services
        with Cluster("Storage Services", graph_attr={"bgcolor": "#FFCCBC"}):
            filesystem = Deployment("File System\n(Storage Mgmt)")
            mongodb_service = Deployment("MongoDB Service\n(Asset CRUD)")

    # Infrastructure Services
    with Cluster("Infrastructure Services", graph_attr={"bgcolor": "#FFE0B2"}):
        with Cluster("Identity", graph_attr={"bgcolor": "#FFCCBC"}):
            keycloak = Auth0("KeyCloak\n(SSO)")

        with Cluster("Data Storage", graph_attr={"bgcolor": "#F0F4C3"}):
            mysql = MariaDB("MySQL/MariaDB\n(Relational)")
            mongodb = MongoDB("MongoDB\n(Documents)")
            redis = Redis("Redis\n(Cache)")

        with Cluster("Logging & Monitoring", graph_attr={"bgcolor": "#E1BEE7"}):
            elastic = Elasticsearch("ElasticSearch\n(Logs)")
            kibana = Kibana("Kibana\n(Analytics)")

    # External Storage Backends
    with Cluster("External Storage", graph_attr={"bgcolor": "#FFF3E0"}):
        s3 = S3("AWS S3\n(Object Storage)")
        egnyte = Custom("Egnyte\n(Cloud Sharing)", "./logos/egnyte.png")
        lucidlink = Custom("LucidLink\n(Cloud FS)", "./logos/lucidlink.png")

    # ==========================================
    # CONNECTIONS
    # ==========================================

    # External Clients to Gateway
    partners >> Edge(color="#1976D2", style="bold", label="API") >> graphql_gateway
    web_ui >> Edge(color="#1976D2", style="bold", label="BFF") >> web_service

    # External Auth to KeyCloak
    oauth >> Edge(color="#FF6F00", style="bold", label="auth") >> keycloak
    saml >> Edge(color="#FF6F00", style="bold", label="auth") >> keycloak
    okta >> Edge(color="#FF6F00", style="bold", label="auth") >> keycloak

    # Gateway to Auth (Direct - Synchronous)
    graphql_gateway >> Edge(color="#2E7D32", style="bold", label="auth") >> auth_service

    # Gateway to MongoDB Service (Direct - Synchronous CRUD)
    graphql_gateway >> Edge(color="#2E7D32", style="bold", label="CRUD") >> mongodb_service

    # Web Service calls Gateway on behalf of Web UI
    web_service >> Edge(color="#2E7D32", style="bold", label="API calls") >> graphql_gateway

    # Auth Service to KeyCloak
    auth_service >> Edge(color="#F57C00", style="dashed", label="SSO") >> keycloak

    # Auth Service sends notifications via RabbitMQ
    auth_service >> Edge(color="#7B1FA2", label="notices") >> rabbitmq

    # Gateway to Conductor/RabbitMQ (Async Entry)
    graphql_gateway >> Edge(color="#F57C00", style="bold", label="requests") >> conductor
    conductor >> Edge(color="#D32F2F", style="bold", label="orchestrate") >> rabbitmq

    # RabbitMQ to Business Services
    rabbitmq >> Edge(color="#7B1FA2", label="queue") >> notification
    rabbitmq >> Edge(color="#7B1FA2", label="queue") >> payment
    rabbitmq >> Edge(color="#7B1FA2", label="queue") >> delivery

    # RabbitMQ to Media Processing
    rabbitmq >> Edge(color="#512DA8", label="queue") >> imagemagick
    rabbitmq >> Edge(color="#512DA8", label="queue") >> ffmpeg
    rabbitmq >> Edge(color="#512DA8", label="queue") >> exiftool
    rabbitmq >> Edge(color="#512DA8", label="queue") >> renditions

    # RabbitMQ to Document Processing
    rabbitmq >> Edge(color="#0097A7", label="queue") >> openoffice
    rabbitmq >> Edge(color="#0097A7", label="queue") >> pdf_service

    # RabbitMQ to Storage Services
    rabbitmq >> Edge(color="#E65100", label="queue") >> filesystem

    # File System to External Storage
    filesystem >> Edge(color="#F57F17", style="bold", label="mount") >> s3
    filesystem >> Edge(color="#F57F17", style="bold", label="mount") >> egnyte
    filesystem >> Edge(color="#F57F17", style="bold", label="mount") >> lucidlink

    # Services to Databases
    auth_service >> Edge(color="#6D4C41", style="dotted") >> mysql
    delivery >> Edge(color="#6D4C41", style="dotted") >> mysql
    payment >> Edge(color="#6D4C41", style="dotted") >> mysql

    # Services to MongoDB
    mongodb_service >> Edge(color="#455A64", style="bold", label="CRUD") >> mongodb
    renditions >> Edge(color="#455A64", style="dotted") >> mongodb
    delivery >> Edge(color="#455A64", style="dotted") >> mongodb

    # Services to Redis (Cache)
    auth_service >> Edge(color="#C62828", style="dotted", label="cache") >> redis
    delivery >> Edge(color="#C62828", style="dotted", label="cache") >> redis

    # KeyCloak uses MySQL as backend
    keycloak >> Edge(color="#6D4C41", style="dotted", label="backend") >> mysql

    # Logging
    conductor >> Edge(color="#9E9E9E", style="dotted") >> elastic
    elastic >> Edge(color="#9E9E9E") >> kibana

print("✓ Creativeworks Architecture Diagram generated: creativeworks_architecture.png")
print("  - File System Service with S3, Egnyte, and LucidLink storage backends")
print("  - Using official Egnyte and LucidLink company logos")
print("  - Updated: Web UI → Web Service (BFF pattern)")
print("  - Updated: Users renamed to Integration & Partners")
print("  - Added: External Auth block (OAuth2.0, SAML, Okta → KeyCloak)")
print("  - Added: MongoDB Service for asset CRUD (GraphQL → MongoDB Service → MongoDB)")
