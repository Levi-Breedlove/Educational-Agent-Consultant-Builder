#!/usr/bin/env python3
"""
OpenAPI Documentation Enhancements
Adds comprehensive examples, descriptions, and metadata to the API documentation
"""

from typing import Dict, Any

# Enhanced API metadata
API_METADATA = {
    "title": "Agent Builder Platform API",
    "description": """
# Agent Builder Platform API

Expert AI consultation system for building production-ready agents in 30-45 minutes.

## Overview

The Agent Builder Platform provides a comprehensive API for creating custom AI agents through 
an expert-guided workflow. The platform leverages 16 specialized MCPs (Model Context Protocol tools), 
vector search with Amazon Bedrock Titan embeddings, and hierarchical multi-agent orchestration.

## Key Features

- **Expert AI Consultants**: AWS Solutions Architect, Senior Developer, DevOps Expert personas
- **95%+ Confidence System**: Multi-factor confidence scoring across all recommendations
- **Vector Search Intelligence**: Semantic understanding using 1536-dimension embeddings
- **Production-Ready Output**: Complete agents with AWS backend, monitoring, and security
- **Cost-Optimized**: Designed for hackathon budgets ($16-30 total)

## Workflow Phases

1. **Requirements** (8-12 min): Natural language use case description with AI-guided clarification
2. **Architecture** (10-15 min): AI-generated architecture with cost and security analysis
3. **Implementation** (10-15 min): Automated code generation with Strands builder integration
4. **Testing** (5-8 min): Comprehensive validation with security and performance checks
5. **Deployment** (3-5 min): Export and deployment with complete documentation

## Authentication

Currently, the API uses session-based authentication. JWT token authentication is available 
for production deployments.

## Rate Limiting

- Default: 100 requests per minute per session
- Burst: 200 requests per minute
- Contact support for higher limits

## Performance Targets

- Health check: < 100ms
- Session operations: < 500ms
- Agent creation: < 5 seconds
- Complete workflow: 30-45 minutes

## Support

- Documentation: https://github.com/agent-builder-platform/docs
- Issues: https://github.com/agent-builder-platform/issues
- Email: support@agent-builder-platform.com
    """,
    "version": "1.0.0",
    "contact": {
        "name": "Agent Builder Platform Team",
        "email": "support@agent-builder-platform.com",
        "url": "https://agent-builder-platform.com"
    },
    "license": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    "servers": [
        {
            "url": "http://localhost:8000",
            "description": "Local development server"
        },
        {
            "url": "https://api.agent-builder-platform.com",
            "description": "Production server"
        },
        {
            "url": "https://staging-api.agent-builder-platform.com",
            "description": "Staging server"
        }
    ]
}

