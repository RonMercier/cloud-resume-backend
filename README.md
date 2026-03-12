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

The architecture follows the guidebook’s requirement to define all API, Lambda, and DynamoDB resources via IaC and deploy them using the SAM CLI rather than the AWS Console.

## Repository Structure
```
.
├── src/
│   ├── app.py                # Lambda handler (visitor counter logic)
│   └── requirements.txt      # Third-party dependencies (optional/empty)
├── tests/                    # pytest tests
├── template.yaml             # SAM template (IaC)
├── samconfig.toml            # Auto-created after first deploy
└── .github/workflows/
    └── deploy.yml            # CI/CD pipeline using OIDC + SAM
```
If requirements.txt is empty, SAM shows “requirements.txt not found, continuing without dependencies,” which is normal and safe.

## SAM Template Summary

The template.yaml defines:

- DynamoDB table (visitorCount)
- Lambda function (visitor-counter-lambda)
- HTTP API route (GET /count)
- CORS config for https://ron-mercier101.com
- IAM role allowing Lambda CRUD access to the table

SAM is used instead of console clicking because the challenge requires full automation via Infrastructure as Code.

## Local Development (Fedora is my goto OS, search for the commands equivalent to your OS)

Prerequisites
- Python 3.12
- pip
- AWS SAM CLI
- Git

## Install Tools
```
sudo dnf install -y python3 python3-pip git
pip install --user aws-sam-cli
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

## Create a Python 3.12 venv
```
python3.12 -m ensurepip --upgrade
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## Build the app
```
sam build
```
If build errors occur because SAM can’t find pip, you can also build inside a container using sam build --use-container.

## Deploying the Backend
```
sam deploy --guided
```
Seeing this the first time is normal:
```
Looking for config file [samconfig.toml]: Not found
```

SAM will ask deployment questions and then auto-generate samconfig.toml for future runs.

After deployment, SAM prints:
- API Endpoint
- DynamoDB Table
- Lambda Function Name

These outputs are used for frontend integration and smoke testing.

## API Contract

GET /count

Returns the current visitor count and may increment the value depending on handler logic.

Example response:
```
{
  "count": 42
}
```

CORS is configured for:
```
https://ron-mercier101.com
```
If you change your site URL later, update the CORS settings in the SAM template.

## Testing
Unit Tests (Pytest)

Put tests under tests/:
```
pytest
```
Smoke test (recommended)

After deployment, call the real API Gateway URL to confirm:
- Lambda executes correctly
- DynamoDB updates
- API returns a valid response

The guidebook strongly recommends smoke tests as the best measure of successful IaC + CI/CD deployments.
