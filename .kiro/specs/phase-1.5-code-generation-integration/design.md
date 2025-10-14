# Design Document: Code Generation Integration

## Overview

This design document outlines the integration of the agent_builder_application's code generation capabilities into the agent-builder-platform. The integration transforms the platform from a consultation-only system into an end-to-end agent creation platform that generates production-ready, deployable agent code.

### Integration Strategy

The integration follows a **modular adapter pattern** where agent_builder_application functionality is adapted to work within the existing agent-builder-platform architecture without disrupting current workflows. Key principles:

1. **Non-Breaking Integration**: Existing consultation workflow remains unchanged
2. **Progressive Enhancement**: Code generation activates after implementation phase
3. **Modular Architecture**: New components integrate via well-defined interfaces
4. **Reusable Components**: Registries and generators are standalone modules
5. **AWS-First Approach**: Primary focus on AWS deployment with optional multi-cloud support
6. **Diagram Integration**: Generated code aligns with AWS architecture diagrams from consultation

### Current Platform Analysis

**Existing Capabilities:**
- 5 specialized AI consultant agents (AWS Solutions Architect, Architecture Advisor, Implementation Guide, Testing Validator, Strands Integration)
- Multi-phase workflow orchestration (Requirements → Architecture → Implementation → Testing → Deployment)
- 16 MCPs for knowledge integration (12 AWS + 4 additional)
- Vector search with Amazon Bedrock Titan embeddings
- FastAPI backend with 11 REST endpoints + WebSocket support
- React + TypeScript + Material-UI frontend with real-time updates
- Confidence tracking system (95%+ confidence baseline)

**Missing Capabilities (To Be Added):**
- Actual code generation (currently only provides guidance)
- Model registry with 49+ AI models (AWS Bedrock prioritized)
- Tool registry with 50+ pre-configured tools
- AWS Bedrock AgentCore deployment configuration generation
- AWS deployment templates (CloudFormation, ECS Fargate, Lambda)
- Interactive code preview and download
- Docker-based testing infrastructure
- AWS cost estimation and optimization tools
- Integration with AWS architecture diagrams from consultation


## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (React + TypeScript)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Chat         │  │ Model        │  │ Tool         │          │
│  │ Interface    │  │ Selector     │  │ Selector     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Code         │  │ Cost         │  │ Test         │          │
│  │ Preview      │  │ Estimator    │  │ Runner       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ REST API + WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Workflow     │  │ Code Gen     │  │ Testing      │          │
│  │ Service      │  │ Service      │  │ Service      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Export       │  │ Deployment   │  │ Cost         │          │
│  │ Service      │  │ Service      │  │ Service      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Core (Orchestrator)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Workflow Phases: Requirements → Architecture →          │   │
│  │  Implementation → Testing → Deployment → Code Generation │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Code Generation Engine (New Module)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Model        │  │ Tool         │  │ Template     │          │
│  │ Registry     │  │ Registry     │  │ Engine       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Code         │  │ Deployment   │  │ Test         │          │
│  │ Generator    │  │ Generator    │  │ Generator    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Component Integration Points

**1. Orchestrator Integration**
- Add new `CODE_GENERATION` phase after `IMPLEMENTATION` phase
- Extract consultation context (model requirements, tools, prompts)
- Trigger code generation service via API

**2. API Layer Integration**
- New endpoints: `/api/code-generation/*`, `/api/models/*`, `/api/tools/*`
- Extend existing `/api/workflow/*` endpoints with code generation triggers
- Add WebSocket events for real-time code generation progress

**3. Frontend Integration**
- New tabs in AgentBuilderPage: "Model Selection", "Tool Selection", "Generated Code"
- Integrate ModelSelector, ToolSelector, and CodePreview components
- Add cost estimation dashboard
- Add test runner interface


## Components and Interfaces

### 1. Model Registry Component

**Purpose**: Centralized registry of 49+ AI models with capabilities, costs, and metadata

**Location**: `agent-builder-platform/code-generation/model_registry.py`

**Interface**:
```python
@dataclass
class ModelInfo:
    model_id: str
    provider: str  # "aws_bedrock", "ollama", "openai"
    name: str
    capabilities: List[str]  # ["text", "vision", "reasoning", "coding"]
    context_window: int
    cost_per_1m_input_tokens: float
    cost_per_1m_output_tokens: float
    max_output_tokens: int
    supports_streaming: bool
    supports_function_calling: bool
    platform_support: List[str]  # ["aws", "local"]
    recommended_use_cases: List[str]

class ModelRegistry:
    def get_all_models(self) -> List[ModelInfo]
    def get_model_by_id(self, model_id: str) -> Optional[ModelInfo]
    def filter_models(self, capabilities: List[str], max_cost: float, 
                     provider: str) -> List[ModelInfo]
    def recommend_models(self, use_case: str, budget: float) -> List[ModelInfo]
    def compare_models(self, model_ids: List[str]) -> Dict[str, Any]
```

