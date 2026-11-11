# AetherOS

Distributed Cloud Infrastructure Simulator & Autonomous Resource Management Platform.

## 🚀 Overview
AetherOS is an Expert-level, full-stack infrastructure engineering platform. It allows administrators to simulate distributed cloud environments, allocate virtual machines using intelligent algorithms, visualize network topologies, and monitor live infrastructure events.

## 🛠️ Technology Stack
* **Backend:** Python, FastAPI, SQLAlchemy, Alembic
* **Microservice:** C++ (cpp-httplib, nlohmann/json, CMake)
* **Database:** PostgreSQL
* **Messaging:** Redis Pub/Sub
* **Frontend:** React, TypeScript, Tailwind CSS, React Flow, Recharts
* **Infrastructure:** Docker, Docker Compose

## ✨ Key Features
* Polyglot Architecture: FastAPI backend communicating with a high-performance C++ microservice.
* Intelligent Allocation: Implements First-Fit, Best-Fit, Worst-Fit, and Balanced resource allocation strategies.
* Dijkstra Network Routing: Calculates the shortest network path between infrastructure nodes.
* Load Balancing: Supports Round Robin and Least Connections routing for simulated traffic.
* Real-Time Monitoring: Redis Pub/Sub and WebSockets stream live infrastructure events directly to the React dashboard.
* Interactive Visualizations: React Flow graph for network topology and Recharts for cluster resource utilization.

## 🚦 Getting Started

### Prerequisites
* Docker Desktop installed and running.

### Installation
1. Clone the repository:
   `git clone https://github.com/Adijah6838/aetheros.git`
2. Setup environment variables:
   `cp .env.example .env`
3. Build and start the cluster:
   `docker compose up -d --build`
4. Apply database migrations:
   `docker compose exec api alembic upgrade head`

### Access
* **Frontend:** http://localhost:5173
* **Backend API Docs:** http://localhost:8000/docs
