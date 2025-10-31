# Inventory Analytics System

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

**Inventory Analytics System** is a professional, comprehensive solution for managing and analyzing inventory data in businesses, stores, and warehouses. The system tracks stock levels, generates intelligent reports, and automates ETL tasks using scheduled workflows, all while supporting Docker deployment for easy setup.

---

## 🌟 Key Features
- **Inventory Management:** Add, update, and remove products with full tracking.
- **Analytics & Reporting:** Generate smart reports on inventory levels, sales trends, and stock movements.
- **ETL Automation:** Schedule automated tasks with Apache Airflow.
- **Docker Ready:** Run the system easily using Docker and Docker Compose.
- **Flexible & Extensible:** Ready for further integration with other business systems.
- **Multi-Environment Support:** Works in local, development, and production setups.

---

## ⚙️ Requirements
- Python 3.10+
- Docker & Docker Compose
- Apache Airflow (for running ETL tasks)
- Python dependencies (`requirements.txt`)

---

## 🚀 Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/Ahmedsalah554/Inventory_Analytics_System.git
cd Inventory_Analytics_System
```

## 2. Install dependencies (optional if using Docker)
pip install -r requirements.txt

## 3. Run with Docker
docker-compose up --build

## 4. Access the system
Airflow UI: http://localhost:8080
Customize tasks in airflow/dags as needed.

## 🗂 Project Structure

```
Inventory_Analytics_System/
│
├── api/               # API endpoints for managing data
├── dags/              # Scheduled ETL tasks using Airflow
├── data/              # Sample or stored data files
├── logs/              # Log files
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile         # Docker image configuration
└── requirements.txt   # Python dependencies
```