**Data Source**: Adapted from agent_builder_application's model registry JSON

**Integration**: 
- AWS Solutions Architect agent queries registry during requirements phase
- Frontend ModelSelector component displays filtered models
- Cost Service uses pricing data for estimates

### 2. Tool Registry Component

**Purpose**: Centralized registry of 50+ pre-configured tools with dependencies and examples

**Location**: `agent-builder-platform/code-generation/tool_registry.py`

**Interface**:
```python
@dataclass
class ToolInfo:
    tool_id: str
    name: str
    category: str  # "rag", "memory", "code_execution", "web", "file_system"
    description: str
    pip_dependencies: List[str]
    platform_support: List[str]  # ["windows", "linux", "macos"]
    requires_api_key: bool
    configuration_params: Dict[str, Any]
    usage_example: str
    documentation_url: str
    strands_compatible: bool

class ToolRegistry:
    def get_all_tools(self) -> List[ToolInfo]
    def get_tool_by_id(self, tool_id: str) -> Optional[ToolInfo]
    def filter_tools(self, category: str, platform: str) -> List[ToolInfo]
    def get_dependencies(self, tool_ids: List[str]) -> List[str]
    def validate_compatibility(self, tool_ids: List[str], 
                              platform: str) -> Dict[str, bool]
```

**Data Source**: Adapted from agent_builder_application's tool registry JSON

**Integration**:
- Implementation Guide agent queries registry during implementation phase
- Frontend ToolSelector component displays categorized tools
- Code Generator includes selected tools in generated code


### 3. Code Generation Engine

**Purpose**: Generate production-ready agent code based on consultation context

**Location**: `agent-builder-platform/code-generation/code_generator.py`

**Interface**:
```python
@dataclass
class GenerationContext:
    session_id: str
    model_id: str
    tool_ids: List[str]
    system_prompt: str
    deployment_target: str  # "aws_bedrock_agentcore", "aws_ecs_fargate", "aws_lambda"
    observability_enabled: bool
    security_level: str  # "basic", "standard", "enhanced"
    requirements: Dict[str, Any]
    architecture: Dict[str, Any]

@dataclass
class GeneratedCode:
    agent_file: str  # Python code
    requirements_file: str  # pip dependencies
    dockerfile: str  # Docker configuration
    readme_file: str  # Documentation
    deployment_scripts: Dict[str, str]  # Platform-specific scripts
    test_files: Dict[str, str]  # Test code
    config_files: Dict[str, str]  # Configuration files

class CodeGenerator:
    def generate_agent_code(self, context: GenerationContext) -> GeneratedCode
    def generate_agentcore_wrapper(self, context: GenerationContext) -> str
    def generate_deployment_config(self, target: str, 
                                   context: GenerationContext) -> Dict[str, str]
    def generate_observability_code(self, context: GenerationContext) -> str
    def generate_security_code(self, context: GenerationContext) -> str
```

**Templates**:
- Base agent template with Strands integration
- AWS Bedrock AgentCore FastAPI wrapper template
- AWS ECS Fargate deployment template
- AWS Lambda deployment template
- AWS CloudFormation infrastructure template
- AWS observability template (CloudWatch, X-Ray, OpenTelemetry)
- AWS security template (Secrets Manager, IAM, KMS)

**Integration**:
- Triggered by orchestrator after implementation phase
- Uses consultation context from workflow state
- Outputs code to session storage for preview/download

### 4. Deployment Configuration Generator

**Purpose**: Generate platform-specific deployment configurations

**Location**: `agent-builder-platform/code-generation/deployment_generator.py`

**Interface**:
```python
@dataclass
class DeploymentConfig:
    platform: str  # "aws" only
    infrastructure_files: Dict[str, str]  # CloudFormation templates
    deployment_scripts: Dict[str, str]  # Bash/PowerShell scripts
    environment_variables: Dict[str, str]
    secrets_config: Dict[str, str]  # AWS Secrets Manager
    monitoring_config: Dict[str, str]  # CloudWatch, X-Ray
    iam_policies: Dict[str, str]  # IAM roles and policies

class DeploymentGenerator:
    def generate_aws_ecs_fargate(self, context: GenerationContext) -> DeploymentConfig
    def generate_aws_lambda(self, context: GenerationContext) -> DeploymentConfig
    def generate_aws_agentcore(self, context: GenerationContext) -> DeploymentConfig
    def generate_aws_cloudformation(self, context: GenerationContext) -> str
```

**AWS Deployment Options**:

