# Strands Multi-Agent Roadmap

**Date**: October 10, 2025  
**Status**: 📋 Planning Phase

## Overview

The Agent Builder Platform has two new specs for comprehensive Strands multi-agent compatibility. These are **future enhancements** that will be implemented after the current MVP is complete.

## Two-Phase Approach

### Phase 1: Basic Strands Compatibility
**Spec**: `.kiro/specs/strands-multi-agent-compatibility/`  
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
**Spec**: `.kiro/specs/strands-advanced-features/`  
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

### Current Focus: MVP Completion
**Priority**: Complete agent-builder-platform MVP first
- Tasks 15, 18, 19, 20, 21 (critical path)
- Tasks 22-26 (launch activities)
- **Estimated**: 45-55 hours

### After MVP: Strands Phase 1
**Priority**: Basic multi-agent compatibility
- 22 implementation tasks
- **Estimated**: 76-98 hours

### Future: Strands Phase 2
**Priority**: Advanced capabilities
- 40 implementation tasks
- **Estimated**: 140-190 hours

## Total Strands Effort

**Combined**: 216-288 hours (5-7 weeks for 1 developer)

## When to Start

### Prerequisites for Phase 1
- ✅ MVP launch complete
- ✅ All 5 agents operational
- ✅ Orchestrator stable
- ✅ 16 MCPs configured

### Prerequisites for Phase 2
- ✅ Phase 1 complete
- ✅ Agent Communication Protocol working
- ✅ Shared Memory System working
- ✅ Basic Strands patterns tested

## Impact on Current System

### Backward Compatibility
Both specs maintain **100% backward compatibility**:
- Existing agents continue to work
- Existing orchestrator continues to work
- Existing APIs continue to work
- New features are **opt-in**

### Performance Impact
- Phase 1: < 10% overhead
- Phase 2: < 15% overhead (combined)

## Documentation References

- **Spec Overview**: `.kiro/specs/SPEC-OVERVIEW.md`
- **Phase 1 Spec**: `.kiro/specs/strands-multi-agent-compatibility/`
- **Phase 2 Spec**: `.kiro/specs/strands-advanced-features/`

## Current Steering Alignment

The steering documents (product.md, structure.md, tech.md) are **correctly focused on the current implementation**. They do not need updates for these future specs until implementation begins.

### When to Update Steering

**Update steering when**:
- Phase 1 implementation starts
- New components are added to agent-core/
- New patterns are implemented
- New MCPs are integrated

**Don't update steering for**:
- Planning documents
- Future specs
- Unimplemented features

## Recommendation

✅ **Current steering is correct** - No updates needed now  
📋 **This roadmap document** - Provides context for future work  
🚀 **Focus on MVP** - Complete current platform first  
⏭️ **Then Strands Phase 1** - After MVP launch

---

**Status**: ✅ Steering in sync with current implementation  
**Next Action**: Complete MVP, then start Strands Phase 1  
**Timeline**: MVP → Phase 1 → Phase 2
