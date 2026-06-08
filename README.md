ShopEasy Inventory Service: Continuous Integration & Continuous Deployment (CI/CD) Pipeline
A production-ready, automated DevOps pipeline implementing a secure, multi-instance cloud deployment for the ShopEasy Inventory microservice backend. This project showcases continuous integration using Jenkins, microservice containerization using multi-stage Docker profiles, configuration management via Ansible automation, and system observability using Prometheus and Grafana.

🏗️ System Architecture Overview
The production infrastructure is separated into a two-node decentralized cluster running within an AWS Virtual Private Cloud (VPC) network interface layout:

Control Node & Monitoring Station (172.31.45.158 / 54.172.189.109)

Hosts the Ansible Automation Engine.

Orchestrates container lifecycles remotely across the private network subnet.

Runs isolated Prometheus and Grafana telemetry systems.

Target Application & Jenkins Node (172.31.42.71 / 54.159.216.133)

Powers the automated Jenkins CI Server (Port 8080).

Hosts the live FastAPI Inventory Application container (Port 8000).

Executes background Node Exporter telemetry hooks (Port 9100) for infrastructure scraping.

🛠️ Step-by-Step Implementation Breakdown
Phase 1: Microservice Containerization
We optimized the core FastAPI application codebase utilizing a secure, space-efficient Multi-Stage Dockerfile.

The Strategy: The structural builder stage leverages a Python base image to build required dependencies into local wheel caches. The clean runner production layer extracts only these raw binary artifacts, omitting extraneous compilation tools.

Security Hardening: The layer strips default root execution privileges by creating an isolated system identity boundary (USER appuser) to block container-escape exploitation vectors.

Phase 2: Continuous Integration Pipeline (Jenkins)
The deployment lifecycle leverages a structured script (Jenkinsfile) tied directly to source control tracking:

Source Checkout: Hooks into the tracking branch at https://github.com/YASH-OG/shopeasy-inventory-service.

Docker Build: Builds and compiles the images locally on the target node.

Registry Push: Securely injects credentials using Jenkins environment variables (dockerhub-credentials-id), tags the image build context, and ships the resulting asset to the public cloud registry container at yashog/shopeasy_devops:latest.

Phase 3: Infrastructure Playbook Orchestration (Ansible)
We resolved directory and credential mapping issues by standardizing key storage protocols (shopeasyjenkins.pem), locking down security rules with strict permissions (chmod 400), and establishing seamless execution parameters:

The Automation Loop: The playbook (deploy.yml) runs across the private cloud loop to ensure Docker is active, pulls the fresh image layers directly from Docker Hub, drops stale runtime containers, and deploys the production service container bound directly to port 8000.

Phase 4: Production Telemetry & Observability
We resolved standard data metric pipeline drops by deploying a dedicated metrics scraper layer directly onto the application node:

Node Exporter: Installed using container host network virtualization layout boundaries (--net=host) on the app node to securely broadcast real-time CPU utilization, storage arrays, and memory maps on Port 9100.

Prometheus: Configured via custom targets block maps (prometheus.yml) to collect endpoint telemetry streams over internal AWS interfaces (172.31.42.71:9100).

Grafana: Connected to the time-series database on the local instance network layer, importing pre-built operational dashboard tracking frameworks (Dashboard ID: 1860) to visualize live performance analytics.

📂 Code Repository Directory Manifest
Ensure your project submission folder is structured exactly like this:

Plaintext
Yash_ShopEasy_DevOps_Project/
├── Dockerfile                  # Multi-stage optimized application compilation manifest
├── docker-compose.yml          # Consolidated multi-container environment descriptor
├── Jenkinsfile                 # Automated CI declarative build step pipeline script
├── hosts                       # Ansible infrastructure location inventory manifest (NO EXTENSION)
├── deploy.yml                  # Ansible playbook containing production orchestration tasks
├── Project_Report.pdf          # 1-2 page operational challenge report file 
└── screenshots/
    ├── FastAPI_Live.png        # Screenshot showing running app docs via browser on Port 8000
    ├── Jenkins_StageView.png   # Screenshot showing successful green Jenkins build sequence
    └── Grafana_Dashboard.png   # Screenshot showing active live telemetry graph visualization
⚙️ Configuration File Blueprints
1. Dockerfile
Dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
2. hosts (Ansible Inventory)
Ini, TOML
[prod_servers]
production_node ansible_host=172.31.42.71 ansible_user=ubuntu ansible_ssh_private_key_file=./shopeasyjenkins.pem
3. deploy.yml (Ansible Playbook)
YAML
---
- name: Deploy ShopEasy Inventory Service to Production
  hosts: prod_servers
  become: yes
  tasks:
    - name: Ensure Docker is installed on the production node
      apt:
        name: docker.io
        state: present
        update_cache: yes

    - name: Pull the latest Docker image from Hub
      docker_image:
        name: yashog/shopeasy_devops
        tag: latest
        source: pull
        force_source: yes

    - name: Stop older container if running
      docker_container:
        name: shopeasy-inventory-app
        state: absent

    - name: Run fresh production container bound to port 8000
      docker_container:
        name: shopeasy-inventory-app
        image: yashog/shopeasy_devops:latest
        state: started
        restart_policy: always
        published_ports:
          - "8000:8000"
🏁 Operational Verification Routes
Interactive API Playground UI: http://54.159.216.133:8000/docs

Jenkins Automation Dashboard: http://54.159.216.133:8080

Prometheus Target Diagnostic UI: http://54.172.189.109:9090/targets

Grafana Live Observability Desk: http://54.172.189.109:3000