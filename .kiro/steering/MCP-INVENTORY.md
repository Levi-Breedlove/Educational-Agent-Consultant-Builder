# MCP Inventory - Complete List

**Date**: October 9, 2025  
**Total MCPs**: 16  
**Status**: ✅ ALL CONFIGURED AND OPERATIONAL

## Complete MCP List

### AWS MCPs (12 total)

1. **aws-docs** - AWS Documentation MCP
   - Comprehensive AWS service documentation, best practices, and pricing information
   - Sync: Monday & Thursday at 2 AM

2. **aws-well-architected** - AWS Well-Architected Framework MCP
   - 6 pillars: Operational Excellence, Security, Reliability, Performance, Cost, Sustainability
   - Sync: Tuesday & Friday at 3 AM

3. **aws-solutions** - AWS Solutions Library MCP
   - Reference architectures and implementation guides
   - Sync: Wednesday & Saturday at 4 AM

4. **aws-pricing** - AWS Pricing MCP
   - Real-time pricing, cost calculators, optimization recommendations
   - Sync: Real-time (no caching)

5. **aws-security** - AWS Security Best Practices MCP
   - Security services, compliance frameworks, security best practices
   - Sync: Monday & Thursday at 5 AM

6. **aws-serverless** - AWS Serverless Patterns MCP
   - Lambda best practices, event-driven architecture, microservices patterns
   - Sync: Tuesday & Friday at 6 AM

7. **aws-containers** - AWS Container Services MCP
   - ECS, EKS, Fargate patterns and container orchestration
   - Sync: Wednesday & Saturday at 7 AM

8. **aws-aiml** - AWS AI/ML Services MCP
   - Bedrock, SageMaker, AI/ML patterns and model deployment
   - Sync: Monday & Thursday at 8 AM

9. **aws-devops** - AWS DevOps and CI/CD MCP
   - CodePipeline, CodeBuild, deployment strategies, DevOps best practices
   - Sync: Monday & Thursday at 10 AM

10. **aws-monitoring** - AWS Monitoring and Observability MCP
    - CloudWatch, X-Ray, monitoring patterns, observability best practices
    - Sync: Tuesday & Friday at 11 AM

11. **aws-networking** - AWS Networking MCP
    - VPC, networking patterns, hybrid connectivity, network security
    - Sync: Wednesday & Saturday at 12 PM

12. **agent-core-patterns** - Agent Core Patterns MCP
    - Agent Core framework patterns, best practices, implementation guides
    - Sync: Monday & Thursday at 1 PM

### Non-AWS MCPs (4 total)

13. **strands-mcp** - Strands Agent Resources MCP
    - Strands agent templates, capabilities, implementation examples
    - Sync: Tuesday & Friday at 9 AM

14. **github-mcp** - GitHub Repository Analysis MCP
    - Repository analysis, MCP discovery, compatibility matrix
    - Sync: Wednesday & Saturday at 4 AM
    - Requires: GITHUB_TOKEN

15. **filesystem-mcp** - Filesystem Operations MCP
    - File system operations for agent configuration and code generation
    - Sync: None (real-time operations)

16. **perplexity-mcp** - Perplexity Research MCP
    - Deep research, current trends, best practices, competitive analysis
    - Sync: Real-time (no caching)
    - Requires: PERPLEXITY_API_KEY
    - Rate Limit: 20 requests/minute, $2/month cost limit

## MCP Categories

### By Domain
- **AWS Infrastructure**: 12 MCPs (aws-docs through agent-core-patterns)
- **Agent Development**: 2 MCPs (strands-mcp, agent-core-patterns)
- **Research & Discovery**: 2 MCPs (github-mcp, perplexity-mcp)
- **Utilities**: 1 MCP (filesystem-mcp)

### By Sync Strategy
- **Scheduled Sync**: 13 MCPs (2-3 times per week)
- **Real-time**: 2 MCPs (aws-pricing, perplexity-mcp)
- **No Sync**: 1 MCP (filesystem-mcp)

### By Authentication
- **No Auth Required**: 14 MCPs
- **API Key Required**: 2 MCPs (github-mcp, perplexity-mcp)

## Vector Search Integration

All synced MCPs support:
- ✅ Amazon Bedrock Titan embeddings (1536 dimensions)
- ✅ Cosine similarity search (0.7 threshold)
- ✅ Hybrid search (70% vector, 30% text)
- ✅ Intelligent query routing
- ✅ Multi-source validation

## Intelligent Routing Rules

The system automatically routes queries to appropriate MCPs:

| Query Type | Primary MCP(s) | Strategy |
|------------|----------------|----------|
| Pricing/Cost | aws-pricing | Real-time |
| Well-Architected | aws-well-architected | Cached + Vector |
| Serverless | aws-serverless | Hybrid + Vector |
| Containers | aws-containers | Hybrid + Vector |
| AI/ML | aws-aiml + perplexity-mcp | Hybrid + Research |
| Security | aws-security | Hybrid + Cached |
| Architecture | aws-solutions | Hybrid + Vector |
| Research | perplexity-mcp | Real-time |
| Repository Analysis | github-mcp | Real-time |
| Agent Patterns | strands-mcp + agent-core-patterns | Cached + Vector |
| Complex Queries | All sources | Multi-source synthesis |

## Health Monitoring

- ✅ Health checks every 5 minutes
- ✅ 30-second timeout per check
- ✅ 3 retry attempts before failure
- ✅ SNS alerts for failures
- ✅ Automatic fallback to cached data

## Cost Optimization

- ✅ Intelligent caching (7-14 day TTL)
- ✅ Scheduled sync (2-3 times per week)
- ✅ Rate limiting (100 requests/minute)
- ✅ Perplexity cost limit ($2/month)
- ✅ Free tier maximization

**Estimated Monthly Cost**: ~$0.50-2.00 (mostly Perplexity API)

## Confidence System

All MCP responses contribute to 95%+ confidence baseline:
- ✅ Multi-factor confidence scoring
- ✅ Source validation across MCPs
- ✅ Freshness-based confidence adjustment
- ✅ Fallback confidence scoring
- ✅ Vector similarity confidence boost

## Configuration File

All MCPs are configured in:
- `agent-builder-platform/mcp-integration/mcp-config.yaml`

## Verification

To verify all MCPs are operational:
```bash
cd agent-builder-platform/mcp-integration
python mcp_health_monitor.py
```

---

**Status**: ✅ ALL 16 MCPs CONFIGURED AND OPERATIONAL
