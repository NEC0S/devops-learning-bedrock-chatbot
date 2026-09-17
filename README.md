# Simple Bedrock Chatbot (Terraform + GitHub Actions)

A chatbot with memory, built on:
- **Amazon Bedrock** (Amazon Nova Micro — the cheapest text model on Bedrock) — generates responses
- **Lambda** (Python) — runs the chat logic
- **DynamoDB** — stores conversation history per `session_id` (this is the "memory")
- **API Gateway (HTTP API)** — exposes a `POST /chat` endpoint

Terraform provisions everything. GitHub Actions runs `plan` on pull requests
and `apply` automatically when you merge to `main`.

## Model access

AWS retired the manual "Model access" page. Serverless models like Amazon
Nova Micro are now automatically enabled the first time your account invokes
them — nothing to set up beforehand. Just make sure `bedrock_model_id` in
`variables.tf` is set to a model available in `eu-north-1` (Nova Micro is,
by default).

If you ever switch to an Anthropic model instead, note first-time users may
need to submit brief use-case details before Anthropic models become
invokable — Amazon's own Nova models don't have this requirement.

This is cheap, not free — expect a few cents at most for heavy testing, but
Bedrock has no ongoing free token allowance.

## Setup

1. **Push this repo to GitHub** (folder structure must stay intact —
   `.github/workflows/terraform.yml` and `lambda/chatbot.py` must keep their paths).

2. **IAM user**: create/reuse an IAM user with permissions for Lambda, DynamoDB,
   IAM (to create the role), API Gateway, and Bedrock. For learning purposes,
   attaching `AdministratorAccess` is simplest — scope it down later.

3. **GitHub repo secrets** (Settings → Secrets and variables → Actions):
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

4. **Push to `main`** — GitHub Actions will provision everything.

5. Check the **Terraform Apply** step's log for the `chat_endpoint` output,
   e.g. `https://abc123.execute-api.us-east-1.amazonaws.com/chat`.

## Testing the chatbot

```bash
curl -X POST https://YOUR-ENDPOINT/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test1", "message": "Hi, my name is Alex."}'
```

Then send a follow-up with the **same** `session_id` — it should remember your name:

```bash
curl -X POST https://YOUR-ENDPOINT/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test1", "message": "What is my name?"}'
```

Change `session_id` to start a fresh conversation with no memory of the previous one.

## Notes / next steps

- Costs are pay-per-use (Bedrock tokens, Lambda invocations, DynamoDB requests,
  API Gateway requests) — this is cheap for testing but not free.
- Add a TTL attribute in DynamoDB to auto-expire old sessions.
- Add an API key or Cognito authorizer on the API Gateway route so it's not
  wide open to the internet.
- Swap long-lived AWS keys for GitHub OIDC + an IAM role once comfortable.