# Enhanced endpoint examples
ENDPOINT_EXAMPLES = {
    "create_session": {
        "summary": "Create a new agent creation session",
        "description": """
Create a new session to begin the agent creation workflow. Sessions track user progress 
through the five workflow phases and maintain state across API calls.

**Use Cases:**
- Starting a new agent creation project
- Resuming work on an existing project
- Managing multiple concurrent projects

**Best Practices:**
- Store the session_id securely for subsequent API calls
- Set experience_level appropriately for tailored guidance
- Sessions auto-expire after 24 hours of inactivity
        """,
        "examples": {
            "beginner": {
                "summary": "Beginner user starting first project",
                "value": {
                    "user_id": "user-123",
                    "experience_level": "beginner"
                }
            },
            "expert": {
                "summary": "Expert user with specific requirements",
                "value": {
                    "user_id": "expert-user-456",
                    "experience_level": "expert"
                }
            },
            "anonymous": {
                "summary": "Anonymous user (no user_id)",
                "value": {
                    "experience_level": "intermediate"
                }
            }
        }
    },
    "create_agent": {
        "summary": "Start agent creation workflow",
        "description": """
Initialize the agent creation workflow with your use case description. The system will 
analyze your requirements and begin the expert consultation process.

**What Happens:**
1. Use case analysis by AWS Solutions Architect agent
2. Service recommendations with cost estimates
3. Security analysis and best practices
4. Clarifying questions for requirements refinement

**Response Time:** Typically 3-5 seconds

**Tips:**
- Provide detailed descriptions for better recommendations
- Include budget and timeline constraints in the description
- Mention specific AWS services if you have preferences
        """,
        "examples": {
            "chatbot": {
                "summary": "Customer support chatbot",
                "value": {
                    "session_id": "session-abc-123",
                    "use_case": "customer_support_chatbot",
                    "description": "Build an AI-powered chatbot that answers customer questions about our products, handles common support requests, and escalates complex issues to human agents. Should integrate with our existing CRM system.",
                    "experience_level": "beginner"
                }
            },
            "data_pipeline": {
                "summary": "Data processing pipeline",
                "value": {
                    "session_id": "session-def-456",
                    "use_case": "data_processing_pipeline",
                    "description": "Create an automated pipeline that ingests CSV files from S3, validates data quality, transforms records, and loads into PostgreSQL. Need to process 10GB daily with error handling and monitoring.",
                    "experience_level": "intermediate"
                }
            },
            "api_gateway": {
                "summary": "Secure API gateway",
                "value": {
                    "session_id": "session-ghi-789",
                    "use_case": "api_gateway",
                    "description": "Build a production-grade API gateway with JWT authentication, rate limiting (1000 req/s), request validation, and comprehensive logging. Must be PCI-DSS compliant.",
                    "experience_level": "expert"
                }
            }
        }
    },
    "submit_requirements": {
        "summary": "Submit requirements for analysis",
        "description": """
Provide additional requirements and context for the AI Solutions Architect to analyze. 
This endpoint triggers deep analysis including cost estimation, security validation, 
and service recommendations.

**Analysis Includes:**
- Use case pattern matching
- AWS service recommendations with rationale
- Cost analysis with monthly estimates
- Security best practices
- Clarifying questions for refinement

**Confidence Scoring:**
- Vector similarity: Semantic match to known patterns
- Source reliability: MCP validation across 16 sources
- Freshness: Knowledge base update recency
- Multi-MCP validation: Cross-source verification

**Target:** 95%+ confidence score
        """,
        "examples": {
            "detailed_requirements": {
                "summary": "Detailed requirements with context",
                "value": {
                    "session_id": "session-abc-123",
                    "user_input": "I need the chatbot to handle 500 concurrent users, respond within 2 seconds, and support English and Spanish. Budget is $50/month.",
                    "context": {
                        "budget_range": "low",
                        "timeline": "2_weeks",
                        "compliance": ["GDPR"],
                        "existing_infrastructure": ["AWS", "PostgreSQL"]
                    }
                }
            }
        }
    },
    "execute_tests": {
        "summary": "Execute comprehensive tests",
        "description": """
Run comprehensive validation tests on the generated agent implementation. Tests include 
security scanning, performance benchmarking, cost validation, and integration testing.

**Test Types:**
- **security**: Vulnerability scanning, IAM policy validation, encryption checks
- **performance**: Load testing, latency benchmarks, throughput validation
- **cost**: Cost estimate validation, optimization recommendations
- **integration**: AWS service integration tests, error handling validation
- **load**: Scalability testing, concurrent user simulation

**Production Readiness Score:**
- 0.90-1.00: Production ready
- 0.75-0.89: Minor improvements needed
- 0.60-0.74: Significant improvements needed
- < 0.60: Not production ready

**Typical Duration:** 30-60 seconds
        """,
        "examples": {
            "all_tests": {
                "summary": "Run all test types",
                "value": {
                    "session_id": "session-abc-123",
                    "test_types": None
                }
            },
            "security_only": {
                "summary": "Security tests only",
                "value": {
                    "session_id": "session-abc-123",
                    "test_types": ["security"]
                }
            },
            "performance_and_cost": {
                "summary": "Performance and cost tests",
                "value": {
                    "session_id": "session-abc-123",
                    "test_types": ["performance", "cost"]
                }
            }
        }
    }
}