1. **AWS Bedrock AgentCore** (Recommended)
   - FastAPI wrapper with /invocations and /ping endpoints
   - ARM64 Docker containers
   - ECR integration
   - OpenTelemetry for X-Ray tracing
   - Session ID handling (33+ characters)

2. **AWS ECS Fargate** (Scalable)
   - CloudFormation templates
   - Auto-scaling configuration
   - Application Load Balancer
   - VPC with private subnets
   - IAM roles and policies

3. **AWS Lambda** (Serverless)
   - Lambda function deployment
   - API Gateway integration
   - Event-driven architecture
   - DynamoDB for state
   - CloudWatch Logs


### 5. Cost Estimation Service

**Purpose**: Provide real-time cost estimates for model usage and infrastructure

**Location**: `agent-builder-platform/code-generation/cost_service.py`

**Interface**:
```python
@dataclass
class CostEstimate:
    model_costs: Dict[str, float]  # Per model costs
    infrastructure_costs: Dict[str, float]  # ECS, Lambda, storage
    total_monthly_estimate: float
    free_tier_savings: float
    cost_breakdown: Dict[str, Any]
    optimization_suggestions: List[str]

class CostService:
    def estimate_model_costs(self, model_id: str, 
                            monthly_requests: int,
                            avg_input_tokens: int,
                            avg_output_tokens: int) -> float
    def estimate_infrastructure_costs(self, deployment_target: str,
                                     expected_load: Dict[str, Any]) -> float
    def calculate_total_cost(self, context: GenerationContext,
                            usage_estimates: Dict[str, Any]) -> CostEstimate
    def suggest_optimizations(self, current_estimate: CostEstimate) -> List[str]
```

**Cost Factors**:
- Model API costs (per 1M tokens)
- ECS Fargate costs (vCPU, memory, hours)
- Lambda costs (invocations, duration, memory)
- Storage costs (S3, DynamoDB)
- Data transfer costs
- Free tier calculations

**Integration**:
- Frontend displays real-time cost estimates
- AWS Solutions Architect uses for budget recommendations
- Cost dashboard shows monthly projections

### 6. Testing Infrastructure Service

**Purpose**: Docker-based testing with live input/output streaming

**Location**: `agent-builder-platform/code-generation/testing_service.py`

**Interface**:
```python
@dataclass
class TestResult:
    test_id: str
    timestamp: datetime
    input_text: str
    output_text: str
    response_time: float
    token_usage: Dict[str, int]
    success: bool
    error_message: Optional[str]
    logs: List[str]

class TestingService:
    def build_test_container(self, generated_code: GeneratedCode) -> str
    def run_test(self, container_id: str, input_text: str) -> TestResult
    def stream_test_output(self, container_id: str, 
                          input_text: str) -> AsyncIterator[str]
    def get_test_history(self, session_id: str) -> List[TestResult]
    def cleanup_container(self, container_id: str) -> None
```

**Testing Workflow**:
1. Build Docker container with generated code
2. Start container with agent code
3. Stream test inputs via WebSocket
4. Stream outputs and logs back to frontend
5. Store test results for history
6. Allow iterative testing and refinement

**Integration**:
- Frontend test runner interface
- WebSocket for real-time streaming
- Testing Validator agent analyzes results


### 7. Context Extraction Service

**Purpose**: Extract code generation parameters from consultation context

**Location**: `agent-builder-platform/code-generation/context_extractor.py`

**Interface**:
```python
@dataclass
class ExtractedContext:
    model_requirements: Dict[str, Any]
    tool_requirements: List[str]
    system_prompt: str
    deployment_preferences: Dict[str, Any]
    budget_constraints: Dict[str, float]
    security_requirements: List[str]
    completeness_score: float
    missing_fields: List[str]

class ContextExtractor:
    def extract_from_workflow(self, workflow_state: WorkflowState) -> ExtractedContext
    def extract_model_requirements(self, requirements_phase: Dict) -> Dict[str, Any]
    def extract_tool_requirements(self, implementation_phase: Dict) -> List[str]
    def extract_system_prompt(self, conversation_history: List[Dict]) -> str
    def validate_completeness(self, context: ExtractedContext) -> Tuple[bool, List[str]]
```

**Extraction Rules**:
- Model requirements from AWS Solutions Architect phase
- Tool requirements from Implementation Guide phase
- System prompts from conversation history
- Deployment preferences from Architecture Advisor phase
- Budget constraints from cost discussions
- Security requirements from Testing Validator phase

**Validation**:
- Check for required fields (model, tools, prompt)
- Validate budget constraints
- Ensure deployment target is specified
- Prompt user for missing information

### 8. Frontend Components

#### ModelSelector Component

**Location**: `agent-builder-platform/frontend/src/components/ModelSelector.tsx`

**Features**:
- Grid/list view of available models
- Filter by provider, capabilities, cost
- Search by name or use case
- Side-by-side comparison
- Cost calculator
- Recommendation engine integration

