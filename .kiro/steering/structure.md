# Project Structure and Organization

## Directory Layout

### `/agent-core/`
Core agent orchestration and workflow coordination.

**Key Files:**
- `orchestrator.py`: Main orchestrator for multi-phase agent creation workflow
- `orchestrator_clean.py`: Clean version of orchestrator
- `agent_core_app.py`: Agent Core application entry point
- `test-orchestrator-integration.py`: Integration tests

**Purpose:** Manages workflow phases (requirements, architecture, implementation, testing), user context tracking, and agent state management.

### `/agent-core-config/`
Configuration for AI consultant setup.

**Key Files:**
- `config.yaml`: Agent Core framework configuration

**Purpose:** Defines agent behavior, capabilities, and integration settings.

### `/agents/`
Specialized AI consultant agents with professional personas.

**Key Files:**
- `aws_solutions_architect.py`: AWS Solutions Architect agent (840 lines)
- `architecture_advisor.py`: Architecture Advisor agent (1290 lines)
- `implementation_guide.py`: Implementation Guide agent (2299 lines)
- `testing_validator.py`: Testing Validator agent (1598 lines)
- `strands_builder_integration.py`: Strands Integration agent (1242 lines)

**Purpose:** Expert consultation agents that provide domain-specific guidance with 95%+ confidence. Each agent has:
- Professional communication patterns
- Experience level adaptation (beginner to expert)
- Use case categorization and pattern matching
- Cost estimation and security validation
- Multi-factor confidence scoring

### `/api/`
FastAPI REST API with WebSocket support.

**Key Files:**
- `main.py`: FastAPI application with 11 endpoints
- `workflow_service.py`: Workflow management service
- `session_service.py`: Session management with DynamoDB
- `export_service.py`: Export service with 5 formats (1886 lines)
- `websocket_service.py`: Real-time updates via WebSocket (391 lines)
- `testing_service.py`: Testing and validation endpoints
- `performance_service.py`: Performance optimization and caching

**Purpose:** Provides REST API and WebSocket endpoints for frontend communication, session management, workflow orchestration, and real-time updates.

### `/frontend/`
React + TypeScript + Material-UI web application.

**Key Directories:**
- `src/components/`: Reusable UI components
- `src/pages/`: Page-level components
- `src/store/`: Redux state management
- `src/api/`: API client services
- `src/hooks/`: Custom React hooks
- `src/theme/`: Material-UI theme configuration

**Key Files:**
- `src/pages/AgentBuilderPage.tsx`: Main application page with tabbed interface
- `src/components/ChatInterface.tsx`: Chat interface for consultations
- `src/components/ArchitectureTab.tsx`: AWS architecture visualization
- `src/components/CodeTab.tsx`: Code workspace with file tree and editor
- `src/components/ConfidenceTab.tsx`: Confidence analysis and history
- `src/components/ConfidenceDashboard.tsx`: Real-time confidence dashboard
- `src/components/CodePreviewV2.tsx`: CodeMirror 6 code editor
- `src/components/AWSArchitectureDiagram.tsx`: AWS architecture diagrams with official icons

**Purpose:** Provides user interface for agent creation workflow with real-time updates, confidence tracking, architecture visualization, and code preview.

### `/infrastructure/`
Infrastructure as Code (CloudFormation templates).

**Key Files:**
- `main-stack.yaml`: Core AWS infrastructure (VPC, ECS, DynamoDB, S3)
- `ecs-fargate-config.yaml`: ECS Fargate deployment configuration
- `storage-config.yaml`: S3 and DynamoDB storage configuration

**Purpose:** Defines all AWS resources needed for the platform with security best practices and cost optimization.

### `/mcp-integration/`
MCP ecosystem, vector search, and knowledge service integration.

**Key Files:**
- `mcp_ecosystem.py`: 16-MCP integration system
- `mcp_health_monitor.py`: Real-time MCP health monitoring
- `enhanced-knowledge-service.py`: Knowledge service with vector search (1078 lines)
- `vector_search_system.py`: Bedrock Titan vector search implementation
- `mcp-config.yaml`: MCP server definitions and sync schedules
- `eventbridge-sync-rules.yaml`: Automated knowledge synchronization
- `test_enhanced_knowledge_core.py`: Comprehensive test suite

