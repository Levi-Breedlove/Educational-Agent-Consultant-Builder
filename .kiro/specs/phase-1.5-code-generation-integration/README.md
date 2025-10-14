# Phase 1.5: Code Generation Integration Spec

## Overview

This spec defines the integration of the agent_builder_application's code generation capabilities into the agent-builder-platform, transforming it from a consultation-only system into a complete end-to-end agent creation platform.

**Phase**: 1.5 (After MVP, Before/Parallel to Strands Multi-Agent)  
**Dependencies**: Phase 0 (agent-builder-platform MVP) must be complete  
**Can Run Parallel With**: Phase 1 (strands-multi-agent-compatibility)

## Status

✅ **Requirements**: Complete and approved  
✅ **Design**: Complete and approved  
✅ **Tasks**: Complete and approved  
✅ **AWS Alignment**: 100% verified (see AWS-ALIGNMENT-VERIFIED.md)  
🚀 **Ready for Implementation**

## Quick Links

### Core Spec Documents
- **[Requirements Document](./requirements.md)** - 12 core requirements with user stories and acceptance criteria
- **[Design Document](./design.md)** - Comprehensive architecture and component design
- **[Tasks Document](./tasks.md)** - 23 main tasks with 95 sub-tasks (START HERE for implementation)

### AWS Alignment
- **[AWS-ALIGNMENT.md](./AWS-ALIGNMENT.md)** - Complete AWS-first verification (100/100 score)

## Key Features

### What's Being Added

1. **Model Registry** - 49+ AI models (AWS Bedrock prioritized, Ollama for local dev) with capabilities, costs, and recommendations
2. **Tool Registry** - 50+ pre-configured tools (RAG, Memory, Code Execution, Web, File System) with dependencies
3. **Code Generation Engine** - Production-ready agent code with AWS observability (CloudWatch, X-Ray) and security best practices
4. **AWS-First Deployment Generators** - Primary: AWS (AgentCore, ECS Fargate, Lambda, CloudFormation); Secondary: Azure, GCP (optional)
5. **AWS Cost Estimation** - Real-time AWS cost calculations with free tier optimization
6. **Testing Infrastructure** - Docker-based testing with live input/output streaming
7. **Frontend Components** - ModelSelector, ToolSelector, CodePreview, CostEstimator, TestRunner
8. **Context Extraction** - Automatic extraction of requirements from consultation conversations
9. **AWS Architecture Integration** - Generated code aligns with AWS architecture diagrams from consultation

### Integration Points

- **Orchestrator**: New CODE_GENERATION phase after IMPLEMENTATION
- **API Layer**: 9 new endpoints for models, tools, code generation, testing, and cost estimation
- **Frontend**: 5 new tabs in AgentBuilderPage
- **Database**: 5 new tables for generated code, selections, tests, and cost estimates

## Implementation Timeline

### Phase 1: Backend Integration (Week 1-2)
- Model and Tool Registries
- Code Generation Engine
- Context Extraction
- API endpoints
- Database schema

**Deliverables**: Working code generation API

### Phase 2: Frontend Integration (Week 2-3)
- ModelSelector, ToolSelector components
- CodePreviewEnhanced component
- CostEstimator, TestRunner components
- AgentBuilderPage integration

**Deliverables**: Functional UI for complete workflow

### Phase 3: Deployment & Testing (Week 3-4)
- AWS deployment generators (AgentCore, ECS Fargate, Lambda, CloudFormation) - Primary
- Optional multi-cloud generators (Azure/GCP) - Secondary
- Testing infrastructure
- AWS security and observability integration
- Documentation

**Deliverables**: Production-ready AWS-focused system

### Phase 4: Polish (Week 4)
- Comprehensive testing
- Documentation
- Bug fixes
- Performance tuning

**Deliverables**: Launch-ready platform

## Estimated Effort

- **Total**: 120-160 hours (3-4 weeks for 1 developer)
- **Backend**: 50-65 hours
- **Frontend**: 40-50 hours
- **Polish**: 30-45 hours

## Success Metrics

### Technical
- Code generation success rate: > 95%
- API response time: < 500ms (p95)
- Frontend load time: < 2 seconds

### User Experience
- % users who generate code: > 70%
- Code quality rating: > 4.5/5
- Time to deployment: < 30 minutes

## Getting Started

To begin implementation:

1. **Review the requirements** - Understand the 12 core requirements
2. **Study the design** - Familiarize yourself with the architecture
3. **Start with Task 1** - Set up the code generation module structure
4. **Follow the task order** - Each task builds on previous tasks

## Repository Context

**Source Repository**: https://github.com/MikePfunk28/agent_builder_application.git  
**Integration Target**: agent-builder-platform  
**Integration Strategy**: Modular adapter pattern (non-breaking)

## Important Notes

### AWS-First Approach
- ✅ **100% AWS-focused** - All deployment options are AWS-only (AgentCore, ECS Fargate, Lambda)
- ✅ **AWS Bedrock prioritized** - Primary model provider with 49+ models
- ✅ **AWS services integrated** - CloudWatch, X-Ray, Secrets Manager, IAM, CloudFormation
- ✅ **Verified alignment** - See [AWS-ALIGNMENT.md](./AWS-ALIGNMENT.md) for complete verification

### Implementation
- All existing functionality remains unchanged (non-breaking integration)
- Code generation is opt-in (triggered after consultation completes)
- Feature flags enable gradual rollout
- Backward compatible with existing sessions
- Unit tests marked as optional (*) to prioritize MVP delivery

## Questions?

Refer to the detailed documents:
- Requirements for "what" and "why"
- Design for "how"
- Tasks for "when" and "what order"

---

**Created**: 2025-10-14  
**Status**: Ready for Implementation  
**Next Step**: Open tasks.md and click "Start task" on Task 1
