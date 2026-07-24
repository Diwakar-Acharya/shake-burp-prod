# 🚀 Shake&Burp — AWS Production Deployment & Architecture

[![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com/)
[![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20S3%20%7C%20RDS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-RDS-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Cache%20%26%20Broker-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)

> The world's first custom UV DTF insulated shaker bottle e-commerce platform built with Django 5, multi-container Docker orchestration, and deployed on AWS Cloud Infrastructure (EC2, S3, RDS).

---

## 🏗️ Architecture Overview

```
                      [ CLIENT / BROWSER ]
                               │
                       Port 80 / 443 (HTTP/HTTPS)
                               ▼
                   ┌───────────────────────┐
                   │  EC2: Nginx Gateway   │
                   └───────────┬───────────┘
                               │ (Docker Internal Network)
                               ▼
                   ┌───────────────────────┐
                   │   Web Container       │
                   │  (Django + Gunicorn)  │
                   └───────┬───────────┬───┘
                           │           │
                           ▼           ▼
             ┌───────────────────┐   ┌───────────────────┐
             │  AWS RDS (Postgres│   │  Redis Container  │
             │  AWS S3 (Media)   │   │  (Message Broker) │
             └───────────────────┘   └─────────┬─────────┘
                                               │
                                               ▼
                                     ┌───────────────────┐
                                     │ Celery Container  │
                                     │ (Async Worker)    │
                                     └───────────────────┘
```

---

## ⚡ Tech Stack & Technologies

* **Core Backend**: Django 5.0 (Python 3.13), Gunicorn WSGI Server.
* **Async Workers**: Celery 5.4 with Redis 7 Broker.
* **Database**: AWS RDS PostgreSQL 15.
* **Object Storage**: AWS S3 Bucket (`django-storages` + `boto3`).
* **Reverse Proxy**: Nginx (Alpine Linux) with Gzip compression & static asset caching.
* **Orchestration**: Docker & Docker Compose v2.
* **Frontend**: HTML5, Custom Glassmorphism CSS, React Canvas Background Animations bundle.

---

## 📋 Prerequisites & AWS Setup

### 1. AWS S3 Bucket
1. Create Bucket: `shakeandburp-media-prodn` (Region: `eu-north-1`).
2. Turn OFF **Block all public access**.
3. Attach Bucket Policy in AWS S3 Permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::shakeandburp-media-prodn/*"
        }
    ]
}
```

### 2. AWS RDS (PostgreSQL)
1. Engine: PostgreSQL 15 (Free Tier).
2. DB Identifier: `shakeandburp-db1`.
3. Inbound Security Group Rule: Allow `PostgreSQL` (Port `5432`) from your EC2 Security Group or `0.0.0.0/0`.

### 3. AWS EC2 Instance
1. Instance: Ubuntu 22.04 LTS (t2.micro / t3.micro).
2. Inbound Security Group Rules:
   * `HTTP` (Port `80`) $\rightarrow$ `0.0.0.0/0`
   * `HTTPS` (Port `443`) $\rightarrow$ `0.0.0.0/0`
   * `SSH` (Port `22`) $\rightarrow$ `0.0.0.0/0`

---

## 🚀 Step-by-Step Deployment Guide on AWS EC2

### Step 1: Connect to EC2 & Install Docker
```bash
# SSH into EC2 instance
ssh -i /path/to/key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Install Docker & Git
sudo apt update && sudo apt install -y docker.io docker-compose-v2 git
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
```

### Step 2: Clone Repository
```bash
git clone https://github.com/Diwakar-Acharya/shake-burp-prod.git app
cd app
```

### Step 3: Configure Environment Variables
Create `.env.production` on EC2:
```bash
nano .env.production
```

Paste the following block (fill in your AWS RDS Password & IAM keys):
```ini
DEBUG=False
SECRET_KEY=c89a7f3d09e145b287a6c51d9e20f18a4b3c7e91f5d2b0e6a4c8f1d3e5a7b9c1
ALLOWED_HOSTS=YOUR_EC2_PUBLIC_IP,localhost,127.0.0.1

# AWS RDS PostgreSQL Connection
DATABASE_URL=postgres://postgres:YOUR_RDS_PASSWORD@YOUR_RDS_ENDPOINT:5432/postgres

# Redis & Celery Broker
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0

# AWS S3 Integration
USE_S3=True
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME=shakeandburp-media-prodn
AWS_S3_REGION_NAME=eu-north-1

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=http://YOUR_EC2_PUBLIC_IP
```

### Step 4: Build & Launch Containers
```bash
# 1. Build Production Docker Images
docker compose -f docker-compose.prod.yml build

# 2. Run Database Migrations on AWS RDS
docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate

# 3. Collect Static Files into Shared Volume
docker compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput

# 4. Start all Containers (Nginx, Gunicorn, Celery, Redis) in Background
docker compose -f docker-compose.prod.yml up -d

# 5. Check Container Health Status
docker compose -f docker-compose.prod.yml ps
```

---

## 🔐 Creating Superuser & Adding Products

1. Create Admin Account on EC2:
```bash
docker compose -f docker-compose.prod.yml run --rm web python manage.py createsuperuser
```
2. Open Admin Panel: `http://YOUR_EC2_PUBLIC_IP/manage-sb-x9k2/`
3. Log in $\rightarrow$ Click **Products** $\rightarrow$ **Add Product** $\rightarrow$ Upload images (automatically stored on AWS S3).

---

## 💻 Local Development Setup (Mac / Linux)

```bash
# Clone repository locally
git clone https://github.com/Diwakar-Acharya/shake-burp-prod.git
cd shake-burp-prod

# Install Dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py migrate

# Start Local Server
python manage.py runserver
```
Visit locally at: `http://127.0.0.1:8000`

---

## 🛡️ License

Distributed under the MIT License. See `LICENSE` for more information.
