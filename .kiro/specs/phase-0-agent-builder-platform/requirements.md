# Requirements Document

## Introduction

The Agent Builder Platform is an educational consultation system that teaches users how to build production-ready Strands agents on AWS infrastructure. The platform leverages 16 specialized MCPs (Model Context Protocol tools) for AWS documentation, Strands patterns, GitHub analysis, and research, along with the Strands agent builder framework, to guide users through learning to create custom agents. The platform acts as a meta-agent teaching system where 5 specialized AI consultants collaborate to educate users on designing, configuring, and deploying Strands agents on AWS tailored to their unique requirements.

**Educational Focus**: This platform teaches users HOW to build Strands agents on AWS, not just builds them. Users learn AWS architecture, Strands framework, and best practices through guided consultation.

## Requirements

### Requirement 1

**User Story:** As a new user, I want to describe my use case in natural language and receive expert-level guided teaching in creating a Strands agent on AWS, so that I can learn to build a production-ready agent while understanding AWS services, Strands framework, and best practices.

#### Acceptance Criteria

1. WHEN a user provides a high-level description of their use case THEN the system SHALL analyze the requirements like an AWS Solutions Architect and suggest appropriate agent capabilities with cost and security considerations
2. WHEN the system analyzes a use case THEN it SHALL recommend relevant MCPs, AWS services, and tools with detailed explanations of why each is beneficial for the specific use case
3. WHEN a user is uncertain about their requirements THEN the system SHALL ask intelligent clarifying questions that progressively reveal technical complexity based on the user's experience level
4. WHEN asking clarifying questions THEN the system SHALL explain the implications of each choice in business terms (cost, security, performance, maintenance)
5. IF a use case is too broad or complex THEN the system SHALL suggest breaking it down into smaller, more manageable agent components with clear prioritization
6. WHEN the requirements phase is complete THEN the system SHALL provide a comprehensive summary of what will be built and why each decision was made

### Requirement 2

**User Story:** As a user building an agent, I want reliable access to comprehensive expertise through 16 specialized MCPs (12 AWS MCPs + GitHub Analysis + Perplexity Research + Strands Patterns + Filesystem), with semantic vector search powered by Amazon Bedrock Titan embeddings, real-time integrations, and intelligent query routing, so that my agent can leverage expert-level knowledge with 95%+ confidence and semantic understanding even when external services are unavailable.

#### Acceptance Criteria

1. WHEN the system recommends AWS-related capabilities THEN it SHALL provide information from 12 specialized AWS MCPs with Amazon Bedrock Titan vector embeddings for semantic understanding, cosine similarity search, multi-factor confidence scoring, and intelligent query routing achieving 95%+ accuracy
2. WHEN the system suggests agent patterns THEN it SHALL utilize cached Strands knowledge with 1536-dimension vector embeddings, Agent Core patterns, and automatic synchronization with embedding generation 2-3 times per week
3. WHEN users need repository analysis or MCP discovery THEN the system SHALL leverage GitHub Analysis MCP to find relevant repositories, analyze code patterns, and recommend optimal MCP combinations with confidence scoring
4. WHEN users require current trends or competitive analysis THEN the system SHALL use Perplexity Research MCP for real-time research, market analysis, and technology trend identification while maintaining cost controls
5. WHEN configuring an agent THEN the system SHALL automatically configure necessary MCP connections from all 16 available MCPs, provide offline capability through cached knowledge with semantic vector search, and include production-ready deployment guidance
6. WHEN MCPs are unavailable or fail THEN the system SHALL seamlessly fall back to synchronized knowledge base with vector search capabilities and maintain 95%+ confidence without service interruption
7. WHEN knowledge base data becomes stale THEN the system SHALL automatically attempt real-time MCP updates across all 16 MCPs, regenerate embeddings when needed, indicate data freshness to users, and apply freshness-based confidence scoring
8. WHEN users ask complex queries THEN the system SHALL use Amazon Bedrock Titan embeddings for semantic understanding, vector similarity search with 0.7 threshold, multi-dimensional query analysis, multi-MCP synthesis (AWS + GitHub + Perplexity + Strands), and provide expert-level responses with confidence validation
9. WHEN the system processes knowledge during sync THEN it SHALL generate vector embeddings using Amazon Bedrock Titan model for all MCP sources, store them securely in DynamoDB, and enable semantic search capabilities across all knowledge domains
10. WHEN users query the system THEN it SHALL intelligently route queries to appropriate MCPs (AWS for infrastructure, GitHub for code analysis, Perplexity for research, Strands for patterns), attempt vector search for semantic understanding, fall back to text search if needed, and combine results intelligently for optimal relevance

