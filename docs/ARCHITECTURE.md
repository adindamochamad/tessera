# Tessera Architecture

## System Overview

Tessera adalah autonomous AI agent yang mengaudit multi-tenant MongoDB databases untuk detect data isolation violations.

```
┌─────────────────────────────────────────────────────────────┐
│                      Tessera System                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │   Frontend   │────────▶│   Backend    │                 │
│  │   Next.js    │         │   FastAPI    │                 │
│  └──────────────┘         └───────┬──────┘                 │
│                                    │                         │
│                           ┌────────┴────────┐               │
│                           │                 │               │
│                    ┌──────▼─────┐   ┌─────▼────────┐      │
│                    │   Gemini   │   │  MongoDB MCP │      │
│                    │  AI Agent  │   │    Server    │      │
│                    └──────┬─────┘   └─────┬────────┘      │
│                           │                │               │
│                    ┌──────▼────────────────▼─────┐        │
│                    │    MongoDB Atlas            │        │
│                    │  - Collections              │        │
│                    │  - Vector Search            │        │
│                    └─────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Frontend (Next.js)

**Purpose**: User interface untuk interact dengan Tessera agent

**Key Features**:
- Dashboard dengan real-time audit status
- Violations list dengan severity filtering
- Compliance reports dan metrics
- Agent activity logs

**Tech Stack**:
- Next.js 14 (App Router)
- TailwindCSS + shadcn/ui
- Recharts untuk data visualization
- TypeScript

**Directory Structure**:
```
frontend/
├── app/
│   ├── dashboard/         # Main dashboard pages
│   ├── violations/        # Violations list/detail
│   ├── reports/           # Compliance reports
│   └── audit/             # Audit trigger interface
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── dashboard/         # Dashboard-specific components
│   └── charts/            # Chart components
└── lib/
    ├── api.ts             # API client
    └── utils.ts           # Utility functions
```

### 2. Backend (FastAPI)

**Purpose**: REST API dan agent orchestration

**Key Modules**:

#### a. Agent Module (`app/agent/`)
- `tessera_agent.py`: Core autonomous agent logic
- Orchestrates audit workflow
- Integrates dengan Gemini untuk AI analysis
- Manages violation detection lifecycle

#### b. Analyzers Module (`app/analyzers/`)
- `query_analyzer.py`: MongoDB query pattern analyzer
- Rules-based detection untuk common violations
- Extensible rule engine

#### c. MCP Module (`app/mcp/`)
- `client.py`: MongoDB MCP client
- Real-time query log retrieval
- Database inspection via MCP protocol

#### d. API Module (`app/api/`)
- REST endpoints untuk frontend
- Routes: `/audit`, `/violations`, `/reports`
- WebSocket support untuk real-time updates

**Tech Stack**:
- FastAPI (async Python web framework)
- LangChain (agent orchestration)
- Google Cloud Vertex AI (Gemini integration)
- Motor (async MongoDB driver)
- Structlog (structured logging)

**Directory Structure**:
```
backend/
├── app/
│   ├── agent/             # Agent logic
│   ├── analyzers/         # Query analyzers
│   ├── mcp/               # MCP integration
│   ├── api/               # REST API routes
│   └── config.py          # Configuration
├── tests/                 # Unit tests
└── requirements.txt       # Dependencies
```

### 3. AI Layer (Google Gemini)

**Purpose**: Intelligent analysis dan decision making

**Capabilities**:
- Root cause analysis untuk violations
- Natural language explanations
- Remediation code generation
- Pattern recognition

**Integration**:
```python
# Example Gemini usage
from vertexai.generative_models import GenerativeModel

model = GenerativeModel("gemini-2.0-flash")
response = model.generate_content(
    f"Analyze this MongoDB query for tenant isolation issues: {query}"
)
```

**Prompts**:
- System prompt defines agent persona
- Function calling untuk structured output
- Few-shot examples untuk consistent responses

### 4. MongoDB Atlas

**Purpose**: Database storage dan Vector Search

**Collections**:
- `violations`: Detected violations history
- `patterns`: Known violation patterns (for Vector Search)
- `audits`: Audit run metadata
- `demo_*`: Demo multi-tenant collections

**Vector Search Index**:
```json
{
  "name": "violations_index",
  "type": "vectorSearch",
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 768,
      "similarity": "cosine"
    }
  ]
}
```

**Embedding Strategy**:
- Query patterns di-embed dengan Vertex AI Text Embeddings
- Semantic similarity search untuk find related violations
- Continuous learning dari new violations

### 5. MongoDB MCP Server

**Purpose**: Real-time query inspection via Model Context Protocol

**MCP Tools**:
- `mongodb_query`: Execute queries
- `mongodb_find`: Collection queries
- `mongodb_aggregate`: Aggregation pipelines
- `mongodb_get_logs`: Profiler logs

**Integration**:
```python
# Example MCP usage
mcp_client = MongoDBMCPClient(server_url)
logs = await mcp_client.get_query_logs(database="demo", since="2026-05-19")
```

## Data Flow

### Audit Workflow

```
1. User triggers audit via Frontend
   │
   ▼