**Props**:
```typescript
interface ModelSelectorProps {
  onModelSelect: (modelId: string) => void;
  selectedModel?: string;
  budget?: number;
  requiredCapabilities?: string[];
  recommendedModels?: string[];
}
```

#### ToolSelector Component

**Location**: `agent-builder-platform/frontend/src/components/ToolSelector.tsx`

**Features**:
- Categorized tool display (RAG, Memory, Code, Web, etc.)
- Platform compatibility indicators
- Dependency visualization
- Search and filter
- Multi-select with dependency resolution
- Configuration parameter inputs

**Props**:
```typescript
interface ToolSelectorProps {
  onToolsSelect: (toolIds: string[]) => void;
  selectedTools?: string[];
  platform?: string;
  categories?: string[];
}
```

#### CodePreviewEnhanced Component

**Location**: `agent-builder-platform/frontend/src/components/CodePreviewEnhanced.tsx`

**Features**:
- Tabbed interface for multiple files
- Syntax highlighting with CodeMirror 6
- Copy to clipboard
- Download individual files
- Download all as ZIP
- File tree navigation
- Search within files
- Diff view for modifications

**Props**:
```typescript
interface CodePreviewEnhancedProps {
  generatedCode: GeneratedCode;
  onDownload: (format: 'zip' | 'individual') => void;
  onModify?: (fileId: string, content: string) => void;
  readOnly?: boolean;
}
```


#### CostEstimator Component

**Location**: `agent-builder-platform/frontend/src/components/CostEstimator.tsx`

**Features**:
- Real-time cost calculation
- Monthly projection charts
- Cost breakdown by service
- Free tier visualization
- Optimization suggestions
- Budget alerts
- Comparison with alternatives

**Props**:
```typescript
interface CostEstimatorProps {
  modelId: string;
  deploymentTarget: string;
  usageEstimates: UsageEstimates;
  onOptimizationApply?: (optimization: string) => void;
}
```

#### TestRunner Component

**Location**: `agent-builder-platform/frontend/src/components/TestRunner.tsx`

**Features**:
- Input text area
- Real-time streaming output
- Test history
- Performance metrics
- Error display
- Log viewer
- Save test cases

**Props**:
```typescript
interface TestRunnerProps {
  sessionId: string;
  containerId?: string;
  onTestComplete: (result: TestResult) => void;
}
```

## Data Models

### Database Schema Extensions

**New Tables**:

```sql
-- Generated code storage
CREATE TABLE generated_code (
    code_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    generation_timestamp TIMESTAMP NOT NULL,
    model_id VARCHAR(100) NOT NULL,
    tool_ids JSON NOT NULL,
    agent_code TEXT NOT NULL,
    requirements_txt TEXT NOT NULL,
    dockerfile TEXT NOT NULL,
    readme_md TEXT NOT NULL,
    deployment_configs JSON NOT NULL,
    test_files JSON NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Model selections
CREATE TABLE model_selections (
    selection_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    model_id VARCHAR(100) NOT NULL,
    selected_at TIMESTAMP NOT NULL,
    selection_reason TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Tool selections
CREATE TABLE tool_selections (
    selection_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    tool_id VARCHAR(100) NOT NULL,
    selected_at TIMESTAMP NOT NULL,
    configuration JSON,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Test results
CREATE TABLE test_results (
    test_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    code_id VARCHAR(36) NOT NULL,
    test_timestamp TIMESTAMP NOT NULL,
    input_text TEXT NOT NULL,
    output_text TEXT,
    response_time_ms INT,
    token_usage JSON,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    logs JSON,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (code_id) REFERENCES generated_code(code_id)
);

-- Cost estimates
CREATE TABLE cost_estimates (
    estimate_id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    estimated_at TIMESTAMP NOT NULL,
    model_costs JSON NOT NULL,
    infrastructure_costs JSON NOT NULL,
    total_monthly_estimate DECIMAL(10, 2) NOT NULL,
    free_tier_savings DECIMAL(10, 2),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```


## Error Handling

### Error Categories

**1. Code Generation Errors**
- Missing required context (model, tools, prompt)
- Invalid model or tool selection
- Template rendering failures
- Dependency conflicts

**Error Response**:
```python
{
    "error_type": "code_generation_error",
    "message": "Missing required system prompt",
    "details": {
        "missing_fields": ["system_prompt"],
        "suggestions": ["Review implementation phase conversation"]
    },
    "recovery_actions": ["return_to_implementation_phase", "provide_default_prompt"]
}
```

**2. Deployment Configuration Errors**
- Unsupported deployment target
- Invalid infrastructure configuration
- Missing credentials or permissions
- Platform-specific validation failures