### Requirement 3

**User Story:** As a user, I want the platform to teach me how to use the Strands agent builder from GitHub, so that I can learn to create agents using proven, community-supported tooling and understand how to use Strands framework effectively.

#### Acceptance Criteria

1. WHEN creating an agent THEN the system SHALL teach the user how to use Strands agent builder and guide them through generating agent configurations
2. WHEN the Strands agent builder is used THEN the system SHALL explain how to translate user requirements into appropriate Strands agent specifications and demonstrate the process
3. WHEN generating agent code THEN the system SHALL teach Strands agent builder patterns and best practices with explanations of WHY each pattern is used
4. WHEN showing Strands integration THEN the system SHALL explain how Strands connects with AWS services (Lambda for action groups, OpenSearch for knowledge bases, Bedrock for AI)
5. IF the Strands agent builder is updated THEN the system SHALL be able to adapt to new versions and teach users about new features

### Requirement 4

**User Story:** As a user, I want multiple specialized agents to collaborate in helping me build my custom agent, so that I receive expert guidance across different domains and aspects of agent creation.

#### Acceptance Criteria

1. WHEN a user starts the agent creation process THEN the system SHALL deploy multiple specialized helper agents (requirements analyst, architecture advisor, implementation guide, etc.)
2. WHEN helper agents collaborate THEN they SHALL share context and coordinate their recommendations
3. WHEN conflicts arise between agent recommendations THEN the system SHALL present options to the user with clear explanations
4. WHEN the agent creation process progresses THEN different specialized agents SHALL take the lead based on the current phase

### Requirement 5

**User Story:** As a user, I want step-by-step expert guidance through the agent creation process with clear explanations and educational content, so that I can understand each decision, learn about agent development, and feel confident about the solution being built.

#### Acceptance Criteria

1. WHEN starting agent creation THEN the system SHALL present a clear workflow with defined phases (Requirements → Architecture → Implementation → Testing → Deployment) with progress indicators
2. WHEN completing each phase THEN the system SHALL explain what was accomplished, what comes next, and how it contributes to the overall solution
3. WHEN making configuration choices THEN the system SHALL explain the implications, trade-offs, costs, and security considerations in understandable business terms
4. WHEN technical decisions are made THEN the system SHALL provide educational context about why this approach is recommended and what alternatives were considered
5. WHEN the process is complete THEN the system SHALL provide comprehensive documentation including agent capabilities, usage instructions, deployment guide, cost analysis, and maintenance recommendations
6. WHEN users want to understand more THEN the system SHALL provide detailed explanations without overwhelming beginners with unnecessary complexity

### Requirement 6

**User Story:** As a user, I want to test and validate my created agent before deployment, so that I can ensure it meets my requirements.

#### Acceptance Criteria

1. WHEN an agent is created THEN the system SHALL provide a testing environment to validate functionality
2. WHEN testing an agent THEN the system SHALL simulate various scenarios relevant to the user's use case
3. WHEN issues are discovered during testing THEN the system SHALL suggest specific improvements or modifications
4. WHEN testing is complete THEN the system SHALL provide a validation report with recommendations

### Requirement 7

**User Story:** As a user, I want to export or deploy my created agent, so that I can use it in my intended environment.

#### Acceptance Criteria

1. WHEN an agent is validated THEN the system SHALL provide export options in multiple formats (configuration files, deployment scripts, etc.)
2. WHEN exporting an agent THEN the system SHALL include all necessary dependencies and configuration details
3. WHEN deploying an agent THEN the system SHALL provide clear instructions for the target environment
4. IF deployment fails THEN the system SHALL provide troubleshooting guidance and alternative deployment methods

### Requirement 8

**User Story:** As a user, I want to save and iterate on my agent designs, so that I can refine and improve them over time.

#### Acceptance Criteria

1. WHEN working on an agent THEN the system SHALL automatically save progress at each major step
2. WHEN returning to a saved agent project THEN the system SHALL restore the complete state and context
3. WHEN modifying an existing agent THEN the system SHALL track changes and allow rollback to previous versions
4. WHEN sharing agent designs THEN the system SHALL provide export/import functionality for collaboration
##
# Requirement 9

