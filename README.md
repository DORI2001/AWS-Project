# MailNet

A serverless mailing list platform built on AWS. Users can subscribe to groups and receive email broadcasts from admins.

**Live site:** https://mailnet.pages.dev

---

## What it does

- Browse mailing groups and subscribe with an email address
- Admin dashboard to create groups, send messages, and delete groups
- Messages trigger an email to every subscriber in the group

---

## Architecture

```
Browser → API Gateway → Lambda → DynamoDB
                                      ↓
                              S3 (message storage)
                                      ↓
                                    SQS
                                      ↓
                              Lambda → SES → subscribers
```

| Service | Role |
|---|---|
| API Gateway | REST API |
| Lambda (Python 3.9) | Business logic |
| DynamoDB | Groups and subscribers |
| S3 | Message storage |
| SQS | Async email trigger |
| SES | Email delivery |
| Secrets Manager | Admin credentials |
| Cloudflare Pages | Frontend hosting |

---

## API

| Method | Route | Description |
|---|---|---|
| GET | `/groups` | List all groups |
| POST | `/groups` | Create a group |
| DELETE | `/groups/{group-id}` | Delete a group |
| POST | `/groups/{group-id}` | Subscribe an email |
| POST | `/groups/{group-id}/post` | Send message to group |
| GET | `/authorize` | Admin login |

---

## Deploy

**Requirements:** AWS CLI, SAM CLI, Python 3.9

```bash
sam build && sam deploy --guided
```

On first deploy you'll be prompted for stack name, region, and IAM permissions. Settings are saved to `samconfig.toml` for subsequent deploys.

---

## Project structure

```
├── create_group/       # POST /groups
├── delete_group/       # DELETE /groups/{id}
├── view_groups/        # GET /groups
├── join_group/         # POST /groups/{id}
├── send_post/          # POST /groups/{id}/post
├── send_email/         # SQS consumer → SES
├── authorize/          # Admin auth via Secrets Manager
├── front-end/
│   └── website/
│       └── index.html  # Frontend
└── template.yaml       # SAM infrastructure definition
```