**Error Response**:
```python
{
    "error_type": "deployment_config_error",
    "message": "AWS credentials not configured",
    "details": {
        "platform": "aws",
        "required_credentials": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
    },
    "recovery_actions": ["configure_credentials", "use_local_deployment"]
}
```

**3. Testing Errors**
- Docker build failures
- Container runtime errors
- Test execution timeouts
- Resource exhaustion

**Error Response**:
```python
{
    "error_type": "testing_error",
    "message": "Docker container build failed",
    "details": {
        "build_logs": ["..."],
        "failed_step": "pip install -r requirements.txt"
    },
    "recovery_actions": ["fix_dependencies", "use_alternative_packages"]
}
```

**4. Cost Estimation Errors**
- Invalid usage estimates
- Missing pricing data
- Calculation overflow

**Error Response**:
```python
{
    "error_type": "cost_estimation_error",
    "message": "Pricing data unavailable for model",
    "details": {
        "model_id": "anthropic.claude-3-opus-20240229-v1:0",
        "fallback_estimate": 15.00
    },
    "recovery_actions": ["use_fallback_estimate", "select_alternative_model"]
}
```

### Error Recovery Strategies

**Graceful Degradation**:
- Use default templates when custom generation fails
- Provide fallback cost estimates
- Allow manual configuration when auto-extraction fails

**User Guidance**:
- Clear error messages with actionable suggestions
- Link to relevant documentation
- Offer to return to previous workflow phases

**Automatic Retry**:
- Retry transient failures (network, timeouts)
- Exponential backoff for API calls
- Circuit breaker for repeated failures


## Testing Strategy

### Unit Testing

**Model Registry Tests**:
```python
def test_model_registry_get_all_models():
    registry = ModelRegistry()
    models = registry.get_all_models()
    assert len(models) >= 49
    assert all(isinstance(m, ModelInfo) for m in models)

def test_model_registry_filter_by_cost():
    registry = ModelRegistry()
    models = registry.filter_models(max_cost=5.0)
    assert all(m.cost_per_1m_input_tokens <= 5.0 for m in models)

def test_model_registry_recommend_for_use_case():
    registry = ModelRegistry()
    models = registry.recommend_models("code_generation", budget=100.0)
    assert len(models) > 0
    assert all("coding" in m.capabilities for m in models)
```

**Tool Registry Tests**:
```python
def test_tool_registry_get_dependencies():
    registry = ToolRegistry()
    deps = registry.get_dependencies(["rag_tool", "memory_tool"])
    assert "langchain" in deps
    assert "chromadb" in deps

def test_tool_registry_validate_compatibility():
    registry = ToolRegistry()
    result = registry.validate_compatibility(["windows_only_tool"], "linux")
    assert result["windows_only_tool"] == False
```

**Code Generator Tests**:
```python
def test_code_generator_basic_agent():
    generator = CodeGenerator()
    context = GenerationContext(
        session_id="test-123",
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        tool_ids=["rag_tool"],
        system_prompt="You are a helpful assistant",
        deployment_target="aws_lambda"
    )
    code = generator.generate_agent_code(context)
    assert "import boto3" in code.agent_file
    assert "langchain" in code.requirements_file
    assert "FROM python:3.11" in code.dockerfile
```

### Integration Testing

**End-to-End Workflow Test**:
```python
async def test_complete_code_generation_workflow():
    # 1. Create session
    session = await create_session()
    
    # 2. Complete consultation phases
    await complete_requirements_phase(session.session_id)
    await complete_architecture_phase(session.session_id)
    await complete_implementation_phase(session.session_id)
    
    # 3. Trigger code generation
    result = await trigger_code_generation(session.session_id)
    assert result.success == True
    
    # 4. Verify generated code
    code = await get_generated_code(session.session_id)
    assert code.agent_file is not None
    assert code.requirements_file is not None
    
    # 5. Test generated code
    test_result = await run_test(session.session_id, "Hello, world!")
    assert test_result.success == True
```

**Context Extraction Test**:
```python
async def test_context_extraction_from_consultation():
    workflow_state = create_mock_workflow_state()
    extractor = ContextExtractor()
    
    context = extractor.extract_from_workflow(workflow_state)
    
    assert context.model_requirements is not None
    assert len(context.tool_requirements) > 0
    assert context.system_prompt != ""
    assert context.completeness_score >= 0.8
```

### Frontend Testing

