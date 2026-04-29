# AWS Cloud Resume Challenge

![Backend](https://github.com/nagutm/aws-cloud-resume-challenge/actions/workflows/backend.yml/badge.svg)
![Frontend](https://github.com/nagutm/aws-cloud-resume-challenge/actions/workflows/frontend.yml/badge.svg)

My implementation of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/aws/) on AWS, with all infrastructure managed by Terraform and deployments automated through GitHub Actions.

Live site: [resume-mufaddal.com](https://resume-mufaddal.com)

## Architecture

A static resume site served from S3 via CloudFront, with a visitor counter backed by Lambda and DynamoDB.

```
Diagram will be uploaded here - TBA
```

When a visitor loads the page, the browser fetches `index.html` from CloudFront (served from a private S3 bucket via Origin Access Control), then makes a separate `fetch()` to API Gateway. That request invokes a Lambda which atomically increments a counter in DynamoDB and returns the new value.

## AWS services used

- **S3** — static site hosting
- **CloudFront** — HTTPS, caching, custom domain
- **Route 53** — DNS
- **ACM** — TLS certificate
- **API Gateway** — HTTP API for the visitor counter
- **Lambda** — counter logic (Python 3.12)
- **DynamoDB** — counter storage
- **IAM** — roles, policies, OIDC trust for GitHub Actions
- **CloudWatch** — Lambda logs

## Tech stack

- **Infrastructure as code:** Terraform
- **Back end:** Python 3.12, boto3
- **Tests:** pytest, moto
- **CI/CD:** GitHub Actions with OIDC authentication to AWS
- **Front end:** plain HTML, CSS, and JavaScript

## Repo layout

```
.
├── frontend/              # static site
│   └── index.html
├── backend/
│   ├── lambda/            # Lambda source
│   │   └── handler.py
│   ├── tests/             # pytest + moto tests
│   ├── conftest.py
│   └── requirements-dev.txt
├── infrastructure/
│   ├── bootstrap/         # one-time S3 + DynamoDB for remote state
│   └── main/              # everything else
└── .github/workflows/
    ├── backend.yml        # tests, terraform plan/apply
    └── frontend.yml       # S3 sync + CloudFront invalidation
```

## CI/CD

Two workflows trigger on path-filtered changes:

**Backend** runs on changes to `backend/**` or `infrastructure/**`. On PRs it runs pytest, `terraform fmt -check`, and `terraform plan`. On merge to `main` it additionally runs `terraform apply`.

**Frontend** runs on changes to `frontend/**`. It syncs the directory to S3 with `--delete` and creates a CloudFront invalidation.

Authentication uses GitHub OIDC — no long-lived AWS access keys are stored as secrets.
