#!/usr/bin/env python3
"""
Multi-Layer Input Validation System
Comprehensive input validation with injection detection, sanitization, and filtering
"""

import re
import logging
import html
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ValidationLevel(Enum):
    """Validation strictness levels"""
    PERMISSIVE = "permissive"
    STANDARD = "standard"
    STRICT = "strict"
    PARANOID = "paranoid"

class ThreatType(Enum):
    """Types of security threats"""
    PROMPT_INJECTION = "prompt_injection"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    COMMAND_INJECTION = "command_injection"
    PATH_TRAVERSAL = "path_traversal"
    MALICIOUS_PATTERN = "malicious_pattern"

@dataclass
class ValidationResult:
    """Result of input validation"""
    is_valid: bool
    sanitized_input: str
    threats_detected: List[ThreatType]
    warnings: List[str]
    confidence_score: float
    original_input: str

class InputValidator:
    """Multi-layer input validation system"""
    
    # Prompt injection patterns
    PROMPT_INJECTION_PATTERNS = [
        r'ignore\s+(previous|above|all)\s+instructions',
        r'disregard\s+(previous|above|all)\s+instructions',
        r'forget\s+(previous|above|all)\s+instructions',
        r'system\s*:\s*you\s+are',
        r'new\s+instructions\s*:',
        r'override\s+instructions',
        r'act\s+as\s+if',
        r'pretend\s+you\s+are',
        r'roleplay\s+as',
        r'simulate\s+being',
        r'</system>',
        r'<\|im_start\|>',
        r'<\|im_end\|>',
        r'\[INST\]',
        r'\[/INST\]',
    ]
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r"('\s*OR\s+'1'\s*=\s*'1)",
        r"('\s*OR\s+1\s*=\s*1)",
        r'(--\s*$)',
        r'(;\s*DROP\s+TABLE)',
        r'(;\s*DELETE\s+FROM)',
        r'(UNION\s+SELECT)',
        r'(INSERT\s+INTO)',
        r'(UPDATE\s+.*\s+SET)',
    ]
    
    # Command injection patterns
    COMMAND_INJECTION_PATTERNS = [
        r'[;&|`$]',
        r'\$\(',
        r'`.*`',
        r'\|\s*bash',
        r'\|\s*sh',
        r'>\s*/dev/',
        r'<\s*/dev/',
    ]
    
    # Path traversal patterns
    PATH_TRAVERSAL_PATTERNS = [
        r'\.\./\.\.',
        r'\.\.\\\.\.', 
        r'/etc/passwd',
        r'/etc/shadow',
        r'C:\\Windows',
        r'%2e%2e',
    ]
    
    # XSS patterns
    XSS_PATTERNS = [
        r'<script[^>]*>',
        r'javascript:',
        r'onerror\s*=',
        r'onload\s*=',
        r'onclick\s*=',
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>',
    ]
    
    # Malicious patterns
    MALICIOUS_PATTERNS = [
        r'eval\s*\(',
        r'exec\s*\(',
        r'__import__\s*\(',
        r'compile\s*\(',
        r'os\.system',
        r'subprocess\.',
        r'shell\s*=\s*True',
    ]
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.STANDARD):
        self.validation_level = validation_level
        self.max_input_length = self._get_max_length()
    
    def _get_max_length(self) -> int:
        """Get maximum input length based on validation level"""
        length_map = {
            ValidationLevel.PERMISSIVE: 50000,
            ValidationLevel.STANDARD: 10000,
            ValidationLevel.STRICT: 5000,
            ValidationLevel.PARANOID: 2000
        }
        return length_map[self.validation_level]
    
    def validate(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Perform multi-layer validation on user input
        
        Args:
            user_input: Raw user input to validate
            context: Optional context for validation decisions
            
        Returns:
            ValidationResult with validation status and sanitized input
        """
        threats_detected = []
        warnings = []
        
        # Layer 1: Length validation
        if len(user_input) > self.max_input_length:
            warnings.append(f"Input exceeds maximum length ({self.max_input_length} chars)")
            user_input = user_input[:self.max_input_length]
        
        # Layer 2: Character encoding validation
        try:
            user_input.encode('utf-8')
        except UnicodeEncodeError:
            warnings.append("Invalid character encoding detected")
            user_input = user_input.encode('utf-8', errors='ignore').decode('utf-8')
        
        # Layer 3: Prompt injection detection
        if self._detect_prompt_injection(user_input):
            threats_detected.append(ThreatType.PROMPT_INJECTION)
            logger.warning("Prompt injection attempt detected")
        
        # Layer 4: SQL injection detection
        if self._detect_sql_injection(user_input):
            threats_detected.append(ThreatType.SQL_INJECTION)
            logger.warning("SQL injection attempt detected")
        
        # Layer 5: Command injection detection
        if self._detect_command_injection(user_input):
            threats_detected.append(ThreatType.COMMAND_INJECTION)
            logger.warning("Command injection attempt detected")
        
        # Layer 6: Path traversal detection
        if self._detect_path_traversal(user_input):
            threats_detected.append(ThreatType.PATH_TRAVERSAL)
            logger.warning("Path traversal attempt detected")
        
        # Layer 7: XSS detection
        if self._detect_xss(user_input):
            threats_detected.append(ThreatType.XSS)
            logger.warning("XSS attempt detected")
        
        # Layer 8: Malicious pattern detection
        if self._detect_malicious_patterns(user_input):
            threats_detected.append(ThreatType.MALICIOUS_PATTERN)
            logger.warning("Malicious pattern detected")
        
        # Layer 9: Sanitization
        sanitized_input = self._sanitize_input(user_input, threats_detected)
        
        # Layer 10: Final validation
        is_valid = len(threats_detected) == 0 or self.validation_level == ValidationLevel.PERMISSIVE
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(threats_detected, warnings)
        
        return ValidationResult(
            is_valid=is_valid,
            sanitized_input=sanitized_input,
            threats_detected=threats_detected,
            warnings=warnings,
            confidence_score=confidence_score,
            original_input=user_input
        )
    
    def _detect_prompt_injection(self, text: str) -> bool:
        """Detect prompt injection attempts"""
        text_lower = text.lower()
        for pattern in self.PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        return False
    
    def _detect_sql_injection(self, text: str) -> bool:
        """Detect SQL injection attempts"""
        for pattern in self.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _detect_command_injection(self, text: str) -> bool:
        """Detect command injection attempts"""
        for pattern in self.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, text):
                return True
        return False
    
    def _detect_path_traversal(self, text: str) -> bool:
        """Detect path traversal attempts"""
        for pattern in self.PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _detect_xss(self, text: str) -> bool:
        """Detect XSS attempts"""
        for pattern in self.XSS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _detect_malicious_patterns(self, text: str) -> bool:
        """Detect malicious code patterns"""
        for pattern in self.MALICIOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _sanitize_input(self, text: str, threats: List[ThreatType]) -> str:
        """Sanitize input based on detected threats"""
        sanitized = text
        
        # HTML escape for XSS protection
        if ThreatType.XSS in threats:
            sanitized = html.escape(sanitized)
        
        # Remove dangerous characters for command injection
        if ThreatType.COMMAND_INJECTION in threats:
            sanitized = re.sub(r'[;&|`$]', '', sanitized)
        
        # Normalize path separators for path traversal
        if ThreatType.PATH_TRAVERSAL in threats:
            sanitized = sanitized.replace('..', '')
        
        # Remove SQL keywords for SQL injection
        if ThreatType.SQL_INJECTION in threats:
            sql_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'UNION', 'SELECT']
            for keyword in sql_keywords:
                sanitized = re.sub(rf'\b{keyword}\b', '', sanitized, flags=re.IGNORECASE)
        
        # Strip whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    def _calculate_confidence(self, threats: List[ThreatType], warnings: List[str]) -> float:
        """Calculate confidence score based on validation results"""
        base_confidence = 1.0
        
        # Reduce confidence for each threat
        threat_penalty = {
            ThreatType.PROMPT_INJECTION: 0.3,
            ThreatType.SQL_INJECTION: 0.4,
            ThreatType.COMMAND_INJECTION: 0.5,
            ThreatType.PATH_TRAVERSAL: 0.3,
            ThreatType.XSS: 0.3,
            ThreatType.MALICIOUS_PATTERN: 0.4
        }
        
        for threat in threats:
            base_confidence -= threat_penalty.get(threat, 0.2)
        
        # Reduce confidence for warnings
        base_confidence -= len(warnings) * 0.05
        
        return max(0.0, min(1.0, base_confidence))
    
    def validate_batch(self, inputs: List[str]) -> List[ValidationResult]:
        """Validate multiple inputs"""
        return [self.validate(inp) for inp in inputs]


class ContextualValidator:
    """Context-aware validation for specific use cases"""
    
    def __init__(self):
        self.base_validator = InputValidator(ValidationLevel.STANDARD)
    
    def validate_aws_resource_name(self, name: str) -> ValidationResult:
        """Validate AWS resource names"""
        # AWS resource name constraints
        if not re.match(r'^[a-zA-Z0-9-_]+$', name):
            return ValidationResult(
                is_valid=False,
                sanitized_input=re.sub(r'[^a-zA-Z0-9-_]', '', name),
                threats_detected=[],
                warnings=["Invalid characters for AWS resource name"],
                confidence_score=0.5,
                original_input=name
            )
        
        if len(name) > 255:
            return ValidationResult(
                is_valid=False,
                sanitized_input=name[:255],
                threats_detected=[],
                warnings=["Name exceeds AWS maximum length"],
                confidence_score=0.6,
                original_input=name
            )
        
        return ValidationResult(
            is_valid=True,
            sanitized_input=name,
            threats_detected=[],
            warnings=[],
            confidence_score=1.0,
            original_input=name
        )
    
    def validate_code_snippet(self, code: str) -> ValidationResult:
        """Validate code snippets for dangerous patterns"""
        result = self.base_validator.validate(code)
        
        # Additional code-specific checks
        dangerous_imports = ['os', 'subprocess', 'eval', 'exec', '__import__']
        for dangerous in dangerous_imports:
            if dangerous in code:
                result.warnings.append(f"Potentially dangerous: {dangerous}")
                result.confidence_score *= 0.9
        
        return result
    
    def validate_configuration(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate configuration dictionaries"""
        config_str = str(config)
        result = self.base_validator.validate(config_str)
        
        # Check for sensitive keys
        sensitive_keys = ['password', 'secret', 'key', 'token', 'credential']
        for key in config.keys():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                result.warnings.append(f"Sensitive configuration key detected: {key}")
        
        return result