**Component Tests**:
```typescript
describe('ModelSelector', () => {
  it('displays all available models', () => {
    render(<ModelSelector onModelSelect={jest.fn()} />);
    expect(screen.getAllByRole('button')).toHaveLength(49);
  });
  
  it('filters models by capability', () => {
    render(<ModelSelector requiredCapabilities={['vision']} />);
    const models = screen.getAllByRole('button');
    expect(models.length).toBeLessThan(49);
  });
  
  it('calls onModelSelect when model is clicked', () => {
    const onSelect = jest.fn();
    render(<ModelSelector onModelSelect={onSelect} />);
    fireEvent.click(screen.getByText('Claude 3 Sonnet'));
    expect(onSelect).toHaveBeenCalledWith('anthropic.claude-3-sonnet-20240229-v1:0');
  });
});
```

**E2E Tests**:
```typescript
describe('Code Generation Flow', () => {
  it('completes full workflow from consultation to code download', async () => {
    // Navigate to agent builder
    await page.goto('/agent-builder');
    
    // Complete consultation
    await completeConsultation(page);
    
    // Select model
    await page.click('[data-testid="model-selector"]');
    await page.click('[data-model-id="claude-3-sonnet"]');
    
    // Select tools
    await page.click('[data-testid="tool-selector"]');
    await page.click('[data-tool-id="rag_tool"]');
    
    // Generate code
    await page.click('[data-testid="generate-code"]');
    await page.waitForSelector('[data-testid="code-preview"]');
    
    // Download code
    const downloadPromise = page.waitForEvent('download');
    await page.click('[data-testid="download-zip"]');
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toContain('.zip');
  });
});
```


## Security Considerations

### 1. Code Generation Security

**Threat**: Malicious code injection via user inputs

**Mitigation**:
- Sanitize all user inputs before template rendering
- Use parameterized templates (Jinja2 with autoescaping)
- Validate generated code against security patterns
- Scan dependencies for known vulnerabilities

**Implementation**:
```python
def sanitize_system_prompt(prompt: str) -> str:
    # Remove potentially dangerous patterns
    dangerous_patterns = [
        r'__import__\(',
        r'eval\(',
        r'exec\(',
        r'os\.system\(',
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, prompt):
            raise SecurityError(f"Dangerous pattern detected: {pattern}")
    return prompt
```

### 2. Secret Management

**Threat**: Hardcoded credentials in generated code

**Mitigation**:
- Always use environment variables for secrets
- Generate AWS Secrets Manager integration code
- Provide .env.example files (never .env with actual values)
- Include security warnings in README

**Generated Code Pattern**:
```python
import os
from aws_secretsmanager import get_secret

# NEVER hardcode credentials
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    API_KEY = get_secret('my-agent/api-key')
```

### 3. Docker Security

**Threat**: Vulnerable Docker images, root user execution

**Mitigation**:
- Use official Python slim images
- Run containers as non-root user
- Scan images for vulnerabilities
- Minimize installed packages

**Dockerfile Template**:
```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 agent
USER agent

# Install dependencies
COPY --chown=agent:agent requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=agent:agent . .

CMD ["python", "agent.py"]
```

### 4. API Security

**Threat**: Unauthorized access to code generation endpoints

**Mitigation**:
- Require authentication for all code generation endpoints
- Rate limiting on generation requests
- Session validation
- CORS configuration

**API Endpoint Protection**:
```python
@app.post("/api/code-generation/generate")
async def generate_code(
    request: GenerateCodeRequest,
    session: Session = Depends(get_current_session),
    rate_limit: None = Depends(rate_limiter)
):
    # Validate session owns the workflow
    if not await validate_session_ownership(session.session_id, request.workflow_id):
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Generate code
    return await code_generator.generate(request)
```

### 5. Data Privacy

**Threat**: Exposure of sensitive user data in generated code or logs

**Mitigation**:
- Redact sensitive data from logs
- Encrypt generated code at rest
- Automatic cleanup of old generated code
- User consent for data retention

**Implementation**:
```python
def log_generation_event(context: GenerationContext):
    # Redact sensitive fields
    safe_context = {
        "session_id": context.session_id,
        "model_id": context.model_id,
        "tool_count": len(context.tool_ids),
        "system_prompt": "[REDACTED]",  # Don't log prompts
    }
    logger.info(f"Code generation started: {safe_context}")
```


## Performance Optimization

### 1. Code Generation Caching

**Strategy**: Cache generated code templates and common patterns

**Implementation**:
```python
from functools import lru_cache
import hashlib

class CodeGeneratorWithCache:
    def __init__(self):
        self.template_cache = {}
        self.generation_cache = {}
    
    def generate_agent_code(self, context: GenerationContext) -> GeneratedCode:
        # Create cache key from context
        cache_key = self._create_cache_key(context)
        
        # Check cache
        if cache_key in self.generation_cache:
            logger.info(f"Cache hit for {cache_key}")
            return self.generation_cache[cache_key]
        
        # Generate code
        code = self._generate_code_internal(context)
        
        # Cache result (with TTL)
        self.generation_cache[cache_key] = code
        
        return code
    
    def _create_cache_key(self, context: GenerationContext) -> str:
        key_data = f"{context.model_id}:{','.join(sorted(context.tool_ids))}:{context.deployment_target}"
        return hashlib.sha256(key_data.encode()).hexdigest()
```