**User Story:** As a user, I want the platform to maintain reliable and up-to-date knowledge even when external services are unavailable, so that I can continue building agents without interruption.

#### Acceptance Criteria

1. WHEN external MCPs are unavailable THEN the system SHALL continue operating using synchronized knowledge base
2. WHEN knowledge base synchronization occurs THEN it SHALL happen automatically 2-3 times per week without user intervention
3. WHEN knowledge becomes outdated THEN the system SHALL indicate data freshness and attempt real-time updates
4. WHEN synchronization fails THEN the system SHALL alert administrators and provide fallback options
5. IF critical information is needed THEN the system SHALL attempt real-time MCP access even with cached data available

### Requirement 10

**User Story:** As a platform administrator, I want comprehensive monitoring and management of the knowledge synchronization system, so that I can ensure reliable service for all users.

#### Acceptance Criteria

1. WHEN knowledge synchronization runs THEN the system SHALL log all activities and status to CloudWatch
2. WHEN synchronization failures occur THEN the system SHALL send automated alerts and provide diagnostic information
3. WHEN knowledge base performance degrades THEN the system SHALL provide optimization recommendations
4. WHEN manual intervention is needed THEN the system SHALL provide tools for manual sync triggers and rollback capabilities#
## Requirement 11

**User Story:** As a user, I want each specialized agent to communicate like a real expert consultant in their domain, so that I receive professional-quality guidance and feel confident in the recommendations.

#### Acceptance Criteria

1. WHEN the Requirements Agent interacts with users THEN it SHALL communicate like an experienced AWS Solutions Architect with deep knowledge of costs, security, and best practices
2. WHEN the Architecture Agent provides recommendations THEN it SHALL explain decisions using AWS Well-Architected Framework principles and provide cost-benefit analysis
3. WHEN the Implementation Agent generates code THEN it SHALL explain the patterns used, security measures implemented, and how the code follows best practices
4. WHEN the Testing Agent validates solutions THEN it SHALL provide detailed analysis like a senior DevOps engineer including performance benchmarks and optimization recommendations
5. WHEN any agent encounters limitations or trade-offs THEN it SHALL clearly explain the constraints and provide alternative approaches
6. WHEN agents collaborate THEN they SHALL maintain consistent expertise levels and coordinate recommendations without contradicting each other

### Requirement 12

**User Story:** As a user, I want the complete agent creation process to be completed in under 60 minutes with minimal frustration, so that I can quickly get from idea to working agent without technical barriers.

#### Acceptance Criteria

1. WHEN a user starts the agent creation process THEN the complete workflow from initial description to deployable agent SHALL be completed in 30-45 minutes for typical use cases
2. WHEN users provide input THEN the system SHALL respond within 5 seconds to maintain engagement and flow
3. WHEN errors or issues occur THEN the system SHALL provide clear, actionable recovery steps without requiring technical debugging knowledge
4. WHEN users need to make decisions THEN the system SHALL provide smart defaults with clear explanations, allowing users to accept recommendations or customize as needed
5. WHEN the process is complete THEN users SHALL receive a fully functional, tested, and documented agent ready for deployment
6. WHEN users want to iterate or modify their agent THEN the system SHALL support rapid changes without restarting the entire process

### Requirement 13

**User Story:** As a user, I want the system to understand my queries semantically rather than just matching keywords, so that I receive more relevant and intelligent responses that understand the intent and context of my questions.

#### Acceptance Criteria

1. WHEN I ask about "cost-effective serverless architecture" THEN the system SHALL understand this semantically and find relevant content about "budget-friendly cloud solutions", "economical AWS patterns", and "free tier optimization" even if those exact words weren't used
2. WHEN I ask "My chatbot needs to handle more users" THEN the system SHALL semantically understand this as a scaling requirement and recommend auto-scaling patterns, load balancing strategies, and performance optimization solutions
3. WHEN the system processes my query THEN it SHALL generate vector embeddings using Amazon Bedrock Titan model and perform cosine similarity search against stored knowledge embeddings
4. WHEN vector search is unavailable THEN the system SHALL gracefully fall back to traditional text search without service interruption
5. WHEN the system returns results THEN it SHALL rank them by semantic relevance using similarity scores and provide more accurate matches than keyword-only search
6. WHEN knowledge is synchronized THEN the system SHALL automatically generate and store vector embeddings for all content to enable semantic search capabilities
7. WHEN I use technical terms or business language THEN the system SHALL understand both and find relevant technical solutions regardless of the vocabulary used
8. WHEN the system stores vectors THEN it SHALL use a hybrid storage architecture with DynamoDB (hot tier) for frequently accessed vectors and S3 (cold tier) for historical data, achieving 83% cost reduction while maintaining performance

