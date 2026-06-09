# Football Live Scores Platform - DevSecOps Final Project

## Overview

This project is a complete DevSecOps platform designed to deliver live football scores, upcoming fixtures, match details, team lineups, standings, and football statistics.

The application is built using Python Flask and deployed on AWS using modern DevOps and Infrastructure as Code practices.

The platform currently supports:

* English Premier League
* Spanish La Liga
* Italian Serie A
* French Ligue 1
* German Bundesliga
* UEFA Champions League

Future improvements include:

* FIFA World Cup 2026
* Historical match archive
* Multi-provider football APIs
* Enhanced monitoring and observability

---

## Project Goals

The objective of this project is to demonstrate the implementation of a complete DevSecOps lifecycle:

* Application Development
* Source Control Management
* Continuous Integration
* Continuous Delivery
* Containerization
* Infrastructure as Code
* Kubernetes Orchestration
* Security Scanning
* Cloud Deployment

---

## Architecture

User
↓
AWS Application Load Balancer
↓
Amazon EKS Cluster
↓
Kubernetes Deployment
↓
Flask Application
↓
Football APIs

Infrastructure is provisioned using Terraform.

Application delivery is automated using GitHub Actions.

---

## Technology Stack

### Backend

* Python 3.12
* Flask
* Requests

### DevOps

* Git
* GitHub
* GitHub Actions

### Containerization

* Docker
* Docker Hub

### Cloud

* AWS
* Amazon EKS
* IAM
* VPC
* Application Load Balancer

### Infrastructure as Code

* Terraform

### Kubernetes

* Deployment
* Service
* Ingress
* Horizontal Pod Autoscaler

### Security

* Bandit
* Trivy
* GitHub OIDC Authentication

---

## CI/CD Pipeline

The GitHub Actions pipeline performs:

1. Source Code Checkout
2. Python Security Scan (Bandit)
3. Docker Image Build
4. Container Vulnerability Scan (Trivy)
5. Docker Image Push
6. AWS Authentication using OIDC
7. Kubernetes Deployment

---

## Security Features

### Bandit

Static code analysis for Python security issues.

### Trivy

Container image vulnerability scanning.

### OIDC Authentication

Secure AWS authentication without storing AWS access keys.

---

## High Availability

The application runs with:

* 3 Kubernetes replicas
* Rolling Updates
* Pod Anti-Affinity
* Health Checks
* Horizontal Pod Autoscaler

This ensures service continuity and resilience.

---

## Monitoring and Scalability

The Kubernetes cluster supports:

* Horizontal Pod Autoscaling
* Load Balancing
* Automatic Self-Healing

Future enhancements:

* Prometheus
* Grafana
* CloudWatch Integration

---

## Deployment Process

Developer pushes code to GitHub.

GitHub Actions automatically:

* Executes security checks
* Builds Docker images
* Scans containers
* Pushes images to Docker Hub
* Deploys updates to Kubernetes

---

## Project Structure

app/
docker/
k8s/
terraform/
data/
.github/workflows/

---

## Future Improvements

* FIFA World Cup 2026 support
* Football-Data.org fallback API
* Match history persistence
* Advanced statistics
* Prometheus Monitoring
* Grafana Dashboards

---

## Contributors

* Kevin 
* Ilya

