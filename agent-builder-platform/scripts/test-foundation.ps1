# Agent Builder Platform - Foundation Testing Script (PowerShell)
# Comprehensive testing without AWS deployment costs

param(
    [switch]$Verbose
)

# Test counters
$script:TestsRun = 0
$script:TestsPassed = 0
$script:TestsFailed = 0

# Logging functions
function Write-Log { 
    param($Message)
    Write-Host "[TEST] $Message" -ForegroundColor Blue
}

function Write-Success { 
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor Green
    $script:TestsPassed++
}

function Write-Failure { 
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor Red
    $script:TestsFailed++
}

function Write-Warning { 
    param($Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Info { 
    param($Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Start-Test {
    param($TestName)
    $script:TestsRun++
    Write-Log "Running: $TestName"
}

# Test 1: Project Structure Validation
function Test-ProjectStructure {
    Start-Test "Project Structure Validation"
    
    $requiredDirs = @(
        "infrastructure",
        "agent-core-config",
        "scripts",
        "docs"
    )
    
    $requiredFiles = @(
        "README.md",
        "infrastructure/main-stack.yaml",
        "agent-core-config/config.yaml",
        "scripts/deploy-infrastructure.sh",
        "scripts/validate-config.sh",
        "docs/troubleshooting.md",
        "docs/cost-optimization.md",
        "docs/security-compliance.md"
    )
    
    $structureValid = $true
    
    foreach ($dir in $requiredDirs) {
        if (Test-Path $dir -PathType Container) {
            Write-Info "Directory exists: $dir"
        } else {
            Write-Failure "Missing directory: $dir"
            $structureValid = $false
        }
    }
    
    foreach ($file in $requiredFiles) {
        if (Test-Path $file -PathType Leaf) {
            Write-Info "File exists: $file"
        } else {
            Write-Failure "Missing file: $file"
            $structureValid = $false
        }
    }
    
    if ($structureValid) {
        Write-Success "Project structure is complete"
    } else {
        Write-Failure "Project structure has missing components"
    }
}

# Test 2: CloudFormation Template Validation
function Test-CloudFormationTemplate {
    Start-Test "CloudFormation Template Syntax"
    
    if (Get-Command aws -ErrorAction SilentlyContinue) {
        try {
            $result = aws cloudformation validate-template --template-body file://infrastructure/main-stack.yaml --region us-east-1 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "CloudFormation template syntax is valid"
            } else {
                Write-Failure "CloudFormation template has syntax errors"
                Write-Host $result -ForegroundColor Red
            }
        } catch {
            Write-Failure "Error validating CloudFormation template: $_"
        }
    } else {
        Write-Warning "AWS CLI not available - skipping CloudFormation validation"
    }
}

# Test 3: Agent Core Configuration Validation
function Test-AgentCoreConfig {
    Start-Test "Agent Core Configuration"
    
    $configFile = "agent-core-config/config.yaml"
    $configValid = $true
    
    if (-not (Test-Path $configFile)) {
        Write-Failure "Agent Core configuration file not found: $configFile"
        return
    }
    
    $configContent = Get-Content $configFile -Raw
    
    # Check for required sections
    $requiredSections = @(
        "agents:",
        "mcps:",
        "tools:",
        "monitoring:",
        "environment:"
    )
    
    foreach ($section in $requiredSections) {
        if ($configContent -match [regex]::Escape($section)) {
            Write-Info "Configuration section found: $section"
        } else {
            Write-Failure "Missing configuration section: $section"
            $configValid = $false
        }
    }
    
    # Check for required agents
    $requiredAgents = @(
        "orchestrator:",
        "requirements-analyst:",
        "architecture-advisor:",
        "implementation-guide:",
        "testing-validator:"
    )
    
    foreach ($agent in $requiredAgents) {
        if ($configContent -match [regex]::Escape($agent)) {
            Write-Info "Expert consultant configured: $agent"
        } else {
            Write-Failure "Missing expert consultant: $agent"
            $configValid = $false
        }
    }
    
    # Check for Bedrock model configuration
    if ($configContent -match "bedrock:anthropic\.claude-3-haiku") {
        Write-Info "Bedrock model properly configured"
    } else {
        Write-Failure "Bedrock model configuration missing or incorrect"
        $configValid = $false
    }
    
    if ($configValid) {
        Write-Success "Agent Core configuration is complete"
    } else {
        Write-Failure "Agent Core configuration has issues"
    }
}

# Test 4: Script Permissions and Syntax
function Test-Scripts {
    Start-Test "Deployment Scripts"
    
    $scripts = @(
        "scripts/deploy-infrastructure.sh",
        "scripts/validate-config.sh"
    )
    
    $scriptsValid = $true
    
    foreach ($script in $scripts) {
        if (Test-Path $script) {
            # Check if script has shebang
            $firstLine = Get-Content $script -First 1
            if ($firstLine -match "^#!/bin/bash") {
                Write-Info "Script has proper shebang: $script"
            } else {
                Write-Failure "Script missing shebang: $script"
                $scriptsValid = $false
            }
            
            # Basic content check
            $content = Get-Content $script -Raw
            if ($content.Length -gt 100) {
                Write-Info "Script has content: $script"
            } else {
                Write-Failure "Script appears empty or too short: $script"
                $scriptsValid = $false
            }
        } else {
            Write-Failure "Script not found: $script"
            $scriptsValid = $false
        }
    }
    
    if ($scriptsValid) {
        Write-Success "All scripts are valid"
    } else {
        Write-Failure "Some scripts have issues"
    }
}

# Test 5: Documentation Completeness
function Test-Documentation {
    Start-Test "Documentation Completeness"
    
    $docsValid = $true
    
    # Check README content
    if (Test-Path "README.md") {
        $readmeContent = Get-Content "README.md" -Raw
        if ($readmeContent -match "Expert Consultation System") {
            Write-Info "README has proper title"
        } else {
            Write-Failure "README missing proper title"
            $docsValid = $false
        }
        
        if ($readmeContent -match "30-45 minutes") {
            Write-Info "README mentions target completion time"
        } else {
            Write-Failure "README missing completion time target"
            $docsValid = $false
        }
    } else {
        Write-Failure "README.md not found"
        $docsValid = $false
    }
    
    # Check troubleshooting guide
    if (Test-Path "docs/troubleshooting.md") {
        $troubleshootingContent = Get-Content "docs/troubleshooting.md" -Raw
        if ($troubleshootingContent -match "Common Issues and Solutions") {
            Write-Info "Troubleshooting guide has proper structure"
        } else {
            Write-Failure "Troubleshooting guide missing proper structure"
            $docsValid = $false
        }
    } else {
        Write-Failure "Troubleshooting guide not found"
        $docsValid = $false
    }
    
    # Check cost optimization guide
    if (Test-Path "docs/cost-optimization.md") {
        $costContent = Get-Content "docs/cost-optimization.md" -Raw
        if ($costContent -match "Hackathon Budget Management") {
            Write-Info "Cost optimization guide has budget focus"
        } else {
            Write-Failure "Cost optimization guide missing budget focus"
            $docsValid = $false
        }
    } else {
        Write-Failure "Cost optimization guide not found"
        $docsValid = $false
    }
    
    if ($docsValid) {
        Write-Success "Documentation is complete"
    } else {
        Write-Failure "Documentation has gaps"
    }
}

# Test 6: AWS Resource Configuration
function Test-AWSResources {
    Start-Test "AWS Resource Configuration"
    
    $resourcesValid = $true
    $template = "infrastructure/main-stack.yaml"
    
    if (-not (Test-Path $template)) {
        Write-Failure "CloudFormation template not found: $template"
        return
    }
    
    $templateContent = Get-Content $template -Raw
    
    # Check for required AWS resources
    $requiredResources = @(
        "AWS::S3::Bucket",
        "AWS::DynamoDB::Table",
        "AWS::ECS::Cluster",
        "AWS::EC2::VPC",
        "AWS::IAM::Role",
        "AWS::ElasticLoadBalancingV2::LoadBalancer"
    )
    
    foreach ($resource in $requiredResources) {
        if ($templateContent -match [regex]::Escape($resource)) {
            Write-Info "AWS resource configured: $resource"
        } else {
            Write-Failure "Missing AWS resource: $resource"
            $resourcesValid = $false
        }
    }
    
    # Check for cost optimization features
    if ($templateContent -match "FARGATE_SPOT") {
        Write-Info "Fargate Spot configured for cost optimization"
    } else {
        Write-Warning "Fargate Spot not configured - may increase costs"
    }
    
    if ($templateContent -match "PAY_PER_REQUEST") {
        Write-Info "DynamoDB pay-per-request configured"
    } else {
        Write-Failure "DynamoDB not configured for pay-per-request"
        $resourcesValid = $false
    }
    
    if ($resourcesValid) {
        Write-Success "AWS resources properly configured"
    } else {
        Write-Failure "AWS resource configuration has issues"
    }
}

# Test 7: Security Configuration
function Test-SecurityConfig {
    Start-Test "Security Configuration"
    
    $securityValid = $true
    $template = "infrastructure/main-stack.yaml"
    
    if (-not (Test-Path $template)) {
        Write-Failure "CloudFormation template not found: $template"
        return
    }
    
    $templateContent = Get-Content $template -Raw
    
    # Check for security features
    if ($templateContent -match "SSEEnabled: true") {
        Write-Info "Encryption at rest configured"
    } else {
        Write-Failure "Encryption at rest not configured"
        $securityValid = $false
    }
    
    if ($templateContent -match "PublicAccessBlockConfiguration") {
        Write-Info "S3 public access blocking configured"
    } else {
        Write-Failure "S3 public access blocking not configured"
        $securityValid = $false
    }
    
    if ($templateContent -match "SecurityGroupIngress") {
        Write-Info "Security groups configured"
    } else {
        Write-Failure "Security groups not properly configured"
        $securityValid = $false
    }
    
    # Check IAM policies
    if ($templateContent -match "bedrock:InvokeModel") {
        Write-Info "Bedrock permissions configured"
    } else {
        Write-Failure "Bedrock permissions not configured"
        $securityValid = $false
    }
    
    if ($securityValid) {
        Write-Success "Security configuration is proper"
    } else {
        Write-Failure "Security configuration has issues"
    }
}

# Test 8: Cost Optimization Features
function Test-CostOptimization {
    Start-Test "Cost Optimization Features"
    
    $costValid = $true
    $template = "infrastructure/main-stack.yaml"
    
    if (-not (Test-Path $template)) {
        Write-Failure "CloudFormation template not found: $template"
        return
    }
    
    $templateContent = Get-Content $template -Raw
    
    # Check lifecycle policies
    if ($templateContent -match "LifecycleConfiguration") {
        Write-Info "S3 lifecycle policies configured"
    } else {
        Write-Warning "S3 lifecycle policies not configured"
    }
    
    # Check for free tier optimization
    if ($templateContent -match "BillingMode: PAY_PER_REQUEST") {
        Write-Info "DynamoDB configured for free tier optimization"
    } else {
        Write-Failure "DynamoDB not optimized for free tier"
        $costValid = $false
    }
    
    # Check monitoring configuration
    $deployScript = "scripts/deploy-infrastructure.sh"
    if (Test-Path $deployScript) {
        $deployContent = Get-Content $deployScript -Raw
        if ($deployContent -match "EstimatedCharges") {
            Write-Info "Cost monitoring configured"
        } else {
            Write-Failure "Cost monitoring not configured"
            $costValid = $false
        }
    } else {
        Write-Failure "Deployment script not found"
        $costValid = $false
    }
    
    if ($costValid) {
        Write-Success "Cost optimization features configured"
    } else {
        Write-Failure "Cost optimization needs improvement"
    }
}

# Test 9: Environment Variable Validation
function Test-EnvironmentValidation {
    Start-Test "Environment Variable Validation"
    
    $envValid = $true
    
    # Check if validation script exists
    if (Test-Path "scripts/validate-config.sh") {
        $validationContent = Get-Content "scripts/validate-config.sh" -Raw
        if ($validationContent.Length -gt 1000) {
            Write-Info "Environment validation script has content"
        } else {
            Write-Failure "Environment validation script appears incomplete"
            $envValid = $false
        }
    } else {
        Write-Failure "Environment validation script missing"
        $envValid = $false
    }
    
    # Check Agent Core config for environment validation
    if (Test-Path "agent-core-config/config.yaml") {
        $configContent = Get-Content "agent-core-config/config.yaml" -Raw
        if ($configContent -match "required_variables:") {
            Write-Info "Agent Core config has environment validation"
        } else {
            Write-Failure "Agent Core config missing environment validation"
            $envValid = $false
        }
    } else {
        Write-Failure "Agent Core config not found"
        $envValid = $false
    }
    
    if ($envValid) {
        Write-Success "Environment validation is configured"
    } else {
        Write-Failure "Environment validation needs work"
    }
}

# Test 10: Integration Readiness
function Test-IntegrationReadiness {
    Start-Test "Integration Readiness"
    
    $integrationValid = $true
    
    if (-not (Test-Path "agent-core-config/config.yaml")) {
        Write-Failure "Agent Core config not found"
        return
    }
    
    $configContent = Get-Content "agent-core-config/config.yaml" -Raw
    
    # Check for MCP configuration
    if ($configContent -match "aws-docs:") {
        Write-Info "AWS docs MCP configured"
    } else {
        Write-Failure "AWS docs MCP not configured"
        $integrationValid = $false
    }
    
    if ($configContent -match "strands:") {
        Write-Info "Strands MCP configured"
    } else {
        Write-Failure "Strands MCP not configured"
        $integrationValid = $false
    }
    
    if ($configContent -match "github:") {
        Write-Info "GitHub MCP configured"
    } else {
        Write-Failure "GitHub MCP not configured"
        $integrationValid = $false
    }
    
    # Check for tool stubs
    if ($configContent -match "tool_implementations:") {
        Write-Info "Tool implementation stubs configured"
    } else {
        Write-Failure "Tool implementation stubs missing"
        $integrationValid = $false
    }
    
    if ($integrationValid) {
        Write-Success "Integration readiness is good"
    } else {
        Write-Failure "Integration readiness needs work"
    }
}

# Generate test report
function Write-TestReport {
    Write-Host ""
    Write-Host "🧪 Foundation Testing Report" -ForegroundColor Magenta
    Write-Host "============================" -ForegroundColor Magenta
    Write-Host ""
    
    $passRate = [math]::Round(($script:TestsPassed * 100 / $script:TestsRun), 0)
    
    Write-Host "📊 Test Results:"
    Write-Host "  • Tests Run: $($script:TestsRun)"
    Write-Host "  • Tests Passed: $($script:TestsPassed)"
    Write-Host "  • Tests Failed: $($script:TestsFailed)"
    Write-Host "  • Pass Rate: $passRate%"
    Write-Host ""
    
    if ($script:TestsFailed -eq 0) {
        Write-Success "All tests passed! Foundation is ready for deployment."
        Write-Host ""
        Write-Host "🚀 Next Steps:"
        Write-Host "  1. Set up environment variables (AWS credentials, GitHub token)"
        Write-Host "  2. Run AWS connectivity test (Phase 3)"
        Write-Host "  3. Deploy with './scripts/deploy-infrastructure.sh'"
        Write-Host "  4. Monitor costs in AWS Billing Dashboard"
        return 0
    } elseif ($passRate -ge 80) {
        Write-Warning "Most tests passed ($passRate%). Review failed tests before deployment."
        Write-Host ""
        Write-Host "🔧 Recommended Actions:"
        Write-Host "  1. Fix the $($script:TestsFailed) failed test(s) above"
        Write-Host "  2. Re-run this test script"
        Write-Host "  3. Proceed with deployment once all tests pass"
        return 1
    } else {
        Write-Failure "Too many tests failed ($($script:TestsFailed)/$($script:TestsRun)). Foundation needs work."
        Write-Host ""
        Write-Host "❌ Required Actions:"
        Write-Host "  1. Address all failed tests listed above"
        Write-Host "  2. Review documentation for guidance"
        Write-Host "  3. Re-run tests before attempting deployment"
        return 2
    }
}

# Main execution
function Main {
    Write-Host "🧪 Agent Builder Platform - Foundation Testing" -ForegroundColor Magenta
    Write-Host "===============================================" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "Testing foundation without AWS deployment costs..." -ForegroundColor Cyan
    Write-Host ""
    
    # Change to the correct directory if needed
    if (-not (Test-Path "infrastructure/main-stack.yaml")) {
        if (Test-Path "agent-builder-platform/infrastructure/main-stack.yaml") {
            Set-Location "agent-builder-platform"
            Write-Info "Changed to agent-builder-platform directory"
        } else {
            Write-Failure "Cannot find project files. Please run from the correct directory."
            return 1
        }
    }
    
    Test-ProjectStructure
    Test-CloudFormationTemplate
    Test-AgentCoreConfig
    Test-Scripts
    Test-Documentation
    Test-AWSResources
    Test-SecurityConfig
    Test-CostOptimization
    Test-EnvironmentValidation
    Test-IntegrationReadiness
    
    Write-TestReport
}

# Run the tests
Main