### Requirement 14

**User Story:** As a user, I want to receive a complete, production-ready solution with all necessary components, so that I can deploy and use my agent immediately without additional development work.

#### Acceptance Criteria

1. WHEN an agent is generated THEN the system SHALL provide complete source code, configuration files, deployment scripts, and documentation including vector search capabilities if applicable
2. WHEN deployment instructions are provided THEN they SHALL include step-by-step commands that work on the first attempt with proper error handling and Bedrock permissions for embedding generation
3. WHEN security is configured THEN the system SHALL implement AWS security best practices including proper IAM roles, encryption for vector storage, and access controls for Bedrock services
4. WHEN cost optimization is applied THEN the system SHALL configure the agent to use AWS free tier where possible, optimize embedding generation costs (~$0.50/month), and provide ongoing cost monitoring including Bedrock usage
5. WHEN monitoring is set up THEN the system SHALL include CloudWatch dashboards, alerts, and performance tracking configured for the specific use case including vector search performance metrics
6. WHEN documentation is generated THEN it SHALL include user guides, API documentation, troubleshooting guides, maintenance procedures, and vector search configuration guidance

### Requirement 15

**User Story:** As a user, I want all AI agent responses to be validated using AWS Automated Reasoning checks to detect hallucinations and highlight unstated assumptions, so that I can trust the recommendations with 95%+ confidence and understand the reasoning behind each decision.

#### Acceptance Criteria

1. WHEN any AI agent (AWS Solutions Architect, Architecture Advisor, Implementation Guide, Testing Validator) generates a response THEN the system SHALL run AWS Automated Reasoning checks to validate logical consistency and detect potential hallucinations
2. WHEN Automated Reasoning detects unstated assumptions in agent responses THEN the system SHALL explicitly highlight these assumptions to the user with clear explanations
3. WHEN Automated Reasoning identifies logical inconsistencies or contradictions THEN the system SHALL flag these issues and request agent clarification before presenting to the user
4. WHEN confidence scoring is calculated THEN it SHALL incorporate Automated Reasoning validation results as a key factor in the multi-factor confidence score
5. WHEN agents make architectural recommendations THEN Automated Reasoning SHALL verify that the recommendations are logically sound, compatible with stated requirements, and free from contradictory constraints
6. WHEN code is generated THEN Automated Reasoning SHALL validate that the implementation matches the architecture design and requirements without introducing unstated dependencies or assumptions
7. WHEN cost estimates are provided THEN Automated Reasoning SHALL verify that all cost factors are accounted for and no hidden costs are assumed without disclosure
8. WHEN security recommendations are made THEN Automated Reasoning SHALL validate that security measures are complete, consistent, and don't rely on unstated security assumptions
9. WHEN the system integrates with Strands agent builder THEN Automated Reasoning SHALL validate that the generated Strands specifications are logically consistent with user requirements
10. WHEN deploying through Agent Core THEN Automated Reasoning SHALL verify that deployment configurations are complete and all dependencies are explicitly stated
11. WHEN Automated Reasoning validation fails THEN the system SHALL prevent the response from being presented to the user and trigger agent re-evaluation with specific feedback about the logical issues detected
12. WHEN all validations pass THEN the system SHALL include an Automated Reasoning confidence badge indicating the response has been formally verified for logical consistency

### Requirement 16

**User Story:** As a system architect, I want the platform to implement hierarchical multi-agent orchestration with manager, specialist, and validator agents following AWS best practices, so that complex tasks are decomposed, delegated, validated, and self-corrected for production-grade reliability.

#### Acceptance Criteria