# Response examples
RESPONSE_EXAMPLES = {
    "session_created": {
        "summary": "Session created successfully",
        "value": {
            "session_id": "session-abc123def456",
            "status": "active",
            "current_phase": "requirements",
            "created_at": "2025-10-06T10:00:00Z",
            "updated_at": "2025-10-06T10:00:00Z",
            "experience_level": "intermediate"
        }
    },
    "agent_created": {
        "summary": "Agent workflow created",
        "value": {
            "agent_id": "agent-xyz789abc123",
            "session_id": "session-abc123def456",
            "status": "requirements",
            "progress_percentage": 0.0,
            "created_at": "2025-10-06T10:05:00Z",
            "use_case": "customer_support_chatbot",
            "description": "Build an AI-powered chatbot...",
            "experience_level": "intermediate",
            "vector_search_enabled": True
        }
    },
    "requirements_analysis": {
        "summary": "Requirements analysis complete",
        "value": {
            "session_id": "session-abc123def456",
            "use_case_analysis": {
                "primary_use_case": "chatbot",
                "complexity": "medium",
                "estimated_duration": "35_minutes"
            },
            "service_recommendations": [
                {
                    "service_name": "AWS Lambda",
                    "reasoning": "Serverless compute for chatbot logic with automatic scaling",
                    "estimated_cost": "$5-10/month",
                    "confidence": 0.97
                },
                {
                    "service_name": "Amazon Lex",
                    "reasoning": "Pre-built conversational AI with NLU capabilities",
                    "estimated_cost": "$15-20/month",
                    "confidence": 0.95
                }
            ],
            "cost_analysis": {
                "estimated_monthly_cost": "$25-35",
                "breakdown": {
                    "compute": "$5-10",
                    "ai_services": "$15-20",
                    "storage": "$2-3",
                    "data_transfer": "$3-5"
                },
                "optimization_opportunities": [
                    "Use Lambda free tier (1M requests/month)",
                    "Enable S3 Intelligent-Tiering for logs"
                ]
            },
            "security_analysis": {
                "recommendations": [
                    "Enable encryption at rest for DynamoDB",
                    "Use IAM roles instead of access keys",
                    "Implement API Gateway throttling"
                ],
                "compliance_considerations": ["GDPR", "SOC2"]
            },
            "clarifying_questions": [
                "What is the expected number of concurrent users?",
                "Do you need multi-language support?",
                "Should the chatbot integrate with existing systems?"
            ],
            "confidence_score": 0.97,
            "next_steps": [
                "Answer clarifying questions",
                "Review service recommendations",
                "Proceed to architecture design"
            ]
        }
    },
    "test_results": {
        "summary": "Test execution results",
        "value": {
            "agent_id": "agent-xyz789abc123",
            "test_execution_id": "test-exec-123456",
            "timestamp": "2025-10-06T10:30:00Z",
            "overall_status": "passed",
            "tests_executed": {
                "security": 8,
                "performance": 5,
                "cost": 3,
                "integration": 6,
                "load": 4
            },
            "summary": {
                "total_tests": 26,
                "passed": 24,
                "failed": 1,
                "warnings": 1
            },
            "production_readiness_score": 0.92,
            "confidence_score": 0.97,
            "recommendations": [
                "Enable CloudWatch alarms for Lambda errors",
                "Add DynamoDB auto-scaling policies",
                "Implement request validation middleware"
            ]
        }
    }
}

# Error response examples
ERROR_EXAMPLES = {
    "not_found": {
        "summary": "Resource not found",
        "value": {
            "error": "Not Found",
            "detail": "Session not found: session-invalid-id",
            "timestamp": "2025-10-06T10:00:00Z"
        }
    },
    "validation_error": {
        "summary": "Validation error",
        "value": {
            "error": "Validation Error",
            "detail": "use_case must be at least 3 characters",
            "timestamp": "2025-10-06T10:00:00Z"
        }
    },
    "internal_error": {
        "summary": "Internal server error",
        "value": {
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again.",
            "timestamp": "2025-10-06T10:00:00Z"
        }
    }
}

def get_enhanced_openapi_schema() -> Dict[str, Any]:
    """Get enhanced OpenAPI schema with comprehensive documentation"""
    return {
        "openapi": "3.0.0",
        "info": API_METADATA,
        "tags": [
            {
                "name": "Health",
                "description": "Health check and system status endpoints"
            },
            {
                "name": "Sessions",
                "description": "Session management for agent creation workflows"
            },
            {
                "name": "Agent Workflow",
                "description": "Agent creation workflow endpoints"
            },
            {
                "name": "Testing & Validation",
                "description": "Testing and validation endpoints"
            },
            {
                "name": "Export & Deployment",
                "description": "Export and deployment endpoints"
            },
            {
                "name": "Performance",
                "description": "Performance monitoring and metrics"
            }
        ]
    }