2. Backend receives request → Creates audit session
   │
   ▼
3. MCP Client fetches query logs dari MongoDB
   │
   ▼
4. Query Analyzer processes each query
   │
   ├─▶ Rule-based detection
   └─▶ Pattern matching
   │
   ▼
5. Violations detected → Send to Gemini untuk analysis
   │
   ▼
6. Gemini generates:
   │ ├─▶ Root cause explanation
   │ ├─▶ Risk assessment
   │ └─▶ Remediation suggestions
   │
   ▼
7. Vector Search finds similar violations dari knowledge base
   │
   ▼
8. Aggregate results → Store ke MongoDB
   │
   ▼
9. Frontend displays violations + compliance score
```

### Vector Search Workflow

```
1. New violation detected
   │
   ▼
2. Extract query pattern: "db.orders.find({status: 'pending'})"
   │
   ▼
3. Generate embedding via Vertex AI:
   pattern → [0.123, -0.456, 0.789, ...]
   │
   ▼
4. Query MongoDB Vector Search:
   $vectorSearch: {
     queryVector: embedding,
     path: "embedding",
     numCandidates: 50,
     limit: 5
   }
   │
   ▼
5. Return top 5 similar violations
   │
   ▼
6. Agent uses similar cases untuk inform remediation
```

## Security Architecture

### Authentication & Authorization
- API key authentication untuk backend endpoints
- Rate limiting untuk prevent abuse
- CORS configuration untuk trusted origins only

### Data Privacy
- Read-only access ke production databases (via MCP)
- Sensitive data masking di logs
- Audit trails untuk all agent actions

### Secrets Management
- Google Secret Manager untuk credentials
- Environment variables tidak committed ke Git
- Service account dengan minimal IAM permissions

## Deployment Architecture

### Cloud Run (Backend)
```yaml
Service: tessera-backend
Region: us-central1
Min instances: 1
Max instances: 10
Memory: 2GB
CPU: 2
Timeout: 300s
```

### Vercel (Frontend)
```yaml
Framework: Next.js
Region: Edge (global CDN)
Build command: npm run build
Environment: Production
```

### MongoDB Atlas
```yaml
Tier: M10 (Production) / M0 (Demo)
Region: us-east-1
Backup: Enabled
Encryption: At rest + in transit
```

## Scalability Considerations

### Horizontal Scaling
- Backend: Cloud Run auto-scales based on traffic
- MongoDB: Atlas handles sharding automatically
- Frontend: Vercel edge network global distribution

### Performance Optimization
- Query log processing: Batch processing untuk efficiency
- Vector Search: Index optimization dengan proper dimensions
- Caching: Redis untuk frequent queries (future)

### Cost Optimization
- Cloud Run: Pay-per-request (no cost when idle)
- MongoDB: M0 free tier untuk demo, M10+ untuk production
- Vertex AI: Gemini 2.0 Flash adalah cost-effective model

## Monitoring & Observability

### Metrics
- Audit duration (p50, p95, p99)
- Violations detected per audit
- API response times
- Error rates

### Logging
- Structured logs dengan Structlog
- Cloud Logging integration
- Query execution traces

### Alerting
- Critical violations detected
- API error rates >5%
- Database connection failures

## Future Architecture Enhancements

### Phase 2
- [ ] PostgreSQL support (row-level security auditing)
- [ ] Real-time streaming audits (vs batch)
- [ ] Custom rule engine (user-defined policies)

### Phase 3
- [ ] Multi-cloud deployment (AWS, Azure)
- [ ] Distributed tracing dengan OpenTelemetry
- [ ] Machine learning untuk anomaly detection

---

**Last Updated**: May 20, 2026
**Version**: 0.1.0