1. WHEN the system starts agent creation workflow THEN it SHALL deploy a Manager Agent that coordinates planning, delegation, monitoring, and synthesis phases
2. WHEN complex tasks are identified THEN the Manager Agent SHALL decompose them into subtasks and delegate to appropriate Specialist Agents (data, code, infrastructure, security)
3. WHEN Specialist Agents complete tasks THEN Validator Agents SHALL review outputs for accuracy, completeness, and logical consistency before approval
4. WHEN agents execute tasks THEN they SHALL use chain-of-thought prompting to expose reasoning and enable self-review before submission
5. WHEN agents produce outputs with confidence below 0.85 threshold THEN the system SHALL trigger retry logic with reflection and validation loops
6. WHEN critical decisions are made (security policies, cost calculations, resource allocation) THEN the system SHALL use multi-model validation with ensemble voting
7. WHEN agents need context THEN they SHALL query multiple MCP servers dynamically for comprehensive information access
8. WHEN task execution occurs THEN the system SHALL use AWS Step Functions for orchestration with checkpoints and state management in DynamoDB
9. WHEN errors occur THEN the system SHALL implement exponential backoff with jitter, fallback strategies, and circuit breakers to prevent cascade failures
10. WHEN tasks fail repeatedly THEN the system SHALL use SQS dead letter queues and escalate to human-in-the-loop review
11. WHEN agents interact THEN the system SHALL log all interactions with CloudWatch metrics (latency, token usage, error rates) and X-Ray tracing
12. WHEN the system operates THEN it SHALL maintain task completion rate >95%, track first-attempt success rate, and measure average correction cycles per task

### Requirement 17

**User Story:** As a user, I want the platform to use Retrieval-Augmented Generation (RAG) with Amazon Bedrock Knowledge Bases to ensure all agent responses are grounded in verified facts with citation tracking, so that I receive accurate, source-backed recommendations.

#### Acceptance Criteria

1. WHEN agents generate responses THEN they SHALL query Amazon Bedrock Knowledge Bases with OpenSearch or Kendra before generating output
2. WHEN knowledge is retrieved THEN the system SHALL track citations and verify information sources for all factual claims
3. WHEN knowledge bases are updated THEN the system SHALL implement versioning and maintain update logs for traceability
4. WHEN agents access knowledge THEN they SHALL use short-term memory (DynamoDB for conversation history), long-term memory (S3 + embeddings for patterns), and episodic memory (task execution logs)
5. WHEN context is needed THEN the system SHALL use Amazon MemoryDB or ElastiCache for fast context retrieval across sessions
6. WHEN responses are generated THEN agents SHALL validate retrieved facts against multiple sources before inclusion
7. WHEN knowledge is stale THEN the system SHALL indicate data freshness and attempt real-time updates from MCP servers

### Requirement 18

**User Story:** As a platform administrator, I want comprehensive observability, monitoring, and continuous improvement mechanisms, so that the system learns from failures, improves over time, and maintains production-grade reliability.

#### Acceptance Criteria

1. WHEN the system operates THEN it SHALL log all agent interactions with outcomes to CloudWatch for analysis
2. WHEN monitoring occurs THEN the system SHALL track custom metrics including accuracy scores, task success rates, confidence distributions, and correction cycles
3. WHEN failures happen THEN the system SHALL analyze failure patterns monthly and implement improvements
4. WHEN prompts are updated THEN the system SHALL use A/B testing framework to validate improvements before deployment
5. WHEN agents complete tasks successfully THEN the system SHALL store successful patterns for future reference and potential fine-tuning
6. WHEN edge cases occur THEN the system SHALL implement human feedback loops for continuous learning
7. WHEN the system is evaluated THEN it SHALL measure and report: task completion rate (>95% target), first-attempt success rate, response accuracy (human evaluation), cost per successful task, and time to resolution
8. WHEN security events occur THEN the system SHALL use IAM roles, Secrets Manager, and KMS for secure operations with audit trails

### Requirement 19

**User Story:** As a system architect, I want advanced prompt engineering with multi-layer guardrails, semantic reasoning, and goal alignment to ensure exact task goal alignment, safety, and precise user intent fulfillment, so that every generated agent is perfectly aligned with user goals and production-ready.

#### Acceptance Criteria