**Cache Strategy**:
- Template cache: In-memory, never expires
- Generation cache: Redis, 1-hour TTL
- Model/tool registry: In-memory, 24-hour TTL

### 2. Parallel Code Generation

**Strategy**: Generate multiple files in parallel

**Implementation**:
```python
async def generate_agent_code_parallel(context: GenerationContext) -> GeneratedCode:
    # Generate files in parallel
    tasks = [
        generate_agent_file(context),
        generate_requirements_file(context),
        generate_dockerfile(context),
        generate_readme_file(context),
        generate_deployment_configs(context),
    ]
    
    results = await asyncio.gather(*tasks)
    
    return GeneratedCode(
        agent_file=results[0],
        requirements_file=results[1],
        dockerfile=results[2],
        readme_file=results[3],
        deployment_scripts=results[4],
    )
```

### 3. Frontend Optimization

**Code Splitting**:
```typescript
// Lazy load code generation components
const ModelSelector = lazy(() => import('./components/ModelSelector'));
const ToolSelector = lazy(() => import('./components/ToolSelector'));
const CodePreviewEnhanced = lazy(() => import('./components/CodePreviewEnhanced'));

// Use Suspense for loading states
<Suspense fallback={<LoadingSkeleton />}>
  <ModelSelector />
</Suspense>
```

**Virtual Scrolling**:
```typescript
// For large model/tool lists
import { FixedSizeList } from 'react-window';

const ModelList = ({ models }) => (
  <FixedSizeList
    height={600}
    itemCount={models.length}
    itemSize={80}
    width="100%"
  >
    {({ index, style }) => (
      <ModelCard model={models[index]} style={style} />
    )}
  </FixedSizeList>
);
```

**Debounced Search**:
```typescript
const useModelSearch = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearch = useMemo(
    () => debounce((term: string) => {
      // Perform search
    }, 300),
    []
  );
  
  return { searchTerm, setSearchTerm: debouncedSearch };
};
```

### 4. Database Optimization

**Indexes**:
```sql
-- Index for fast session lookups
CREATE INDEX idx_generated_code_session ON generated_code(session_id);
CREATE INDEX idx_test_results_session ON test_results(session_id);

-- Index for model/tool lookups
CREATE INDEX idx_model_selections_session ON model_selections(session_id);
CREATE INDEX idx_tool_selections_session ON tool_selections(session_id);

-- Composite index for cost estimates
CREATE INDEX idx_cost_estimates_session_date ON cost_estimates(session_id, estimated_at DESC);
```

**Query Optimization**:
```python
# Use select_related to avoid N+1 queries
def get_session_with_code(session_id: str):
    return Session.objects.select_related(
        'generated_code',
        'model_selections',
        'tool_selections'
    ).get(session_id=session_id)
```


## Deployment Strategy

### Phase 1: Backend Integration (Week 1-2)

**Tasks**:
1. Create code-generation module structure
2. Implement Model Registry with 49+ models
3. Implement Tool Registry with 50+ tools
4. Create Code Generator with base templates
5. Add API endpoints for code generation
6. Implement Context Extractor
7. Add database tables and migrations

**Deliverables**:
- Working code generation API
- Model and tool registries populated
- Basic code templates functional
- API tests passing

### Phase 2: Frontend Integration (Week 2-3)

**Tasks**:
1. Create ModelSelector component
2. Create ToolSelector component
3. Create CodePreviewEnhanced component
4. Create CostEstimator component
5. Integrate components into AgentBuilderPage
6. Add new tabs to workflow UI
7. Implement WebSocket for real-time updates

**Deliverables**:
- Functional UI for model/tool selection
- Code preview with download capability
- Cost estimation dashboard
- E2E workflow working

### Phase 3: Deployment & Testing (Week 3-4)

**Tasks**:
1. Implement AWS Deployment Generator (AgentCore, ECS Fargate, Lambda)
2. Create AWS CloudFormation templates
3. Implement Testing Service with Docker
4. Create TestRunner component
5. Add test history and metrics
6. Implement AWS security scanning
7. Performance optimization

**Deliverables**:
- AWS deployment support (AgentCore, ECS, Lambda)
- Docker-based testing infrastructure
- AWS security scanning integrated
- Performance benchmarks met

### Phase 4: Polish & Documentation (Week 4)

**Tasks**:
1. Comprehensive testing (unit, integration, E2E)
2. Documentation updates
3. User guide creation
4. Video tutorials
5. Bug fixes and refinements
6. Performance tuning
7. Security audit

