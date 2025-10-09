#!/usr/bin/env python3
"""
Output Validation Scanner
Comprehensive validation of AI-generated outputs for security, credentials, IAM, error handling, and cost controls
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class FindingSeverity(Enum):
    """Severity levels for validation findings"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class FindingCategory(Enum):
    """Categories of validation findings"""
    SECURITY = "security"
    CREDENTIALS = "credentials"
    IAM_POLICY = "iam_policy"
    ERROR_HANDLING = "error_handling"
    COST_CONTROL = "cost_control"
    BEST_PRACTICE = "best_practice"
    COMPLIANCE = "compliance"
    ETHICAL = "ethical"
    ACCESSIBILITY = "accessibility"
    PRIVACY = "privacy"

@dataclass
class ValidationFinding:
    """A single validation finding"""
    severity: FindingSeverity
    category: FindingCategory
    title: str
    description: str
    location: str
    remediation: str
    confidence: float

@dataclass
class OutputValidationResult:
    """Result of output validation"""
    is_valid: bool
    findings: List[ValidationFinding]
    security_score: float
    compliance_score: float
    overall_confidence: float
    passed_checks: int
    failed_checks: int
    warnings: List[str]

class OutputValidator:
    """Comprehensive output validation system"""
    
    # Credential patterns
    CREDENTIAL_PATTERNS = {
        'aws_access_key': r'AKIA[0-9A-Z]{16}',
        'aws_secret_key': r'[A-Za-z0-9/+=]{40}',
        'generic_api_key': r'api[_-]?key["\']?\s*[:=]\s*["\']?[A-Za-z0-9]{20,}',
        'password': r'password["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',
        'private_key': r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
        'jwt_token': r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]+',
        'github_token': r'gh[pousr]_[A-Za-z0-9]{36}',
        'slack_token': r'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9]{24,}',
    }
    
    # IAM policy issues
    IAM_ISSUES = {
        'wildcard_resource': r'"Resource"\s*:\s*"\*"',
        'wildcard_action': r'"Action"\s*:\s*"\*"',
        'admin_policy': r'arn:aws:iam::aws:policy/AdministratorAccess',
        'full_access': r'"Action"\s*:\s*"[^"]+:\*"',
        'no_condition': r'"Effect"\s*:\s*"Allow"(?!.*"Condition")',
    }
    
    # Security issues
    SECURITY_ISSUES = {
        'public_access': r'(PubliclyAccessible|public-read|public-read-write)',
        'no_encryption': r'(Encrypted\s*[:=]\s*false|encryption\s*[:=]\s*false)',
        'insecure_protocol': r'(http://|ftp://)',
        'weak_cipher': r'(SSLv3|TLSv1\.0|TLSv1\.1|DES|RC4)',
        'sql_injection_risk': r'(execute\s*\(.*\+|query\s*\(.*\+|raw\s*\()',
        'command_injection_risk': r'(os\.system|subprocess\.call|shell\s*=\s*True)',
        'xxe_risk': r'(XMLParser|etree\.parse)(?!.*resolve_entities\s*=\s*False)',
    }
    
    # Error handling patterns
    ERROR_HANDLING_PATTERNS = {
        'bare_except': r'except\s*:',
        'pass_in_except': r'except.*:\s*pass',
        'no_logging': r'except.*:(?!.*log)',
        'generic_exception': r'except\s+Exception\s*:',
    }
    
    # Cost control patterns
    COST_CONTROL_PATTERNS = {
        'no_timeout': r'(Lambda|Function)(?!.*Timeout)',
        'no_memory_limit': r'(Lambda|Function)(?!.*MemorySize)',
        'no_reserved_concurrency': r'Lambda(?!.*ReservedConcurrentExecutions)',
        'no_lifecycle_policy': r'S3.*Bucket(?!.*LifecycleConfiguration)',
        'no_auto_scaling': r'(DynamoDB|ECS)(?!.*AutoScaling)',
    }
    
    # Ethical and safety patterns
    ETHICAL_CONCERNS = {
        'surveillance_keywords': r'(track|monitor|spy|surveillance|location.*tracking|facial.*recognition)',
        'discrimination_risk': r'(race|ethnicity|gender|age|religion).*(?:filter|score|rank|classify)',
        'manipulation_patterns': r'(dark.*pattern|manipulat|addict|exploit.*behavior)',
        'privacy_violation': r'(scrape|harvest).*(?:email|phone|personal|data)',
        'harmful_content': r'(weapon|violence|self.*harm|suicide|illegal)',
    }
    
    # Accessibility patterns
    ACCESSIBILITY_ISSUES = {
        'no_alt_text': r'<img(?!.*alt=)',
        'no_aria_labels': r'(button|input|select)(?!.*aria-label)',
        'color_only_info': r'color.*(?:indicate|show|display)(?!.*text|label)',
    }
    
    def __init__(self):
        self.findings: List[ValidationFinding] = []
    
    def validate(self, output: str, output_type: str = "code") -> OutputValidationResult:
        """
        Validate AI-generated output
        
        Args:
            output: The generated output to validate
            output_type: Type of output (code, config, documentation)
            
        Returns:
            OutputValidationResult with all findings
        """
        self.findings = []
        
        # Run all validation checks
        self._check_credentials(output)
        self._check_iam_policies(output)
        self._check_security_issues(output)
        self._check_error_handling(output)
        self._check_cost_controls(output)
        self._check_best_practices(output)
        self._check_ethical_concerns(output)
        self._check_accessibility(output)
        self._check_privacy_compliance(output)
        
        # Calculate scores
        security_score = self._calculate_security_score()
        compliance_score = self._calculate_compliance_score()
        overall_confidence = self._calculate_overall_confidence()
        
        # Count checks
        passed_checks = len([f for f in self.findings if f.severity in [FindingSeverity.LOW, FindingSeverity.INFO]])
        failed_checks = len([f for f in self.findings if f.severity in [FindingSeverity.CRITICAL, FindingSeverity.HIGH]])
        
        # Determine if valid
        is_valid = failed_checks == 0 and security_score >= 0.7
        
        # Generate warnings
        warnings = [f.title for f in self.findings if f.severity == FindingSeverity.HIGH]
        
        return OutputValidationResult(
            is_valid=is_valid,
            findings=self.findings,
            security_score=security_score,
            compliance_score=compliance_score,
            overall_confidence=overall_confidence,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            warnings=warnings
        )
    
    def _check_credentials(self, output: str):
        """Check for hardcoded credentials"""
        for cred_type, pattern in self.CREDENTIAL_PATTERNS.items():
            matches = re.finditer(pattern, output, re.IGNORECASE)
            for match in matches:
                self.findings.append(ValidationFinding(
                    severity=FindingSeverity.CRITICAL,
                    category=FindingCategory.CREDENTIALS,
                    title=f"Hardcoded {cred_type} detected",
                    description=f"Found potential {cred_type} in output: {match.group()[:20]}...",
                    location=f"Position {match.start()}-{match.end()}",
                    remediation="Use environment variables or AWS Secrets Manager for credentials",
                    confidence=0.9
                ))
    
    def _check_iam_policies(self, output: str):
        """Check IAM policies for security issues"""
        # Check for wildcard resources
        if re.search(self.IAM_ISSUES['wildcard_resource'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.HIGH,
                category=FindingCategory.IAM_POLICY,
                title="Wildcard resource in IAM policy",
                description="IAM policy uses '*' for Resource, violating least privilege",
                location="IAM Policy",
                remediation="Specify exact ARNs for resources instead of using wildcards",
                confidence=0.95
            ))
        
        # Check for wildcard actions
        if re.search(self.IAM_ISSUES['wildcard_action'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.HIGH,
                category=FindingCategory.IAM_POLICY,
                title="Wildcard action in IAM policy",
                description="IAM policy uses '*' for Action, granting excessive permissions",
                location="IAM Policy",
                remediation="Specify exact actions needed instead of using wildcards",
                confidence=0.95
            ))
        
        # Check for admin policy
        if re.search(self.IAM_ISSUES['admin_policy'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.CRITICAL,
                category=FindingCategory.IAM_POLICY,
                title="AdministratorAccess policy attached",
                description="Using AdministratorAccess policy violates least privilege principle",
                location="IAM Policy",
                remediation="Create custom policy with only required permissions",
                confidence=1.0
            ))
    
    def _check_security_issues(self, output: str):
        """Check for security vulnerabilities"""
        # Public access
        if re.search(self.SECURITY_ISSUES['public_access'], output, re.IGNORECASE):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.HIGH,
                category=FindingCategory.SECURITY,
                title="Public access configuration detected",
                description="Resource configured with public access",
                location="Resource Configuration",
                remediation="Restrict access to specific IPs or VPC endpoints",
                confidence=0.85
            ))
        
        # No encryption
        if re.search(self.SECURITY_ISSUES['no_encryption'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.HIGH,
                category=FindingCategory.SECURITY,
                title="Encryption disabled",
                description="Resource configured without encryption",
                location="Resource Configuration",
                remediation="Enable encryption at rest and in transit",
                confidence=0.9
            ))
        
        # SQL injection risk
        if re.search(self.SECURITY_ISSUES['sql_injection_risk'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.CRITICAL,
                category=FindingCategory.SECURITY,
                title="SQL injection vulnerability",
                description="String concatenation in SQL query detected",
                location="Code",
                remediation="Use parameterized queries or ORM",
                confidence=0.8
            ))
        
        # Command injection risk
        if re.search(self.SECURITY_ISSUES['command_injection_risk'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.CRITICAL,
                category=FindingCategory.SECURITY,
                title="Command injection vulnerability",
                description="Unsafe command execution detected",
                location="Code",
                remediation="Avoid shell=True, validate and sanitize all inputs",
                confidence=0.85
            ))
    
    def _check_error_handling(self, output: str):
        """Check error handling patterns"""
        # Bare except
        if re.search(self.ERROR_HANDLING_PATTERNS['bare_except'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.MEDIUM,
                category=FindingCategory.ERROR_HANDLING,
                title="Bare except clause",
                description="Using bare 'except:' catches all exceptions including system exits",
                location="Code",
                remediation="Catch specific exceptions or use 'except Exception:'",
                confidence=0.95
            ))
        
        # Pass in except
        if re.search(self.ERROR_HANDLING_PATTERNS['pass_in_except'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.MEDIUM,
                category=FindingCategory.ERROR_HANDLING,
                title="Silent exception handling",
                description="Exception caught but not logged or handled",
                location="Code",
                remediation="Log exceptions and handle appropriately",
                confidence=0.9
            ))
    
    def _check_cost_controls(self, output: str):
        """Check for cost control measures"""
        # No timeout on Lambda
        if 'Lambda' in output and not re.search(r'Timeout\s*[:=]', output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.MEDIUM,
                category=FindingCategory.COST_CONTROL,
                title="No timeout configured",
                description="Lambda function without timeout can incur unexpected costs",
                location="Lambda Configuration",
                remediation="Set appropriate timeout value (e.g., 30 seconds)",
                confidence=0.8
            ))
        
        # No lifecycle policy on S3
        if 'S3' in output and 'Bucket' in output and not re.search(r'LifecycleConfiguration', output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.LOW,
                category=FindingCategory.COST_CONTROL,
                title="No S3 lifecycle policy",
                description="S3 bucket without lifecycle policy may accumulate unnecessary costs",
                location="S3 Configuration",
                remediation="Configure lifecycle policy to transition or expire old objects",
                confidence=0.7
            ))
    
    def _check_best_practices(self, output: str):
        """Check for AWS best practices"""
        # Check for logging
        if 'Lambda' in output and not re.search(r'(logging|logger|log)', output, re.IGNORECASE):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.LOW,
                category=FindingCategory.BEST_PRACTICE,
                title="No logging configured",
                description="Code lacks logging for debugging and monitoring",
                location="Code",
                remediation="Add logging statements for key operations",
                confidence=0.75
            ))
        
        # Check for monitoring
        if not re.search(r'(CloudWatch|Metric|Alarm)', output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.LOW,
                category=FindingCategory.BEST_PRACTICE,
                title="No monitoring configured",
                description="No CloudWatch monitoring or alarms configured",
                location="Configuration",
                remediation="Add CloudWatch metrics and alarms for key operations",
                confidence=0.7
            ))
    
    def _check_ethical_concerns(self, output: str):
        """Check for ethical concerns and potential misuse"""
        output_lower = output.lower()
        
        # Check for surveillance patterns
        if re.search(self.ETHICAL_CONCERNS['surveillance_keywords'], output_lower):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.HIGH,
                category=FindingCategory.COMPLIANCE,
                title="Potential surveillance or tracking functionality",
                description="Code contains patterns that could enable surveillance or invasive tracking",
                location="Code",
                remediation="Ensure user consent, transparency, and compliance with privacy laws. Implement opt-in mechanisms and data minimization.",
                confidence=0.75
            ))
        
        # Check for discrimination risk
        if re.search(self.ETHICAL_CONCERNS['discrimination_risk'], output_lower):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.CRITICAL,
                category=FindingCategory.COMPLIANCE,
                title="Potential discrimination risk",
                description="Code contains patterns that could enable discrimination based on protected characteristics",
                location="Code",
                remediation="Remove discriminatory logic. Ensure algorithmic fairness and bias testing. Consult legal and ethics teams.",
                confidence=0.85
            ))
        
        # Check for manipulation patterns
        if re.search(self.ETHICAL_CONCERNS['manipulation_patterns'], output_lower):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.HIGH,
                category=FindingCategory.COMPLIANCE,
                title="Potential manipulative or dark patterns",
                description="Code may implement manipulative user experience patterns",
                location="Code",
                remediation="Remove dark patterns. Ensure transparent, user-friendly design that respects user autonomy.",
                confidence=0.70
            ))
        
        # Check for privacy violations
        if re.search(self.ETHICAL_CONCERNS['privacy_violation'], output_lower):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.CRITICAL,
                category=FindingCategory.COMPLIANCE,
                title="Potential privacy violation",
                description="Code may scrape or harvest personal data without consent",
                location="Code",
                remediation="Ensure explicit user consent, comply with GDPR/CCPA, implement data minimization.",
                confidence=0.80
            ))
        
        # Check for harmful content
        if re.search(self.ETHICAL_CONCERNS['harmful_content'], output_lower):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.CRITICAL,
                category=FindingCategory.COMPLIANCE,
                title="Potential harmful content or illegal activity",
                description="Code references potentially harmful or illegal content",
                location="Code",
                remediation="Review content policies. Implement content moderation. Ensure compliance with laws and platform policies.",
                confidence=0.90
            ))
    
    def _check_accessibility(self, output: str):
        """Check for accessibility issues"""
        output_lower = output.lower()
        
        # Check for images without alt text
        if re.search(self.ACCESSIBILITY_ISSUES['no_alt_text'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.MEDIUM,
                category=FindingCategory.BEST_PRACTICE,
                title="Images without alt text",
                description="Images lack alternative text for screen readers",
                location="HTML/UI Code",
                remediation="Add descriptive alt text to all images for accessibility (WCAG 2.1 Level A)",
                confidence=0.90
            ))
        
        # Check for interactive elements without ARIA labels
        if re.search(self.ACCESSIBILITY_ISSUES['no_aria_labels'], output):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.MEDIUM,
                category=FindingCategory.BEST_PRACTICE,
                title="Interactive elements without ARIA labels",
                description="Buttons or inputs lack ARIA labels for screen readers",
                location="HTML/UI Code",
                remediation="Add aria-label or aria-labelledby to all interactive elements (WCAG 2.1 Level A)",
                confidence=0.85
            ))
        
        # Check for color-only information
        if re.search(self.ACCESSIBILITY_ISSUES['color_only_info'], output_lower):
            self.findings.append(ValidationFinding(
                severity=FindingSeverity.MEDIUM,
                category=FindingCategory.BEST_PRACTICE,
                title="Information conveyed by color only",
                description="Information may be conveyed by color alone, inaccessible to colorblind users",
                location="UI Code",
                remediation="Use text labels, patterns, or icons in addition to color (WCAG 2.1 Level A)",
                confidence=0.70
            ))
    
    def _check_privacy_compliance(self, output: str):
        """Check for privacy and data protection compliance"""
        output_lower = output.lower()
        
        # Check for PII handling without encryption
        if re.search(r'(email|phone|ssn|credit.*card|passport)', output_lower):
            if not re.search(r'(encrypt|hash|kms)', output_lower):
                self.findings.append(ValidationFinding(
                    severity=FindingSeverity.HIGH,
                    category=FindingCategory.COMPLIANCE,
                    title="PII handled without encryption",
                    description="Personally Identifiable Information (PII) may be stored or transmitted without encryption",
                    location="Code",
                    remediation="Encrypt PII at rest (AWS KMS) and in transit (TLS). Implement data minimization and retention policies.",
                    confidence=0.85
                ))
        
        # Check for data retention policy
        if re.search(r'(store|save|persist).*data', output_lower):
            if not re.search(r'(retention|ttl|expir|delete)', output_lower):
                self.findings.append(ValidationFinding(
                    severity=FindingSeverity.MEDIUM,
                    category=FindingCategory.COMPLIANCE,
                    title="No data retention policy",
                    description="Data storage without retention or deletion policy may violate GDPR/CCPA",
                    location="Code/Configuration",
                    remediation="Implement data retention policies with automatic deletion. Document retention periods.",
                    confidence=0.75
                ))
        
        # Check for user consent mechanisms
        if re.search(r'(collect|track|analytics|cookie)', output_lower):
            if not re.search(r'(consent|opt.*in|permission|agree)', output_lower):
                self.findings.append(ValidationFinding(
                    severity=FindingSeverity.HIGH,
                    category=FindingCategory.COMPLIANCE,
                    title="Data collection without consent mechanism",
                    description="Data collection or tracking without explicit user consent violates GDPR/CCPA",
                    location="Code",
                    remediation="Implement explicit consent mechanisms (opt-in). Provide clear privacy policy and data usage information.",
                    confidence=0.80
                ))
    
    def _calculate_security_score(self) -> float:
        """Calculate security score based on findings"""
        if not self.findings:
            return 1.0
        
        severity_weights = {
            FindingSeverity.CRITICAL: 0.4,
            FindingSeverity.HIGH: 0.25,
            FindingSeverity.MEDIUM: 0.15,
            FindingSeverity.LOW: 0.05,
            FindingSeverity.INFO: 0.0
        }
        
        total_penalty = sum(severity_weights.get(f.severity, 0) for f in self.findings)
        return max(0.0, 1.0 - total_penalty)
    
    def _calculate_compliance_score(self) -> float:
        """Calculate compliance score"""
        security_findings = [f for f in self.findings if f.category == FindingCategory.SECURITY]
        iam_findings = [f for f in self.findings if f.category == FindingCategory.IAM_POLICY]
        
        critical_findings = len([f for f in security_findings + iam_findings if f.severity == FindingSeverity.CRITICAL])
        
        if critical_findings > 0:
            return 0.0
        
        high_findings = len([f for f in security_findings + iam_findings if f.severity == FindingSeverity.HIGH])
        
        return max(0.0, 1.0 - (high_findings * 0.2))
    
    def _calculate_overall_confidence(self) -> float:
        """Calculate overall confidence in the output"""
        if not self.findings:
            return 1.0
        
        # Average confidence of all findings
        avg_confidence = sum(f.confidence for f in self.findings) / len(self.findings)
        
        # Adjust based on severity
        critical_count = len([f for f in self.findings if f.severity == FindingSeverity.CRITICAL])
        high_count = len([f for f in self.findings if f.severity == FindingSeverity.HIGH])
        
        confidence_penalty = (critical_count * 0.3) + (high_count * 0.15)
        
        return max(0.0, min(1.0, avg_confidence - confidence_penalty))
