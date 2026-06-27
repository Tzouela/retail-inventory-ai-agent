# Retail Inventory AI Agent — Backend

An agentic AI system that autonomously monitors retail stock levels,
analyzes sales patterns, and generates reorder recommendations for human approval.

## Stack
- **Agent Framework:** Strands Agents SDK
- **LLM:** Amazon Bedrock (Claude Haiku 4.5 via global inference profile)
- **API:** FastAPI with async streaming
- **Database:** MySQL (Docker locally, RDS MySQL 8.0 for deployment)
- **Containerization:** Docker + Docker Compose
- **Cloud:** AWS AgentCore Runtime (eu-north-1)
- **Auth:** Amazon Cognito (JWT)

---

## Architecture
User Request

→ AgentCore Runtime (eu-north-1)

→ Main Agent (orchestrator)

→ check_low_stock tool → RDS MySQL

→ get_sales_velocity tool → RDS MySQL

→ inventory_analysis_agent (sub-agent)

→ Structured reorder report (Pydantic)

→ Human approval gate

---

## Agent Capabilities

- **Autonomous stock check** — queries real inventory data without user prompting
- **Sales velocity analysis** — calculates avg daily/weekly sales over 60 days
- **Priority classification** — Critical/High/Medium based on stock levels and velocity
- **Reorder calculation** — formula: (avg_weekly_sales × 2) + (min_qty - current_qty)
- **Structured output** — Pydantic model ensures consistent response format
- **Human-in-the-loop** — no orders placed without explicit manager approval

---

## Database Schema

Three normalized tables with foreign key relationships:
products (product_id PK, name, brand, category, sku UNIQUE, supplier, price DECIMAL, description)

↓ one-to-many

stock (stock_id PK, product_id FK, size, colour, quantity, minimum_quantity, last_updated)

↓ one-to-many

sales (sale_id PK, stock_id FK, quantity_sold, price_sold DECIMAL, date_sold)

**Key design decisions:**
- `DECIMAL(10,2)` for prices — exact arithmetic, no floating point errors
- `size` and `colour` in `stock` not `products` — each variant tracked independently
- `last_updated` with `ON UPDATE CURRENT_TIMESTAMP` — auto-maintained by MySQL
- Modular migrations (`001_`, `002_`, `003_`) for versioned schema changes

---

## Local Development

### Prerequisites
- Docker Desktop
- Python 3.11+
- AWS CLI configured with `eu-north-1` credentials

### Start locally
```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make dev
```

Agent runs at `http://localhost:8081`

### Test
```bash
curl -X POST http://localhost:8081/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Run a stock check and tell me which products need reordering."}'
```

---

## AWS Deployment (Module 3)

### Infrastructure
- **AgentCore Runtime:** `inventory_agent` (eu-north-1)
- **ECR Repository:** `inventory-ai-agent`
- **RDS:** MySQL 8.0 on `db.t3.micro` (provisioned temporarily for documentation)
- **Cognito:** User Pool `inventory-agent-users` with web + M2M clients
- **CloudFormation Stack:** `inventory-ai-agent`

### Deploy
```bash
# Build and push Docker image to ECR
make build-and-push

# Deploy CloudFormation stack
make deploy

# Get endpoint URL
make outputs
```

### Architecture decisions
- **eu-north-1** — AWS account region, AgentCore Runtime available here
- **Global inference profile** — `global.anthropic.claude-haiku-4-5-20251001-v1:0` required for on-demand invocation
- **Public RDS** — temporary demo deployment; production would use private VPC
- **Cognito JWT** — matches workshop pattern; allows both browser (Authorization Code) and service (Client Credentials) auth
- **RDS torn down after documentation** — cost-conscious decision; local Docker MySQL used for development

### Deployed endpoint
https://bedrock-agentcore.eu-north-1.amazonaws.com/runtimes/arn%3Aaws%3Abedrock-agentcore%3Aeu-north-1%3A626230556988%3Aruntime%2Finventory_agent-1EKutF8qhR/invocations?qualifier=DEFAULT

---

## Environment Variables

| Variable | Purpose | Local Value |
|----------|---------|-------------|
| `AWS_REGION` | General AWS services | `eu-north-1` |
| `AGENT_MODEL_ID` | Bedrock model | `global.anthropic.claude-haiku-4-5-20251001-v1:0` |
| `DB_HOST` | MySQL host | `127.0.0.1` (local) / RDS endpoint (deployed) |
| `DB_PORT` | MySQL port | `3307` (local Docker) / `3306` (RDS) |
| `DB_NAME` | Database name | `inventory_db` |
| `DB_USER` | Database user | `inventory_user` |
| `DB_PASSWORD` | Database password | `inventory_pass` |
| `USER_POOL_ID` | Cognito User Pool | `eu-north-1_TgT8wxrUh` |
| `WEB_CLIENT_ID` | Cognito web client | `4sun6m6qko1qg8g30eh3dsv493` |
| `M2M_CLIENT_ID` | Cognito M2M client | `31b2b17sqsrct8hc8l31gedue7` |
