#!/bin/bash

# Agent Builder Platform - Configuration Validation Script
# Validates all configuration files and environment setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log() { echo -e "${BLUE}[VALIDATE]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

VALIDATION_ERRORS=0
VALIDATION_WARNINGS=0

# Validate environment variables
validate_environment() {
    log "Validating environment variables..."
    
    # Required variables
    REQUIRED_VARS=(
        "AWS_REGION"
        "AWS_ACCOUNT_ID" 
        "GITHUB_TOKEN"
    )
    
    for var in "${REQUIRED_VARS[@]}"; do
        if [[ -z "${!var}" ]]; then
            error "Required environment variable $var is not set"
            ((VALIDATION_ERRORS++))
        else
            success "Environment variable $var is set"
        fi
    done
    
    # Validate AWS_REGION format
    if [[ -n "$AWS_REGION" ]]; then
        if [[ $AWS_REGION =~ ^[a-z]{2}-[a-z]+-[0-9]$ ]]; then
            success "AWS_REGION format is valid: $AWS_REGION"
        else
            error "AWS_REGION format is invalid: $AWS_REGION (expected format: us-east-1)"
            ((VALIDATION_ERRORS++))
        fi
    fi
    
    # Validate AWS_ACCOUNT_ID format
    if [[ -n "$AWS_ACCOUNT_ID" ]]; then
        if [[ $AWS_ACCOUNT_ID =~ ^[0-9]{12}$ ]]; then
            success "AWS_ACCOUNT_ID format is valid"
        else
            error "AWS_ACCOUNT_ID format is invalid (expected 12 digits)"
            ((VALIDATION_ERRORS++))
        fi
    fi
    
    # Validate GITHUB_TOKEN format
    if [[ -n "$GITHUB_TOKEN" ]]; then
        if [[ $GITHUB_TOKEN =~ ^gh[ps]_[A-Za-z0-9_]{36,}$ ]]; then
            success "GITHUB_TOKEN format is valid"
        else
            warning "GITHUB_TOKEN format may be invalid (expected ghp_ or ghs_ prefix)"
            ((VALIDATION_WARNINGS++))
        fi
    fi
}

# Validate AWS connectivity
validate_aws_connectivity() {
    log "Validating AWS connectivity..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        error "AWS CLI is not installed"
        ((VALIDATION_ERRORS++))
        return
    fi
    
    # Check AWS credentials
    if aws sts get-caller-identity &> /dev/null; then
        success "AWS credentials are valid"
        
        # Get account info
        ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        USER_ARN=$(aws sts get-caller-identity --query Arn --output text)
        
        log "Connected as: $USER_ARN"
        log "Account ID: $ACCOUNT_ID"
        
        # Validate account ID matches environment
        if [[ -n "$AWS_ACCOUNT_ID" && "$AWS_ACCOUNT_ID" != "$ACCOUNT_ID" ]]; then
            error "AWS_ACCOUNT_ID environment variable ($AWS_ACCOUNT_ID) doesn't match actual account ($ACCOUNT_ID)"
            ((VALIDATION_ERRORS++))
        fi
    else
        error "AWS credentials are invalid or not configured"
        ((VALIDATION_ERRORS++))
    fi
}

# Validate Bedrock access
validate_bedrock_access() {
    log "Validating Bedrock access..."
    
    if aws bedrock list-foundation-models --region ${AWS_REGION:-us-east-1} &> /dev/null; then
        success "Bedrock access is available"
        
        # Check for Claude 3 Haiku model
        if aws bedrock list-foundation-models --region ${AWS_REGION:-us-east-1} \
           --query 'modelSummaries[?contains(modelId, `claude-3-haiku`)]' \
           --output text | grep -q claude; then
            success "Claude 3 Haiku model is available"
        else
            warning "Claude 3 Haiku model may not be available in this region"
            ((VALIDATION_WARNINGS++))
        fi
    else
        error "Bedrock access is not available - required for AI consultants"
        ((VALIDATION_ERRORS++))
    fi
}

# Validate CloudFormation template
validate_cloudformation() {
    log "Validating CloudFormation template..."
    
    if [[ ! -f "infrastructure/main-stack.yaml" ]]; then
        error "CloudFormation template not found: infrastructure/main-stack.yaml"
        ((VALIDATION_ERRORS++))
        return
    fi
    
    if aws cloudformation validate-template \
       --template-body file://infrastructure/main-stack.yaml \
       --region ${AWS_REGION:-us-east-1} &> /dev/null; then
        success "CloudFormation template is valid"
    else
        error "CloudFormation template validation failed"
        ((VALIDATION_ERRORS++))
    fi
}

