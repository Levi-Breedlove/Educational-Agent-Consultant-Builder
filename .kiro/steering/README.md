# Steering Documents

**Purpose**: Guide AI assistance and development by documenting current implementation

---

## Quick Start

### 📊 Alignment Status
See **[ALIGNMENT-STATUS.md](./ALIGNMENT-STATUS.md)** for:
- Current alignment verification (100/100 score)
- Update strategy for future phases
- When to update each steering document

### 🗺️ Future Roadmap
See **[STRANDS-ROADMAP.md](./STRANDS-ROADMAP.md)** for:
- Overview of all future phases (1, 1.5, 2)
- Timeline and dependencies
- Implementation strategy

---

## Core Steering Documents

### product.md
**Purpose**: Product overview and value proposition  
**Focus**: Current Phase 0 (MVP) implementation  
**Content**:
- Core value proposition
- Key features (5 AI agents, 16 MCPs, vector search)
- Target users
- Success metrics

**Update When**: Phase 1.5 or Phase 1 implementation starts

---

### structure.md
**Purpose**: Project structure and organization  
**Focus**: Current Phase 0 file structure  
**Content**:
- Directory layout (`/agent-core/`, `/agents/`, `/api/`, `/frontend/`, etc.)
- Key files in each directory
- Code organization patterns
- Naming conventions

**Update When**: New files or directories are created in future phases

---

### tech.md
**Purpose**: Technology stack and commands  
**Focus**: Current Phase 0 technologies  
**Content**:
- Languages & frameworks (Python, TypeScript, React, FastAPI)
- AWS services (Bedrock, ECS, DynamoDB, S3, etc.)
- Frontend technologies (Material-UI, Redux, CodeMirror)
- Backend technologies (Uvicorn, WebSocket, JWT)
- Common commands (setup, testing, deployment)

**Update When**: New dependencies or technologies are added in future phases

---

### MCP-INVENTORY.md
**Purpose**: Complete MCP inventory  
**Focus**: Current 16 configured MCPs  
**Content**:
- AWS MCPs (12 total): Documentation, Well-Architected, Solutions, Pricing, Security, Serverless, Containers, AI/ML, DevOps, Monitoring, Networking, Agent Core Patterns
- Non-AWS MCPs (4 total): Strands, GitHub, Filesystem, Perplexity
- MCP categories and sync strategies
- Health monitoring and cost optimization

**Update When**: Phase 2 adds 4 new MCPs (code, database, testing, docs)

---

## Roadmap Documents

### STRANDS-ROADMAP.md
**Purpose**: Future phases roadmap  
**Focus**: Phases 1, 1.5, and 2  
**Content**:
- Three-phase approach overview
- Phase 1.5: Code Generation Integration (120-160 hours)
- Phase 1: Strands Multi-Agent Compatibility (76-98 hours)
- Phase 2: Strands Advanced Features (140-190 hours)
- Timeline and prerequisites
- Implementation strategy (sequential vs parallel)

**Update When**: New phases are added or timelines change

---

### ALIGNMENT-STATUS.md
**Purpose**: Steering alignment verification  
**Focus**: Current alignment status  
**Content**:
- Alignment verification for all steering documents
- Update strategy for each phase
- Key principles (what to include/exclude)
- Verification checklist

**Update When**: Alignment needs to be re-verified

---

## File Structure

```
.kiro/steering/
├── README.md                    # This file - quick start guide
├── ALIGNMENT-STATUS.md          # Steering alignment verification
├── STRANDS-ROADMAP.md           # Future phases roadmap
│
├── product.md                   # Product overview (Phase 0 focus)
├── structure.md                 # Project structure (Phase 0 focus)
├── tech.md                      # Technology stack (Phase 0 focus)
└── MCP-INVENTORY.md             # MCP inventory (16 MCPs)
```

---

## Key Principles

### What Steering Documents Should Contain
✅ **Current implementation only** - Document what exists now  
✅ **Accurate file structure** - Only existing files and directories  
✅ **Current technologies** - Only dependencies in use  
✅ **Configured MCPs** - Only MCPs that are set up

### What Steering Documents Should NOT Contain
❌ **Future features** - Don't document unimplemented features  
❌ **Planned files** - Don't reference non-existent files  
❌ **Future dependencies** - Don't list packages not yet added  
❌ **Unconfigured MCPs** - Don't list MCPs not yet set up

### Where Future Plans Belong
✅ **Spec documents** (`.kiro/specs/`) - Requirements, design, tasks for future phases  
✅ **Roadmap documents** (`.kiro/steering/*-ROADMAP.md`) - Timeline and context for future work

---

## Update Strategy

### Phase 0 (MVP) - Current
✅ **All steering documents current** - No updates needed  
✅ **Focus on implementation** - Complete Task 14.8 and remaining MVP tasks

### Phase 1.5 (Code Generation) - After MVP
📝 **Update product.md** - Add code generation features  
📝 **Update structure.md** - Add `/code-generation/` directory and new components  
📝 **Update tech.md** - Add new dependencies (jinja2, docker, jszip, file-saver)  
✅ **Keep MCP-INVENTORY.md** - No new MCPs

### Phase 1 (Strands Multi-Agent) - After MVP
📝 **Update product.md** - Add Strands patterns  
📝 **Update structure.md** - Add agent-core components  
✅ **Keep tech.md** - Same stack  
✅ **Keep MCP-INVENTORY.md** - No new MCPs

### Phase 2 (Strands Advanced) - After Phase 1
📝 **Update product.md** - Add advanced features  
📝 **Update structure.md** - Add new components  
✅ **Keep tech.md** - Minimal changes  
📝 **Update MCP-INVENTORY.md** - Add 4 new MCPs

---

## Current Status

| Document | Status | Last Updated | Next Update |
|----------|--------|--------------|-------------|
| product.md | ✅ Current | Phase 0 | Phase 1.5 or 1 start |
| structure.md | ✅ Current | Phase 0 | Phase 1.5 or 1 start |
| tech.md | ✅ Current | Phase 0 | Phase 1.5 or 1 start |
| MCP-INVENTORY.md | ✅ Current | Phase 0 | Phase 2 start |
| STRANDS-ROADMAP.md | ✅ Current | Oct 14, 2025 | When phases change |
| ALIGNMENT-STATUS.md | ✅ Current | Oct 14, 2025 | When alignment changes |

**Overall Alignment**: 100/100 ⭐⭐⭐⭐⭐

---

## Questions?

- **Alignment Status**: See [ALIGNMENT-STATUS.md](./ALIGNMENT-STATUS.md)
- **Future Roadmap**: See [STRANDS-ROADMAP.md](./STRANDS-ROADMAP.md)
- **Product Overview**: See [product.md](./product.md)
- **Project Structure**: See [structure.md](./structure.md)
- **Technology Stack**: See [tech.md](./tech.md)
- **MCP Inventory**: See [MCP-INVENTORY.md](./MCP-INVENTORY.md)

---

**Last Updated**: October 14, 2025  
**Status**: ✅ ALL STEERING DOCUMENTS ALIGNED  
**Next Action**: Continue Phase 0 (MVP) implementation