1. WHEN constructing prompts THEN the system SHALL use structured prompt templates with explicit safety instructions, task constraints, output format specifications, and validation criteria embedded inline
2. WHEN processing user input THEN the system SHALL implement multi-layer input validation including prompt injection detection, malicious pattern filtering, input sanitization, length limits, and character encoding validation
3. WHEN generating agent responses THEN the system SHALL use chain-of-thought prompting to expose reasoning steps, enable self-review, and provide transparency in decision-making processes
4. WHEN validating outputs THEN the system SHALL scan generated code for security vulnerabilities, hardcoded credentials, weak IAM policies, missing error handling, and cost control gaps before delivery
5. WHEN semantic reasoning is required THEN the system SHALL use vector embeddings to understand user intent beyond keywords, map business language to technical solutions, and identify implicit requirements
6. WHEN ensuring goal alignment THEN the system SHALL validate that every recommendation directly addresses stated user goals, highlight any assumptions made, and confirm alignment before proceeding
7. WHEN safety is critical THEN the system SHALL enforce guardrails including: never generate unauthorized resource access, always include input validation, enforce least-privilege IAM, validate all inputs, never expose credentials, include rate limiting and cost controls
8. WHEN accuracy is paramount THEN the system SHALL only recommend services with high confidence, provide cost estimates with explicit assumptions, cite sources for technical claims, and use Automated Reasoning for validation
9. WHEN task completion is measured THEN the system SHALL achieve >95% first-attempt success rate, <0.85 confidence triggers retry with reflection, and all outputs pass multi-layer validation before delivery
10. WHEN prompts are engineered THEN the system SHALL use few-shot examples for complex tasks, provide clear success criteria, include edge case handling, and specify exact output formats with validation rules
11. WHEN handling ambiguity THEN the system SHALL ask clarifying questions rather than make assumptions, present options with trade-offs, and confirm understanding before proceeding
12. WHEN generating code THEN the system SHALL include comprehensive error handling, input validation, logging, monitoring hooks, security controls, and cost optimization patterns by default

### Requirement 20

**User Story:** As a user, I want every agent to maintain a baseline confidence floor of 95% with transparent confidence breakdowns and consultative communication patterns, so that I feel confident in the recommendations and maintain a sense of being consulted throughout the entire experience.

#### Acceptance Criteria

1. WHEN agents generate recommendations THEN the system SHALL enforce a minimum confidence threshold of 95% before presenting any output to users, with agents refusing to respond if confidence falls below this baseline
2. WHEN confidence scores are calculated THEN the system SHALL use multi-factor weighted scoring including information completeness (25%), requirement clarity (20%), technical feasibility (20%), validation coverage (15%), risk assessment (10%), and user alignment (10%)
3. WHEN presenting confidence to users THEN the system SHALL provide transparent breakdowns showing each confidence factor, what increases confidence, what reduces it, and specific actions to improve confidence
4. WHEN agents communicate THEN they SHALL use consultative language patterns including "Let's explore...", "What if we...", "I recommend..." rather than directive language like "You must..." or "Do this..."
5. WHEN making recommendations THEN agents SHALL explain their reasoning process, show why they're confident, cite specific sources, and acknowledge any uncertainties or assumptions explicitly
6. WHEN confidence is below 95% THEN agents SHALL proactively ask targeted clarifying questions to fill knowledge gaps, explain why they need the information, and show how it will improve the recommendation
7. WHEN presenting options THEN agents SHALL offer 2-3 alternative approaches with clear trade-offs, pros/cons analysis, and recommendations rather than single prescriptive solutions
8. WHEN users provide input THEN agents SHALL actively acknowledge understanding, summarize what they heard, validate interpretation, and ask "Does this align with your vision?" before proceeding
9. WHEN making critical decisions THEN agents SHALL use multi-model validation with ensemble voting, cross-validate with multiple knowledge sources, and boost confidence by 5% (capped at 98%) when all sources agree with >90% alignment
10. WHEN uncertainty exists THEN agents SHALL explicitly track known-knowns (certainties), known-unknowns (identified gaps), and assumed-knowns (risky assumptions), calculating confidence penalties of 3% per unknown and 2% per assumption
11. WHEN validation occurs THEN the system SHALL implement continuous validation loops throughout the workflow, checking confidence at each step, enhancing outputs when confidence drops below 90%, and maintaining confidence history across phases
12. WHEN communicating confidence THEN agents SHALL use certainty indicators in language ("I'm certain...", "Based on best practices...", "This is a common pattern...") and provide validation steps users can take to verify recommendations
13. WHEN agents collaborate THEN they SHALL maintain consistent expertise levels, coordinate recommendations without contradictions, and provide unified confidence assessments across all specialist agents
14. WHEN presenting technical information THEN agents SHALL progressively disclose complexity, starting simple and adding detail based on user questions, avoiding overwhelming users while maintaining technical accuracy
15. WHEN errors or limitations occur THEN agents SHALL acknowledge them transparently, explain constraints clearly, provide alternative approaches, and maintain trust through honest communication about what they can and cannot do