# Validate Agent Core configuration
validate_agent_core_config() {
    log "Validating Agent Core configuration..."
    
    CONFIG_FILE="agent-core-config/config.yaml"
    
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error "Agent Core configuration not found: $CONFIG_FILE"
        ((VALIDATION_ERRORS++))
        return
    fi
    
    # Check for required sections
    REQUIRED_SECTIONS=(
        "agents:"
        "mcps:"
        "tools:"
        "monitoring:"
    )
    
    for section in "${REQUIRED_SECTIONS[@]}"; do
        if grep -q "$section" "$CONFIG_FILE"; then
            success "Configuration section found: $section"
        else
            error "Required configuration section missing: $section"
            ((VALIDATION_ERRORS++))
        fi
    done
    
    # Check for required agents
    REQUIRED_AGENTS=(
        "orchestrator:"
        "requirements-analyst:"
        "architecture-advisor:"
        "implementation-guide:"
        "testing-validator:"
    )
    
    for agent in "${REQUIRED_AGENTS[@]}"; do
        if grep -q "$agent" "$CONFIG_FILE"; then
            success "Expert consultant configured: $agent"
        else
            error "Required expert consultant missing: $agent"
            ((VALIDATION_ERRORS++))
        fi
    done
}

# Validate project structure
validate_project_structure() {
    log "Validating project structure..."
    
    REQUIRED_DIRS=(
        "infrastructure"
        "agent-core-config"
        "scripts"
    )
    
    REQUIRED_FILES=(
        "README.md"
        "infrastructure/main-stack.yaml"
        "agent-core-config/config.yaml"
        "scripts/deploy-infrastructure.sh"
    )
    
    for dir in "${REQUIRED_DIRS[@]}"; do
        if [[ -d "$dir" ]]; then
            success "Directory exists: $dir"
        else
            error "Required directory missing: $dir"
            ((VALIDATION_ERRORS++))
        fi
    done
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [[ -f "$file" ]]; then
            success "File exists: $file"
        else
            error "Required file missing: $file"
            ((VALIDATION_ERRORS++))
        fi
    done
}

# Validate deployment readiness
validate_deployment_readiness() {
    log "Validating deployment readiness..."
    
    # Check if deployment script is executable
    if [[ -x "scripts/deploy-infrastructure.sh" ]]; then
        success "Deployment script is executable"
    else
        warning "Deployment script may not be executable"
        ((VALIDATION_WARNINGS++))
    fi
    
    # Check for .env file (should not exist before deployment)
    if [[ -f ".env" ]]; then
        warning ".env file already exists - may contain stale configuration"
        ((VALIDATION_WARNINGS++))
    else
        success "No stale .env file found"
    fi
    
    # Validate cost thresholds
    if [[ -n "$COST_THRESHOLD_WARNING" ]]; then
        if (( $(echo "$COST_THRESHOLD_WARNING <= 20" | bc -l) )); then
            success "Cost warning threshold is within budget: \$$COST_THRESHOLD_WARNING"
        else
            warning "Cost warning threshold exceeds recommended budget: \$$COST_THRESHOLD_WARNING"
            ((VALIDATION_WARNINGS++))
        fi
    fi
}

# Generate validation report
generate_report() {
    echo
    echo "🔍 Configuration Validation Report"
    echo "=================================="
    echo
    
    if (( VALIDATION_ERRORS == 0 )); then
        success "All critical validations passed!"
    else
        error "$VALIDATION_ERRORS critical validation errors found"
    fi
    
    if (( VALIDATION_WARNINGS > 0 )); then
        warning "$VALIDATION_WARNINGS warnings found"
    else
        success "No warnings found"
    fi
    
    echo
    echo "📊 Validation Summary:"
    echo "  • Errors: $VALIDATION_ERRORS"
    echo "  • Warnings: $VALIDATION_WARNINGS"
    echo
    
    if (( VALIDATION_ERRORS == 0 )); then
        echo "✅ Configuration is ready for deployment!"
        echo
        echo "🚀 Next Steps:"
        echo "  1. Run './scripts/deploy-infrastructure.sh' to deploy AWS infrastructure"
        echo "  2. Monitor costs using AWS Billing Dashboard"
        echo "  3. Proceed with Task 2: MCP integrations and knowledge synchronization"
        return 0
    else
        echo "❌ Configuration has critical errors that must be fixed before deployment"
        echo
        echo "🔧 Required Actions:"
        echo "  1. Fix all validation errors listed above"
        echo "  2. Re-run this validation script"
        echo "  3. Only proceed with deployment after all errors are resolved"
        return 1
    fi
}

# Main validation function
main() {
    echo "🔍 Agent Builder Platform - Configuration Validation"
    echo "===================================================="
    echo
    
    validate_project_structure
    validate_environment
    validate_aws_connectivity
    validate_bedrock_access
    validate_cloudformation
    validate_agent_core_config
    validate_deployment_readiness
    
    generate_report
}

# Run validation
main "$@"