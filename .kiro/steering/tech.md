# Technology Stack

## Core Technologies

### Languages & Frameworks
- **Python 3.x**: Primary language for all agents and services
- **TypeScript**: Type-safe JavaScript for frontend development
- **React 18**: UI framework with hooks and concurrent features
- **FastAPI**: Modern Python web framework with automatic OpenAPI docs
- **YAML**: Configuration and infrastructure definitions
- **Shell Scripts**: Deployment automation (bash/PowerShell)

### AWS Services
- **Amazon Bedrock**: Claude (AI consultants), Titan (vector embeddings)
- **Amazon ECS Fargate**: Container orchestration for Agent Core runtime
- **Amazon DynamoDB**: Knowledge base storage with vector embeddings
- **Amazon S3**: Project storage and artifacts
- **AWS Lambda**: Knowledge synchronization functions
- **Amazon EventBridge**: Scheduled knowledge sync triggers
- **Amazon CloudWatch**: Monitoring and alerting
- **AWS IAM**: Security and access control

### Frontend Technologies
- **Material-UI (MUI) 5**: Component library with theming support
- **Redux Toolkit**: State management with slices
- **React Query**: Server state management and caching
- **CodeMirror 6**: Modern code editor with syntax highlighting
- **Vite**: Fast build tool and dev server
- **Vitest**: Unit testing framework
- **Axios**: HTTP client for API communication

### Backend Technologies
- **Uvicorn**: ASGI server for FastAPI
- **WebSocket**: Real-time bidirectional communication
- **JWT**: JSON Web Tokens for authentication
- **Pydantic**: Data validation and settings management
- **Boto3**: AWS SDK for Python

### MCP Integration
- **16 Specialized MCPs**: 
  - **12 AWS MCPs**: Documentation, Well-Architected, Solutions, Pricing, Security, Serverless, Containers, AI/ML, DevOps, Monitoring, Networking, Agent Core Patterns
  - **4 Additional MCPs**: Strands Agent Resources, GitHub Analysis, Perplexity Research, Filesystem Operations
- **MCP Command**: `uvx` (Python package runner)
- **MCP Configuration**: `mcp-integration/mcp-config.yaml`

### Architecture Pattern
- **Hybrid Serverless**: 90% serverless components, 10% container components
- **Vector Search**: Semantic understanding with 0.7 cosine similarity threshold
- **Intelligent Routing**: Query-based routing to optimal knowledge sources
- **Multi-Source Validation**: 95%+ confidence scoring across sources

## Project Structure

```
agent-builder-platform/
├── agent-core/              # Agent orchestration and workflow coordination
├── agent-core-config/       # AI consultant configuration
├── agents/                  # 5 specialized AI agents
├── api/                     # FastAPI REST API + WebSocket (11 endpoints)
├── frontend/                # React + TypeScript + Material-UI
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── pages/           # Page components
│   │   ├── store/           # Redux state management
│   │   ├── api/             # API client services
│   │   ├── hooks/           # Custom React hooks
│   │   └── theme/           # Material-UI theme
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── infrastructure/          # CloudFormation templates for AWS resources
├── mcp-integration/         # MCP ecosystem, vector search, knowledge service
├── scripts/                 # Deployment and testing automation
├── docs/                    # Comprehensive documentation
├── .kiro/                   # Kiro IDE configuration and specs
│   ├── specs/               # Requirements, design, tasks
│   └── steering/            # Steering documents (this directory)
└── venv/                    # Python virtual environment
```

## Common Commands

### Environment Setup
```bash
# Create virtual environment (Linux/Mac)
python3 -m venv venv
source venv/bin/activate

# Create virtual environment (Windows)
python -m venv venv-windows
.\venv-windows\Scripts\activate
```

### Testing
```bash
# Test MCP ecosystem
python test_mcp_ecosystem.py

# Test orchestrator
python agent-core/test-orchestrator-integration.py

# Test enhanced knowledge service
python mcp-integration/test_enhanced_knowledge_core.py

# Validate configuration
./scripts/validate-config.sh
```

### Frontend Development
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Run tests with coverage
npm run test:coverage
```

### API Development
```bash
# Start FastAPI server
cd api
uvicorn main:app --reload

# Run API tests
python run_all_tests.py

# Generate OpenAPI docs
python generate_api_docs.py
```

### Deployment
```bash
# Deploy AWS infrastructure
./scripts/deploy-infrastructure.sh

# Deploy MCP integration
./scripts/deploy-mcp-integration.sh

# Deploy frontend
./scripts/deploy-frontend.sh

# Test AWS connectivity
./scripts/test-aws-connectivity.sh
```

### Development
```bash
# Run with LocalStack (local AWS simulation)
./scripts/test-with-localstack.sh

# Test vector search
./scripts/test-vector-search.sh

# Generate architecture diagram
pip install diagrams
python generate_architecture_diagram.py
```

## Key Dependencies

### Python Packages
- `asyncio`: Asynchronous operations
- `dataclasses`: Data structure definitions
- `enum`: Enumeration types
- `logging`: Application logging
- `json`: JSON processing
- `typing`: Type hints
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `boto3`: AWS SDK
- `pydantic`: Data validation
- `python-jose`: JWT handling
- `websockets`: WebSocket support
- `diagrams`: Architecture diagram generation (optional)

### Frontend Packages
- `react`: ^18.2.0
- `react-dom`: ^18.2.0
- `@mui/material`: ^5.14.19
- `@mui/icons-material`: ^5.14.19
- `@reduxjs/toolkit`: ^2.0.1
- `@tanstack/react-query`: ^5.14.2
- `@uiw/react-codemirror`: ^4.21.21
- `axios`: ^1.6.2
- `react-router-dom`: ^6.20.1

### External Services
- **Amazon Bedrock**: AI model access (Claude, Titan)
- **Perplexity API**: Research capabilities (requires `PERPLEXITY_API_KEY`)
- **GitHub API**: Repository analysis (requires `GITHUB_TOKEN`)

## Configuration

### Environment Variables
- `PROJECT_NAME`: Project identifier
- `ENVIRONMENT`: Deployment environment (dev/staging/prod)
- `PERPLEXITY_API_KEY`: Perplexity API access
- `GITHUB_TOKEN`: GitHub API access
- `SNS_TOPIC_ARN`: CloudWatch alerts
- `KMS_KEY_ID`: Encryption key

### Key Configuration Files
- `mcp-integration/mcp-config.yaml`: MCP server definitions and sync schedules
- `agent-core-config/config.yaml`: Agent Core configuration
- `infrastructure/*.yaml`: CloudFormation templates
