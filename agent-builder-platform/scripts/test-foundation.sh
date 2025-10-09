#!/bin/bash

# Agent Builder Platform - Foundation Testing Script
# Comprehensive testing without AWS deployment costs

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Logging functions
log() { echo -e "${BLUE}[TEST]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; ((TESTS_PASSED++)); }
failure() { echo -e "${RED}❌ $1${NC}"; ((TESTS_FAILED++)); }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
info() { echo -e "${PURPLE}ℹ️  $1${NC}"; }

run_test() {
    ((TESTS_RUN++))
    log "Running: $1"
}

# Test 1: Project Structure Validation
test_project_structure() {
    run_test "Project Structure Validation"
    
    local required_dirs=(
        "infrastructure"
        "agent-core-config"
        "scripts"
        "docs"
    )
    
    local required_files=(
        "README.md"
        "infrastructure/main-stack.yaml"
        "agent-core-config/config.yaml"
        "scripts/deploy-infrastructure.sh"
        "scripts/validate-config.sh"
        "docs/troubleshooting.md"
        "docs/cost-optimization.md"
        "docs/security-compliance.md"
    )
    
    local structure_valid=true
    
    for dir in "${required_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            info "Directory exists: $dir"
        else
            failure "Missing directory: $dir"
            structure_valid=false
        fi
    done
    
    for file in "${required_files[@]}"; do
        if [[ -f "$file" ]]; then
            info "File exists: $file"
        else
            failure "Missing file: $file"
            structure_valid=false
        fi
    done
    
    if $structure_valid; then
        success "Project structure is complete"
    else
        failure "Project structure has missing components"
    fi
}

# Test 2: CloudFormation Template Validation
test_cloudformation_template() {
    run_test "CloudFormation Template Syntax"
    
    if command -v aws &> /dev/null; then
        if aws cloudformation validate-template \
           --template-body file://infrastructure/main-stack.yaml \
           --region us-east-1 &> /dev/null; then
            success "CloudFormation template syntax is valid"
        else
            failure "CloudFormation template has syntax errors"
            aws cloudformation validate-template \
                --template-body file://infrastructure/main-stack.yaml \
                --region us-east-1 2>&1 | head -5
        fi
    else
        warning "AWS CLI not available - skipping CloudFormation validation"
    fi
}

# Test 3: Agent Core Configuration Validation
test_agent_core_config() {
    run_test "Agent Core Configuration"
    
    local config_file="agent-core-config/config.yaml"
    local config_valid=true
    
    # Check for required sections
    local required_sections=(
        "agents:"
        "mcps:"
        "tools:"
        "monitoring:"
        "environment:"
    )
    
    for section in "${required_sections[@]}"; do
        if grep -q "$section" "$config_file"; then
            info "Configuration section found: $section"
        else
            failure "Missing configuration section: $section"
            config_valid=false
        fi
    done
    
    # Check for required agents
    local required_agents=(
        "orchestrator:"
        "requirements-analyst:"
        "architecture-advisor:"
        "implementation-guide:"
        "testing-validator:"
    )
    
    for agent in "${required_agents[@]}"; do
        if grep -q "$agent" "$config_file"; then
            info "Expert consultant configured: $agent"
        else
            failure "Missing expert consultant: $agent"
            config_valid=false
        fi
    done
    
    # Check for Bedrock model configuration
    if grep -q "bedrock:anthropic.claude-3-haiku" "$config_file"; then
        info "Bedrock model properly configured"
    else
        failure "Bedrock model configuration missing or incorrect"
        config_valid=false
    fi
    
    if $config_valid; then
        success "Agent Core configuration is complete"
    else
        failure "Agent Core configuration has issues"
    fi
}

# Test 4: Script Permissions and Syntax
test_scripts() {
    run_test "Deployment Scripts"
    
    local scripts=(
        "scripts/deploy-infrastructure.sh"
        "scripts/validate-config.sh"
    )
    
    local scripts_valid=true
    
    for script in "${scripts[@]}"; do
        if [[ -f "$script" ]]; then
            # Check if script has shebang
            if head -1 "$script" | grep -q "#!/bin/bash"; then
                info "Script has proper shebang: $script"
            else
                failure "Script missing shebang: $script"
                scripts_valid=false
            fi
            
            # Basic syntax check
            if bash -n "$script" 2>/dev/null; then
                info "Script syntax is valid: $script"
            else
                failure "Script has syntax errors: $script"
                scripts_valid=false
            fi
        else
            failure "Script not found: $script"
            scripts_valid=false
        fi
    done
    
    if $scripts_valid; then
        success "All scripts are valid"
    else
        failure "Some scripts have issues"
    fi
}

# Test 5: Documentation Completeness
test_documentation() {
    run_test "Documentation Completeness"
    
    local docs_valid=true
    
    # Check README content
    if grep -q "Expert Consultation System" README.md; then
        info "README has proper title"
    else
        failure "README missing proper title"
        docs_valid=false
    fi
    
    if grep -q "30-45 minutes" README.md; then
        info "README mentions target completion time"
    else
        failure "README missing completion time target"
        docs_valid=false
    fi
    
    # Check troubleshooting guide
    if grep -q "Common Issues and Solutions" docs/troubleshooting.md; then
        info "Troubleshooting guide has proper structure"
    else
        failure "Troubleshooting guide missing proper structure"
        docs_valid=false
    fi
    
    # Check cost optimization guide
    if grep -q "Hackathon Budget Management" docs/cost-optimization.md; then
        info "Cost optimization guide has budget focus"
    else
        failure "Cost optimization guide missing budget focus"
        docs_valid=false
    fi
    
    if $docs_valid; then
        success "Documentation is complete"
    else
        failure "Documentation has gaps"
    fi
}

# Test 6: AWS Resource Configuration
test_aws_resources() {
    run_test "AWS Resource Configuration"
    
    local resources_valid=true
    local template="infrastructure/main-stack.yaml"
    
    # Check for required AWS resources
    local required_resources=(
        "AWS::S3::Bucket"
        "AWS::DynamoDB::Table"
        "AWS::ECS::Cluster"
        "AWS::EC2::VPC"
        "AWS::IAM::Role"
        "AWS::ElasticLoadBalancingV2::LoadBalancer"
    )
    
    for resource in "${required_resources[@]}"; do
        if grep -q "$resource" "$template"; then
            info "AWS resource configured: $resource"
        else
            failure "Missing AWS resource: $resource"
            resources_valid=false
        fi
    done
    
    # Check for cost optimization features
    if grep -q "FARGATE_SPOT" "$template"; then
        info "Fargate Spot configured for cost optimization"
    else
        warning "Fargate Spot not configured - may increase costs"
    fi
    
    if grep -q "PAY_PER_REQUEST" "$template"; then
        info "DynamoDB pay-per-request configured"
    else
        failure "DynamoDB not configured for pay-per-request"
        resources_valid=false
    fi
    
    if $resources_valid; then
        success "AWS resources properly configured"
    else
        failure "AWS resource configuration has issues"
    fi
}

# Test 7: Security Configuration
test_security_config() {
    run_test "Security Configuration"
    
    local security_valid=true
    local template="infrastructure/main-stack.yaml"
    
    # Check for security features
    if grep -q "SSEEnabled: true" "$template"; then
        info "Encryption at rest configured"
    else
        failure "Encryption at rest not configured"
        security_valid=false
    fi
    
    if grep -q "PublicAccessBlockConfiguration" "$template"; then
        info "S3 public access blocking configured"
    else
        failure "S3 public access blocking not configured"
        security_valid=false
    fi
    
    if grep -q "SecurityGroupIngress" "$template"; then
        info "Security groups configured"
    else
        failure "Security groups not properly configured"
        security_valid=false
    fi
    
    # Check IAM policies
    if grep -q "bedrock:InvokeModel" "$template"; then
        info "Bedrock permissions configured"
    else
        failure "Bedrock permissions not configured"
        security_valid=false
    fi
    
    if $security_valid; then
        success "Security configuration is proper"
    else
        failure "Security configuration has issues"
    fi
}

# Test 8: Cost Optimization Features
test_cost_optimization() {
    run_test "Cost Optimization Features"
    
    local cost_valid=true
    local template="infrastructure/main-stack.yaml"
    
    # Check lifecycle policies
    if grep -q "LifecycleConfiguration" "$template"; then
        info "S3 lifecycle policies configured"
    else
        warning "S3 lifecycle policies not configured"
    fi
    
    # Check for free tier optimization
    if grep -q "BillingMode: PAY_PER_REQUEST" "$template"; then
        info "DynamoDB configured for free tier optimization"
    else
        failure "DynamoDB not optimized for free tier"
        cost_valid=false
    fi
    
    # Check monitoring configuration
    if grep -q "EstimatedCharges" scripts/deploy-infrastructure.sh; then
        info "Cost monitoring configured"
    else
        failure "Cost monitoring not configured"
        cost_valid=false
    fi
    
    if $cost_valid; then
        success "Cost optimization features configured"
    else
        failure "Cost optimization needs improvement"
    fi
}

# Test 9: Environment Variable Validation
test_environment_validation() {
    run_test "Environment Variable Validation"
    
    local env_valid=true
    
    # Check if validation script exists and works
    if [[ -f "scripts/validate-config.sh" ]]; then
        if bash -n scripts/validate-config.sh; then
            info "Environment validation script syntax is correct"
        else
            failure "Environment validation script has syntax errors"
            env_valid=false
        fi
    else
        failure "Environment validation script missing"
        env_valid=false
    fi
    
    # Check Agent Core config for environment validation
    if grep -q "required_variables:" agent-core-config/config.yaml; then
        info "Agent Core config has environment validation"
    else
        failure "Agent Core config missing environment validation"
        env_valid=false
    fi
    
    if $env_valid; then
        success "Environment validation is configured"
    else
        failure "Environment validation needs work"
    fi
}

# Test 10: Integration Readiness
test_integration_readiness() {
    run_test "Integration Readiness"
    
    local integration_valid=true
    
    # Check for MCP configuration
    if grep -q "aws-docs:" agent-core-config/config.yaml; then
        info "AWS docs MCP configured"
    else
        failure "AWS docs MCP not configured"
        integration_valid=false
    fi
    
    if grep -q "strands:" agent-core-config/config.yaml; then
        info "Strands MCP configured"
    else
        failure "Strands MCP not configured"
        integration_valid=false
    fi
    
    if grep -q "github:" agent-core-config/config.yaml; then
        info "GitHub MCP configured"
    else
        failure "GitHub MCP not configured"
        integration_valid=false
    fi
    
    # Check for tool stubs
    if grep -q "tool_implementations:" agent-core-config/config.yaml; then
        info "Tool implementation stubs configured"
    else
        failure "Tool implementation stubs missing"
        integration_valid=false
    fi
    
    if $integration_valid; then
        success "Integration readiness is good"
    else
        failure "Integration readiness needs work"
    fi
}

# Generate test report
generate_test_report() {
    echo
    echo "🧪 Foundation Testing Report"
    echo "============================"
    echo
    
    local pass_rate=$((TESTS_PASSED * 100 / TESTS_RUN))
    
    echo "📊 Test Results:"
    echo "  • Tests Run: $TESTS_RUN"
    echo "  • Tests Passed: $TESTS_PASSED"
    echo "  • Tests Failed: $TESTS_FAILED"
    echo "  • Pass Rate: $pass_rate%"
    echo
    
    if (( TESTS_FAILED == 0 )); then
        success "All tests passed! Foundation is ready for deployment."
        echo
        echo "🚀 Next Steps:"
        echo "  1. Set up environment variables (AWS credentials, GitHub token)"
        echo "  2. Run './scripts/validate-config.sh' for AWS connectivity"
        echo "  3. Deploy with './scripts/deploy-infrastructure.sh'"
        echo "  4. Monitor costs in AWS Billing Dashboard"
        return 0
    elif (( pass_rate >= 80 )); then
        warning "Most tests passed ($pass_rate%). Review failed tests before deployment."
        echo
        echo "🔧 Recommended Actions:"
        echo "  1. Fix the $TESTS_FAILED failed test(s) above"
        echo "  2. Re-run this test script"
        echo "  3. Proceed with deployment once all tests pass"
        return 1
    else
        failure "Too many tests failed ($TESTS_FAILED/$TESTS_RUN). Foundation needs work."
        echo
        echo "❌ Required Actions:"
        echo "  1. Address all failed tests listed above"
        echo "  2. Review documentation for guidance"
        echo "  3. Re-run tests before attempting deployment"
        return 2
    fi
}

# Main test execution
main() {
    echo "🧪 Agent Builder Platform - Foundation Testing"
    echo "=============================================="
    echo
    echo "Testing foundation without AWS deployment costs..."
    echo
    
    test_project_structure
    test_cloudformation_template
    test_agent_core_config
    test_scripts
    test_documentation
    test_aws_resources
    test_security_config
    test_cost_optimization
    test_environment_validation
    test_integration_readiness
    
    generate_test_report
}

# Run tests
main "$@"