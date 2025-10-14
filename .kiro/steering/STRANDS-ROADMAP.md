# Strands Multi-Agent Roadmap

**Date**: October 14, 2025 (Updated)  
**Status**: 📋 Planning Phase

## Overview

The Agent Builder Platform has **three future enhancement specs** that will be implemented after the current MVP is complete:

1. **Phase 1.5**: Code Generation Integration (independent of Strands)
2. **Phase 1**: Strands Multi-Agent Compatibility
3. **Phase 2**: Strands Advanced Features

**Note**: Phase 1.5 (Code Generation) is **independent** of Strands work and can be implemented in parallel with Phase 1.

## Three-Phase Approach

### Phase 1.5: Code Generation Integration (Independent)
**Spec**: `.kiro/specs/phase-1.5-code-generation-integration/`  
**Status**: 📝 Ready for implementation  
**Effort**: 120-160 hours (3-4 weeks)  
**Dependencies**: Phase 0 (MVP) completion  
**Can Run Parallel With**: Phase 1 (Strands)

**What It Adds**:
- Model Registry (49+ AI models)
- Tool Registry (50+ pre-configured tools)
- Code Generation Engine
- Deployment Generators (AWS, Azure, GCP, AgentCore)
- Cost Estimation Service
- Docker-based Testing Infrastructure
- Frontend Components (ModelSelector, ToolSelector, CodePreview, etc.)

**Key Files to Create**:
- `code-generation/model_registry.py`
- `code-generation/tool_registry.py`
- `code-generation/code_generator.py`
- `code-generation/deployment_generator.py`
- `code-generation/cost_service.py`
- `code-generation/testing_service.py`
- `api/code_generation_service.py`
- Frontend components in `frontend/src/components/`

**Note**: This phase is **independent of Strands work** and transforms the platform from consultation-only to end-to-end code generation.

---

### Phase 1: Basic Strands Compatibility
**Spec**: `.kiro/specs/phase-1-strands-multi-agent-compatibility/`  
**Status**: 📝 Ready for implementation  
**Effort**: 76-98 hours (2-2.5 weeks)

**What It Adds**:
- Agent Communication Protocol
- Shared Memory System
- 4 Strands patterns (Hierarchical, Sequential, Parallel, Conditional)
- Strands metadata for all 5 agents
- Enhanced orchestrator
- Strands spec export

**Key Files to Create**:
- `agent-core/agent_communication.py`
- `agent-core/shared_memory.py`
- `agent-core/strands_agent_base.py`
- `agent-core/strands_multi_agent_coordinator.py`

### Phase 2: Advanced Features
**Spec**: `.kiro/specs/phase-2-strands-advanced-features/`  
**Status**: 📝 Planning (depends on Phase 1)  
**Effort**: 140-190 hours (3.5-4.5 weeks)

**What It Adds**:
- Agent Loop Pattern (Perception → Reasoning → Action → Reflection)
- State Management (session persistence)
- Structured Output (schema validation)
- Conversation Management (multi-turn context)
- 3 advanced patterns (Swarm, Workflow, Graph)
- Hook System (event-driven automation)
- 4 new MCPs (code, database, testing, docs)
- MCP Tool Wrappers

**Key Files to Create**:
- `agent-core/agent_loop.py`
- `agent-core/state_manager.py`
- `agent-core/structured_output.py`
- `agent-core/conversation_manager.py`
- `agent-core/swarm_coordinator.py`
- `agent-core/workflow_engine.py`
- `agent-core/graph_executor.py`
- `agent-core/hook_system.py`
- `mcp-integration/mcp_tool_wrappers.py`

## Timeline

### Current Focus: MVP Completion (Phase 0)
**Priority**: Complete agent-builder-platform MVP first
- Tasks 14.8, 15, 19, 20, 21 (critical path)
- Tasks 22-27 (launch activities)
- **Estimated**: 51-68 hours

### After MVP: Phase 1.5 (Code Generation) - Recommended Next
**Priority**: End-to-end code generation
- 23 implementation tasks (95 sub-tasks)
- **Estimated**: 120-160 hours
- **Can run in parallel with Phase 1**

### After MVP: Phase 1 (Strands Multi-Agent) - Can be Parallel
**Priority**: Basic multi-agent compatibility
- 22 implementation tasks
- **Estimated**: 76-98 hours
- **Can run in parallel with Phase 1.5**

### Future: Phase 2 (Strands Advanced)
**Priority**: Advanced capabilities
- 40 implementation tasks
- **Estimated**: 140-190 hours
- **Requires Phase 1 completion**