**Purpose:** Manages all MCP connections, knowledge synchronization, vector search, and intelligent query routing. Provides 95%+ confidence through multi-source validation.

### `/scripts/`
Deployment and testing automation scripts.

**Key Files:**
- `deploy-infrastructure.sh`: Deploy AWS infrastructure
- `deploy-mcp-integration.sh`: Deploy MCP integration
- `validate-config.sh`: Pre-deployment validation
- `test-aws-connectivity.sh`: AWS connectivity tests
- `test-vector-search.sh`: Vector search validation
- `test-with-localstack.sh`: Local AWS simulation testing

**Purpose:** Automates deployment, testing, and validation workflows.

### `/docs/`
Comprehensive project documentation.

**Key Files:**
- `README.md`: Documentation hub
- `complete-architecture.md`: Full system architecture
- `mcp-integration-overview.md`: MCP system details
- `vector-search-guide.md`: Vector search implementation
- `cost-optimization.md`: Budget management
- `security-compliance.md`: Security best practices
- `testing-guide.md`: Testing procedures

**Purpose:** Complete technical documentation for all aspects of the platform.

### Root Level Files

**Status & Validation:**
- `STATUS-DASHBOARD.md`: Current project status (19/27 tasks complete, 70%)
- `COMPLETE-DOCUMENTATION.md`: Comprehensive system documentation
- `.kiro/specs/agent-builder-platform/`: Spec documents (requirements, design, tasks)
- `.kiro/specs/agent-builder-platform/ALIGNMENT-REPORT.md`: Spec-to-implementation alignment
- `.kiro/specs/agent-builder-platform/SYNC-COMPLETE.md`: Synchronization summary

**Test Files:**
- `test_mcp_ecosystem.py`: MCP ecosystem tests
- `test_orchestrator_*.py`: Various orchestrator tests
- `test_integrated_consultation.py`: End-to-end consultation tests
- `api/test_*.py`: API endpoint tests (workflow, export, websocket, session, testing)
- `frontend/src/components/__tests__/`: Frontend component tests

## Code Organization Patterns

### Agent Structure
All agents follow a consistent pattern:
1. **Enums**: Experience levels, use case categories
2. **Dataclasses**: Structured data (recommendations, estimates)
3. **Knowledge Base**: Domain-specific information
4. **Core Logic**: Consultation methods with confidence scoring
5. **Integration**: MCP ecosystem and vector search integration

### Configuration Pattern
- YAML for infrastructure and MCP configuration
- Environment variables for secrets and deployment settings
- Dataclasses for runtime configuration

### Testing Pattern
- Unit tests for individual components
- Integration tests for multi-component workflows
- Validation scripts for pre-deployment checks
- Test files co-located with implementation files

## Naming Conventions

### Files
- Python files: `snake_case.py`
- Config files: `kebab-case.yaml`
- Scripts: `kebab-case.sh` or `.ps1`
- Documentation: `UPPERCASE-WITH-DASHES.md` for status, `lowercase-with-dashes.md` for guides

### Python Code
- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### AWS Resources
- Pattern: `${PROJECT_NAME}-resource-type-${ENVIRONMENT}`
- Example: `agent-builder-aws-knowledge-dev`

## Key Architectural Principles

1. **Modular Design**: Clear separation between orchestration, agents, MCP integration, and infrastructure
2. **Hybrid Serverless**: 90% serverless (Lambda, EventBridge) + 10% containers (ECS Fargate)
3. **Intelligent Routing**: Query-based routing to optimal knowledge sources (vector/text/real-time)
4. **Graceful Degradation**: Automatic fallback mechanisms when services unavailable
5. **Cost Optimization**: Free tier maximization, intelligent caching, batch processing
6. **Security First**: Encryption at rest/transit, IAM least privilege, VPC isolation
