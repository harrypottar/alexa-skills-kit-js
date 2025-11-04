from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.compute import Deployment, Pod, StatefulSet
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.onprem.database import PostgreSQL, MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.programming.framework import React
from diagrams.saas.identity import Auth0
from diagrams.generic.device import Mobile
from diagrams.onprem.network import Nginx

# Configure diagram attributes for better presentation
graph_attr = {
    "fontsize": "16",
    "bgcolor": "white",
    "pad": "0.5",
}

cluster_attr = {
    "fontsize": "14",
}

with Diagram(
    "Kubernetes Microservices Architecture",
    show=False,
    direction="TB",
    graph_attr=graph_attr,
    outformat="png",
    filename="k8s_architecture"
):

    # External Users Layer
    with Cluster("External Access", graph_attr={"bgcolor": "#E3F2FD"}):
        web_users = React("Web Application")
        mobile_users = Mobile("Mobile Apps")

    # Edge Layer
    with Cluster("Edge Layer", graph_attr={"bgcolor": "#FFF3E0"}):
        loadbalancer = Nginx("Load Balancer")
        cdn = Service("CDN")

    # Kubernetes Cluster
    with Cluster("Kubernetes Cluster", graph_attr={"bgcolor": "#E8F5E9"}):

        # Ingress
        ingress = Ingress("API Gateway\nIngress Controller")

        # Microservices Layer
        with Cluster("Application Services", graph_attr={"bgcolor": "#C8E6C9"}):
            auth_service = Deployment("Authentication\nService")
            user_service = Deployment("User Management\nService")
            business_service = Deployment("Business Logic\nService")
            analytics_service = Deployment("Analytics\nService")
            notification_service = Deployment("Notification\nService")

        # Data Layer
        with Cluster("Data Layer", graph_attr={"bgcolor": "#FFECB3"}):
            postgres = PostgreSQL("PostgreSQL\n(Primary DB)")
            mongo = MongoDB("MongoDB\n(Documents)")
            redis = Redis("Redis\n(Cache)")
            kafka = Kafka("Kafka\n(Event Streaming)")

        # Observability
        with Cluster("Observability", graph_attr={"bgcolor": "#F3E5F5"}):
            prometheus = Prometheus("Prometheus")
            grafana = Grafana("Grafana\nDashboards")

    # External Services
    with Cluster("External Services", graph_attr={"bgcolor": "#FCE4EC"}):
        auth_provider = Auth0("Auth Provider\n(SSO/OAuth)")
        third_party = Service("3rd Party APIs")
        legacy = Service("Legacy Systems")

    # Define connections - External to Edge
    web_users >> Edge(color="blue", style="bold") >> loadbalancer
    mobile_users >> Edge(color="blue", style="bold") >> loadbalancer

    # Edge to Kubernetes
    loadbalancer >> Edge(color="darkgreen") >> ingress

    # Ingress to Services
    ingress >> Edge(color="darkgreen") >> auth_service
    ingress >> Edge(color="darkgreen") >> user_service
    ingress >> Edge(color="darkgreen") >> business_service
    ingress >> Edge(color="darkgreen") >> analytics_service

    # Auth flow
    auth_service >> Edge(color="orange", style="dashed", label="OAuth") >> auth_provider

    # Services to Data Layer
    user_service >> Edge(color="purple") >> postgres
    business_service >> Edge(color="purple") >> postgres
    business_service >> Edge(color="purple") >> mongo

    # Caching
    user_service >> Edge(color="red", style="dotted", label="cache") >> redis
    business_service >> Edge(color="red", style="dotted", label="cache") >> redis

    # Event streaming
    business_service >> Edge(color="brown", label="events") >> kafka
    notification_service >> Edge(color="brown", label="consume") >> kafka
    analytics_service >> Edge(color="brown", label="consume") >> kafka

    # External integrations
    business_service >> Edge(color="gray", style="dashed") >> third_party
    business_service >> Edge(color="gray", style="dashed") >> legacy

    # Monitoring
    prometheus >> Edge(color="purple", style="dotted") >> grafana
    business_service >> Edge(color="lightgray", style="dotted", label="metrics") >> prometheus

print("✓ Diagram generated: k8s_architecture.png")