**Deliverables**:
- Complete test coverage
- User documentation
- Video tutorials
- Production-ready system

### Rollout Strategy

**Beta Testing**:
- Internal testing with 5-10 users
- Collect feedback on UX and generated code quality
- Iterate on templates and UI

**Gradual Rollout**:
- Enable for 25% of users (feature flag)
- Monitor performance and error rates
- Increase to 50%, then 100%

**Monitoring**:
- Track code generation success rate
- Monitor API response times
- Track user satisfaction scores
- Monitor cost estimates accuracy


## Migration and Compatibility

### Backward Compatibility

**Existing Workflows**:
- All existing consultation workflows continue to work unchanged
- Code generation is opt-in (triggered explicitly by user)
- No breaking changes to existing API endpoints
- Frontend remains functional without code generation features

**Feature Flags**:
```python
class FeatureFlags:
    CODE_GENERATION_ENABLED = os.environ.get('FEATURE_CODE_GENERATION', 'true') == 'true'
    TESTING_ENABLED = os.environ.get('FEATURE_TESTING', 'true') == 'true'
    MULTI_CLOUD_ENABLED = os.environ.get('FEATURE_MULTI_CLOUD', 'false') == 'true'

# Use in code
if FeatureFlags.CODE_GENERATION_ENABLED:
    return await generate_code(context)
else:
    return {"message": "Code generation not available"}
```

### Data Migration

**No Migration Required**:
- New tables are additive (no changes to existing schema)
- Existing sessions continue to work
- New fields are optional

**Optional Migration**:
- Backfill model/tool selections from conversation history
- Generate code for completed sessions (on-demand)

### Integration with Existing Components

**Orchestrator Integration**:
```python
# Add new phase to WorkflowPhase enum
class WorkflowPhase(Enum):
    # ... existing phases ...
    CODE_GENERATION = "code_generation"  # NEW

# Extend orchestrator workflow
async def run_workflow(self, context: UserContext):
    # ... existing phases ...
    
    # NEW: Code generation phase
    if self.should_generate_code(workflow_state):
        await self.run_code_generation_phase(workflow_state)
```

**API Integration**:
```python
# Extend existing workflow endpoint
@app.post("/api/workflow/advance")
async def advance_workflow(request: AdvanceWorkflowRequest):
    # ... existing logic ...
    
    # NEW: Trigger code generation if implementation complete
    if workflow_state.current_phase == WorkflowPhase.IMPLEMENTATION:
        if request.trigger_code_generation:
            await trigger_code_generation(workflow_state)
```

**Frontend Integration**:
```typescript
// Add new tabs to AgentBuilderPage
const tabs = [
  { label: 'Chat', component: ChatInterface },
  { label: 'Architecture', component: ArchitectureTab },
  { label: 'Code', component: CodeTab },
  { label: 'Confidence', component: ConfidenceTab },
  // NEW tabs
  { label: 'Model Selection', component: ModelSelector },
  { label: 'Tool Selection', component: ToolSelector },
  { label: 'Generated Code', component: CodePreviewEnhanced },
  { label: 'Testing', component: TestRunner },
];
```

### Dependency Management

**New Python Dependencies**:
```txt
# Code generation
jinja2>=3.1.0
pyyaml>=6.0
docker>=6.1.0

# Security scanning
bandit>=1.7.0
safety>=2.3.0

# Cost calculation
numpy>=1.24.0
```

**New Frontend Dependencies**:
```json
{
  "dependencies": {
    "@uiw/react-codemirror": "^4.21.21",
    "react-window": "^1.8.10",
    "jszip": "^3.10.1",
    "file-saver": "^2.0.5"
  }
}
```

## Success Metrics

### Technical Metrics

**Code Generation**:
- Success rate: > 95%
- Average generation time: < 5 seconds
- Template coverage: 100% of common patterns

**Performance**:
- API response time: < 500ms (p95)
- Frontend load time: < 2 seconds
- Code preview render: < 1 second

**Reliability**:
- Uptime: > 99.9%
- Error rate: < 1%
- Test success rate: > 90%

### User Experience Metrics

**Adoption**:
- % of users who generate code: > 70%
- % of users who download code: > 80%
- % of users who test code: > 50%

**Satisfaction**:
- Code quality rating: > 4.5/5
- Ease of use rating: > 4.5/5
- Time to deployment: < 30 minutes

**Business Metrics**:
- Reduction in manual coding time: > 80%
- Increase in successful deployments: > 50%
- User retention: > 85%

## Conclusion

This design provides a comprehensive integration of code generation capabilities into the agent-builder-platform. The modular architecture ensures backward compatibility while adding powerful new features. The phased rollout strategy minimizes risk while the extensive testing strategy ensures quality. The result is a complete end-to-end platform that guides users from initial requirements through to production-ready, deployable agent code.