## Total Effort

**Phase 0 (MVP)**: 51-68 hours  
**Phase 1.5 (Code Generation)**: 120-160 hours  
**Phase 1 (Strands Multi-Agent)**: 76-98 hours  
**Phase 2 (Strands Advanced)**: 140-190 hours  
**Total All Phases**: 387-516 hours (9-13 weeks sequential, 7.5-10.5 weeks with parallel execution)

## When to Start

### Prerequisites for Phase 1.5 (Code Generation)
- ✅ Phase 0 (MVP) launch complete
- ✅ Implementation Guide agent operational
- ✅ Orchestrator with implementation phase working
- ✅ API endpoints functional
- ✅ Frontend tabbed interface operational

### Prerequisites for Phase 1 (Strands Multi-Agent)
- ✅ Phase 0 (MVP) launch complete
- ✅ All 5 agents operational
- ✅ Orchestrator stable
- ✅ 16 MCPs configured
- ⚠️ **Independent of Phase 1.5** (can run in parallel)

### Prerequisites for Phase 2 (Strands Advanced)
- ✅ Phase 1 complete
- ✅ Agent Communication Protocol working
- ✅ Shared Memory System working
- ✅ Basic Strands patterns tested

## Impact on Current System

### Backward Compatibility
All three future phases maintain **100% backward compatibility**:
- Existing agents continue to work
- Existing orchestrator continues to work
- Existing APIs continue to work
- New features are **opt-in**

### Performance Impact
- Phase 1.5 (Code Generation): < 5% overhead (mostly on-demand)
- Phase 1 (Strands Multi-Agent): < 10% overhead
- Phase 2 (Strands Advanced): < 15% overhead (combined)

## Documentation References

- **Spec Overview**: `.kiro/specs/SPEC-OVERVIEW.md`
- **Phase 0 Spec**: `.kiro/specs/phase-0-agent-builder-platform/`
- **Phase 1.5 Spec**: `.kiro/specs/phase-1.5-code-generation-integration/`
- **Phase 1 Spec**: `.kiro/specs/phase-1-strands-multi-agent-compatibility/`
- **Phase 2 Spec**: `.kiro/specs/phase-2-strands-advanced-features/`

## Current Steering Alignment

The steering documents (product.md, structure.md, tech.md) are **correctly focused on the current implementation** (Phase 0). They do not need updates for future phases until implementation begins.

### When to Update Steering

**Update steering when Phase 1.5 starts**:
- Add code generation to product.md
- Add new directories to structure.md
- Add new dependencies to tech.md

**Update steering when Phase 1 starts**:
- Add Strands patterns to product.md
- Add agent-core components to structure.md
- No new tech needed (same stack)

**Update steering when Phase 2 starts**:
- Add advanced features to product.md
- Add new components to structure.md
- Add 4 new MCPs to MCP-INVENTORY.md

**Don't update steering for**:
- Planning documents
- Future specs
- Unimplemented features

## Recommendation

✅ **Current steering is correct** - No updates needed now  
📋 **This roadmap document** - Provides context for all future work  
🚀 **Focus on Phase 0 (MVP)** - Complete current platform first  
⏭️ **Then Phase 1.5 (Code Generation)** - Recommended next priority  
⏭️ **Or Phase 1 (Strands)** - Can run parallel with Phase 1.5  
⏭️ **Finally Phase 2 (Advanced)** - After Phase 1 complete

## Implementation Strategy

### Sequential Approach
1. Phase 0 (MVP) - 51-68 hours
2. Phase 1.5 (Code Generation) - 120-160 hours
3. Phase 1 (Strands Multi-Agent) - 76-98 hours
4. Phase 2 (Strands Advanced) - 140-190 hours
**Total**: 387-516 hours (9-13 weeks)

### Parallel Approach (Recommended)
1. Phase 0 (MVP) - 51-68 hours (1-2 weeks)
2. **Phase 1.5 + Phase 1 in parallel** - 120-160 hours (3-4 weeks)
3. Phase 2 (Strands Advanced) - 140-190 hours (3.5-4.5 weeks)
**Total**: 7.5-10.5 weeks (saves 1.5-2.5 weeks)

---

**Status**: ✅ Steering in sync with current implementation  
**Next Action**: Complete Phase 0 (MVP), then start Phase 1.5 or Phase 1  
**Timeline**: Phase 0 → Phase 1.5 + Phase 1 (parallel) → Phase 2

**Last Updated**: October 14, 2025 (Added Phase 1.5 Code Generation Integration)
