#!/usr/bin/env python3
"""
Production Readiness Test Suite
Runs 1,000 comprehensive tests on each agent component to ensure production readiness
"""

import asyncio
import sys
import os
import time
import random
import string
from typing import Dict, List, Any
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.strands_builder_integration import (
    StrandsBuilderIntegration,
    RequirementsTranslator,
    StrandsAgentGenerator,
    AgentValidator,
    StrandsSpecification,
    StrandsCapability,
    ValidationStatus
)


class ProductionReadinessTestSuite:
    """Comprehensive production readiness test suite"""
    
    def __init__(self):
        self.results = defaultdict(list)
        self.start_time = None
        self.end_time = None
        
    def generate_random_string(self, length: int = 10) -> str:
        """Generate random string for testing"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def generate_test_requirements(self, variation: int = 0) -> Dict[str, Any]:
        """Generate varied test requirements"""
        use_cases = ['chatbot', 'api_backend', 'data_processing', 'web_application', 'automation']
        aws_services_options = [
            ['lambda', 'bedrock', 'dynamodb'],
            ['lambda', 'api_gateway', 's3'],
            ['lambda', 's3', 'dynamodb', 'glue'],
            ['ecs_fargate', 'rds', 'elasticache'],
            ['lambda', 'bedrock', 'dynamodb', 'api_gateway', 's3']
        ]
        mcp_options = [
            ['aws_ai_ml', 'aws_serverless'],
            ['aws_serverless', 'aws_networking'],
            ['aws_documentation', 'aws_well_architected'],
            ['aws_ai_ml', 'aws_serverless', 'strands_patterns'],
            ['aws_security', 'aws_monitoring']
        ]
        
        use_case = use_cases[variation % len(use_cases)]
        aws_services = aws_services_options[variation % len(aws_services_options)]
        mcps = mcp_options[variation % len(mcp_options)]
        
        return {
            'name': f'test-agent-{variation}-{self.generate_random_string(5)}',
            'use_case': use_case,
            'description': f'Test agent {variation} for {use_case}',
            'aws_services': aws_services,
            'mcps': mcps,
            'environment_variables': {
                'TEST_VAR': f'value_{variation}',
                'ITERATION': str(variation)
            },
            'deployment_config': {
                'platform': 'aws',
                'compute': 'lambda',
                'memory': 512 + (variation % 5) * 256,
                'timeout': 60 + (variation % 10) * 30
            }
        }
    
    async def test_requirements_translator(self, iterations: int = 1000) -> Dict[str, Any]:
        """Test RequirementsTranslator with 1000 iterations"""
        print(f"\n🧪 Testing RequirementsTranslator ({iterations} iterations)...")
        
        translator = RequirementsTranslator()
        passed = 0
        failed = 0
        errors = []
        times = []
        
        for i in range(iterations):
            try:
                start = time.time()
                requirements = self.generate_test_requirements(i)
                spec = await translator.translate_to_strands_format(requirements)
                elapsed = time.time() - start
                times.append(elapsed)
                
                # Validate translation
                assert spec.name == requirements['name']
                assert spec.description == requirements['description']
                assert len(spec.capabilities) > 0
                assert len(spec.tools) > 0
                assert len(spec.aws_services) > 0
                
                passed += 1
                
                if (i + 1) % 100 == 0:
                    print(f"  Progress: {i + 1}/{iterations} ({passed} passed)")
                    
            except Exception as e:
                failed += 1
                errors.append(f"Iteration {i}: {str(e)}")
                if len(errors) <= 5:  # Only store first 5 errors
                    self.results['translator_errors'].append(str(e))
        
        avg_time = sum(times) / len(times) if times else 0
        min_time = min(times) if times else 0
        max_time = max(times) if times else 0
        
        result = {
            'component': 'RequirementsTranslator',
            'total_tests': iterations,
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / iterations) * 100,
            'avg_time_ms': avg_time * 1000,
            'min_time_ms': min_time * 1000,
            'max_time_ms': max_time * 1000,
            'errors': errors[:5]  # First 5 errors
        }
        
        self.results['translator'] = result
        return result
    
    async def test_agent_generator(self, iterations: int = 1000) -> Dict[str, Any]:
        """Test StrandsAgentGenerator with 1000 iterations"""
        print(f"\n🧪 Testing StrandsAgentGenerator ({iterations} iterations)...")
        
        translator = RequirementsTranslator()
        generator = StrandsAgentGenerator()
        passed = 0
        failed = 0
        errors = []
        times = []
        
        for i in range(iterations):
            try:
                start = time.time()
                requirements = self.generate_test_requirements(i)
                spec = await translator.translate_to_strands_format(requirements)
                agent = await generator.generate_agent(spec)
                elapsed = time.time() - start
                times.append(elapsed)
                
                # Validate generation
                assert agent.name == spec.name
                assert len(agent.code_files) >= 5
                assert len(agent.config_files) >= 4
                assert agent.documentation is not None
                assert 'agent.py' in agent.code_files
                assert 'config.yaml' in agent.config_files
                
                passed += 1
                
                if (i + 1) % 100 == 0:
                    print(f"  Progress: {i + 1}/{iterations} ({passed} passed)")
                    
            except Exception as e:
                failed += 1
                errors.append(f"Iteration {i}: {str(e)}")
                if len(errors) <= 5:
                    self.results['generator_errors'].append(str(e))
        
        avg_time = sum(times) / len(times) if times else 0
        min_time = min(times) if times else 0
        max_time = max(times) if times else 0
        
        result = {
            'component': 'StrandsAgentGenerator',
            'total_tests': iterations,
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / iterations) * 100,
            'avg_time_ms': avg_time * 1000,
            'min_time_ms': min_time * 1000,
            'max_time_ms': max_time * 1000,
            'errors': errors[:5]
        }
        
        self.results['generator'] = result
        return result
    
    async def test_agent_validator(self, iterations: int = 1000) -> Dict[str, Any]:
        """Test AgentValidator with 1000 iterations"""
        print(f"\n🧪 Testing AgentValidator ({iterations} iterations)...")
        
        translator = RequirementsTranslator()
        generator = StrandsAgentGenerator()
        validator = AgentValidator()
        passed = 0
        failed = 0
        errors = []
        times = []
        confidence_scores = []
        
        for i in range(iterations):
            try:
                start = time.time()
                requirements = self.generate_test_requirements(i)
                spec = await translator.translate_to_strands_format(requirements)
                agent = await generator.generate_agent(spec)
                validation = await validator.validate_agent(agent, requirements)
                elapsed = time.time() - start
                times.append(elapsed)
                
                # Validate validation results
                assert validation.status in [ValidationStatus.PASSED, ValidationStatus.WARNING, ValidationStatus.FAILED]
                assert 0.0 <= validation.confidence_score <= 1.0
                assert isinstance(validation.passed_checks, list)
                assert isinstance(validation.failed_checks, list)
                
                confidence_scores.append(validation.confidence_score)
                passed += 1
                
                if (i + 1) % 100 == 0:
                    avg_conf = sum(confidence_scores) / len(confidence_scores)
                    print(f"  Progress: {i + 1}/{iterations} ({passed} passed, avg confidence: {avg_conf:.2f})")
                    
            except Exception as e:
                failed += 1
                errors.append(f"Iteration {i}: {str(e)}")
                if len(errors) <= 5:
                    self.results['validator_errors'].append(str(e))
        
        avg_time = sum(times) / len(times) if times else 0
        min_time = min(times) if times else 0
        max_time = max(times) if times else 0
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        min_confidence = min(confidence_scores) if confidence_scores else 0
        max_confidence = max(confidence_scores) if confidence_scores else 0
        
        result = {
            'component': 'AgentValidator',
            'total_tests': iterations,
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / iterations) * 100,
            'avg_time_ms': avg_time * 1000,
            'min_time_ms': min_time * 1000,
            'max_time_ms': max_time * 1000,
            'avg_confidence': avg_confidence,
            'min_confidence': min_confidence,
            'max_confidence': max_confidence,
            'errors': errors[:5]
        }
        
        self.results['validator'] = result
        return result
    
    async def test_full_integration(self, iterations: int = 1000) -> Dict[str, Any]:
        """Test full StrandsBuilderIntegration with 1000 iterations"""
        print(f"\n🧪 Testing StrandsBuilderIntegration (Full Pipeline) ({iterations} iterations)...")
        
        integration = StrandsBuilderIntegration()
        passed = 0
        failed = 0
        errors = []
        times = []
        confidence_scores = []
        
        for i in range(iterations):
            try:
                start = time.time()
                requirements = self.generate_test_requirements(i)
                result = await integration.create_agent_from_requirements(requirements)
                elapsed = time.time() - start
                times.append(elapsed)
                
                # Validate full pipeline
                assert result['status'] == 'success'
                assert 'agent' in result
                assert 'validation' in result
                
                agent = result['agent']
                validation = result['validation']
                
                assert len(agent['code_files']) >= 5
                assert len(agent['config_files']) >= 4
                assert validation['confidence_score'] >= 0.0
                
                confidence_scores.append(validation['confidence_score'])
                passed += 1
                
                if (i + 1) % 100 == 0:
                    avg_conf = sum(confidence_scores) / len(confidence_scores)
                    print(f"  Progress: {i + 1}/{iterations} ({passed} passed, avg confidence: {avg_conf:.2f})")
                    
            except Exception as e:
                failed += 1
                errors.append(f"Iteration {i}: {str(e)}")
                if len(errors) <= 5:
                    self.results['integration_errors'].append(str(e))
        
        avg_time = sum(times) / len(times) if times else 0
        min_time = min(times) if times else 0
        max_time = max(times) if times else 0
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        min_confidence = min(confidence_scores) if confidence_scores else 0
        max_confidence = max(confidence_scores) if confidence_scores else 0
        
        # Calculate percentiles
        sorted_times = sorted(times)
        p50 = sorted_times[len(sorted_times) // 2] if sorted_times else 0
        p95 = sorted_times[int(len(sorted_times) * 0.95)] if sorted_times else 0
        p99 = sorted_times[int(len(sorted_times) * 0.99)] if sorted_times else 0
        
        result = {
            'component': 'StrandsBuilderIntegration (Full Pipeline)',
            'total_tests': iterations,
            'passed': passed,
            'failed': failed,
            'success_rate': (passed / iterations) * 100,
            'avg_time_ms': avg_time * 1000,
            'min_time_ms': min_time * 1000,
            'max_time_ms': max_time * 1000,
            'p50_time_ms': p50 * 1000,
            'p95_time_ms': p95 * 1000,
            'p99_time_ms': p99 * 1000,
            'avg_confidence': avg_confidence,
            'min_confidence': min_confidence,
            'max_confidence': max_confidence,
            'errors': errors[:5]
        }
        
        self.results['integration'] = result
        return result
    
    async def run_all_tests(self, iterations_per_component: int = 1000):
        """Run all production readiness tests"""
        print("=" * 80)
        print("🚀 PRODUCTION READINESS TEST SUITE")
        print("=" * 80)
        print(f"Running {iterations_per_component} tests per component...")
        print(f"Total tests: {iterations_per_component * 4} = {iterations_per_component * 4:,}")
        print("=" * 80)
        
        self.start_time = time.time()
        
        # Run all component tests
        await self.test_requirements_translator(iterations_per_component)
        await self.test_agent_generator(iterations_per_component)
        await self.test_agent_validator(iterations_per_component)
        await self.test_full_integration(iterations_per_component)
        
        self.end_time = time.time()
        
        # Generate final report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📊 PRODUCTION READINESS TEST REPORT")
        print("=" * 80)
        
        total_time = self.end_time - self.start_time
        total_tests = sum(r['total_tests'] for r in [
            self.results['translator'],
            self.results['generator'],
            self.results['validator'],
            self.results['integration']
        ])
        total_passed = sum(r['passed'] for r in [
            self.results['translator'],
            self.results['generator'],
            self.results['validator'],
            self.results['integration']
        ])
        total_failed = sum(r['failed'] for r in [
            self.results['translator'],
            self.results['generator'],
            self.results['validator'],
            self.results['integration']
        ])
        
        print(f"\n⏱️  Total Execution Time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
        print(f"📈 Total Tests: {total_tests:,}")
        print(f"✅ Total Passed: {total_passed:,}")
        print(f"❌ Total Failed: {total_failed:,}")
        print(f"🎯 Overall Success Rate: {(total_passed/total_tests)*100:.2f}%")
        print(f"⚡ Tests per Second: {total_tests/total_time:.2f}")
        
        # Component-specific results
        for component_key in ['translator', 'generator', 'validator', 'integration']:
            result = self.results[component_key]
            print(f"\n{'─' * 80}")
            print(f"📦 {result['component']}")
            print(f"{'─' * 80}")
            print(f"  Total Tests: {result['total_tests']:,}")
            print(f"  ✅ Passed: {result['passed']:,}")
            print(f"  ❌ Failed: {result['failed']:,}")
            print(f"  🎯 Success Rate: {result['success_rate']:.2f}%")
            print(f"  ⏱️  Avg Time: {result['avg_time_ms']:.2f}ms")
            print(f"  ⚡ Min Time: {result['min_time_ms']:.2f}ms")
            print(f"  🐌 Max Time: {result['max_time_ms']:.2f}ms")
            
            if 'avg_confidence' in result:
                print(f"  📊 Avg Confidence: {result['avg_confidence']:.2f}")
                print(f"  📉 Min Confidence: {result['min_confidence']:.2f}")
                print(f"  📈 Max Confidence: {result['max_confidence']:.2f}")
            
            if 'p50_time_ms' in result:
                print(f"  📊 P50 Time: {result['p50_time_ms']:.2f}ms")
                print(f"  📊 P95 Time: {result['p95_time_ms']:.2f}ms")
                print(f"  📊 P99 Time: {result['p99_time_ms']:.2f}ms")
            
            if result['errors']:
                print(f"  ⚠️  Sample Errors:")
                for error in result['errors'][:3]:
                    print(f"     - {error[:100]}...")
        
        # Production readiness assessment
        print(f"\n{'=' * 80}")
        print("🏆 PRODUCTION READINESS ASSESSMENT")
        print(f"{'=' * 80}")
        
        overall_success_rate = (total_passed / total_tests) * 100
        
        if overall_success_rate >= 99.9:
            status = "✅ EXCELLENT - Production Ready"
            grade = "A+"
        elif overall_success_rate >= 99.0:
            status = "✅ VERY GOOD - Production Ready"
            grade = "A"
        elif overall_success_rate >= 95.0:
            status = "✅ GOOD - Production Ready with Minor Issues"
            grade = "B+"
        elif overall_success_rate >= 90.0:
            status = "⚠️  ACCEPTABLE - Needs Improvement"
            grade = "B"
        else:
            status = "❌ NOT READY - Significant Issues"
            grade = "C"
        
        print(f"\n  Status: {status}")
        print(f"  Grade: {grade}")
        print(f"  Success Rate: {overall_success_rate:.2f}%")
        print(f"  Total Tests Passed: {total_passed:,} / {total_tests:,}")
        
        # Confidence assessment
        if 'integration' in self.results:
            avg_conf = self.results['integration']['avg_confidence']
            if avg_conf >= 0.95:
                conf_status = "✅ EXCELLENT"
            elif avg_conf >= 0.90:
                conf_status = "✅ VERY GOOD"
            elif avg_conf >= 0.80:
                conf_status = "⚠️  GOOD"
            else:
                conf_status = "❌ NEEDS IMPROVEMENT"
            
            print(f"\n  Confidence Assessment: {conf_status}")
            print(f"  Average Confidence: {avg_conf:.2f}")
        
        # Performance assessment
        if 'integration' in self.results:
            avg_time = self.results['integration']['avg_time_ms']
            if avg_time < 100:
                perf_status = "✅ EXCELLENT"
            elif avg_time < 500:
                perf_status = "✅ VERY GOOD"
            elif avg_time < 1000:
                perf_status = "⚠️  ACCEPTABLE"
            else:
                perf_status = "❌ SLOW"
            
            print(f"\n  Performance Assessment: {perf_status}")
            print(f"  Average Pipeline Time: {avg_time:.2f}ms")
        
        print(f"\n{'=' * 80}")
        print("✅ Production Readiness Test Suite Completed!")
        print(f"{'=' * 80}\n")


async def main():
    """Main test execution"""
    suite = ProductionReadinessTestSuite()
    
    # Run 1,000 tests per component (4,000 total tests)
    await suite.run_all_tests(iterations_per_component=1000)


if __name__ == "__main__":
    asyncio.run(main())
