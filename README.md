# Cloud Resume Challenge — Backend (AWS SAM)
Serverless backend powering my Cloud Resume Challenge.
Implements a visitor counter API using AWS Lambda, API Gateway (HTTP API), and DynamoDB, all deployed via AWS SAM and automated with GitHub Actions CI/CD.

This backend corresponds to Steps 12–14 of the Cloud Resume Challenge guidebook, which requires:
- Infrastructure as Code using AWS SAM
- A dedicated backend GitHub repo
- Automated CI/CD for Lambda + API deployments

## Architecture
High‑level Overview

<img width="4032" height="497" alt="image" src="https://github.com/user-attachments/assets/896b44f5-131e-47c2-b3dd-b4c29ef4ace6" />


## Components
| Component                  | Purpose                                          |
|----------------------------|--------------------------------------------------|
| API Gateway (HTTP API)     | Exposes the /count endpoint                      |
| Lambda (Python)            | Reads/updates visitor count                      |
| DynamoDB (Pay_PER_REQUEST) | Stores the count (cheap and Scalable)            |
| SAM Template               | Defines the entire backend IaC stack             |
| GitHub Actions             | Test -> Build -> Deploy (no manual console work) |
