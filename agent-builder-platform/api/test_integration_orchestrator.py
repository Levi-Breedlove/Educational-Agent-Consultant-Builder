#!/usr/bin/env python3
"""
Integration Tests with Orchestrator
Tests end-to-end workflows with the Manager Agent orchestrator
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from api.main import app
from api.models import ExperienceLevel, WorkflowPhase

# Create test client
client = TestClient(app)


class TestOrchestratorIntegration:
    """Test integration with orchestrator"""
    
    def test_complete_workflow_creation(self):
        """Test complete agent creation workflow"""
        print("\n  Testing complete workflow creation...")
        
        # Step 1: Create session
        session_response = client.post("/api/sessions", json={
            "user_id": "integration-test-user",
            "experience_level": "intermediate"
        })
        assert session_response.status_code == 201
        session_id = session_response.json()["session_id"]
        print(f"    ✓ Session created: {session_id}")
        
        # Step 2: Create agent workflow
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "data_processing_pipeline",
            "description": "Build an automated data processing pipeline that ingests CSV files, validates data, and stores results in a database",
            "experience_level": "intermediate"
        })
        assert agent_response.status_code == 201
        agent_data = agent_response.json()
        agent_id = agent_data["agent_id"]
        print(f"    ✓ Agent workflow created: {agent_id}")
        assert agent_data["status"] == "requirements"
        assert agent_data["vector_search_enabled"] == True
        
        # Step 3: Check workflow status
        status_response = client.get(f"/api/agents/{agent_id}/status")
        assert status_response.status_code == 200
        status_data = status_response.json()
        print(f"    ✓ Workflow status: {status_data['current_phase']}")
        assert status_data["progress_percentage"] >= 0
        
        # Step 4: Get recommendations
        rec_response = client.get(f"/api/agents/{agent_id}/recommendations")
        assert rec_response.status_code == 200
        rec_data = rec_response.json()
        print(f"    ✓ Recommendations retrieved (confidence: {rec_data['confidence_score']:.2f})")
        assert rec_data["confidence_score"] > 0.0
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")
        print(f"    ✓ Cleanup completed")
    
    def test_requirements_submission(self):
        """Test submitting requirements to orchestrator"""
        print("\n  Testing requirements submission...")
        
        # Create session and agent
        session_response = client.post("/api/sessions", json={})
        session_id = session_response.json()["session_id"]
        
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "api_gateway",
            "description": "Build a secure API gateway with rate limiting and authentication"
        })
        agent_id = agent_response.json()["agent_id"]
        
        # Submit requirements
        req_response = client.post(f"/api/agents/{agent_id}/requirements", json={
            "session_id": session_id,
            "user_input": "I need the API to handle 1000 requests per second with JWT authentication",
            "context": {
                "budget": "medium",
                "timeline": "1_month"
            }
        })
        assert req_response.status_code == 200
        req_data = req_response.json()
        
        print(f"    ✓ Requirements submitted")
        print(f"    ✓ Confidence score: {req_data['confidence_score']:.2f}")
        assert "use_case_analysis" in req_data
        assert "service_recommendations" in req_data
        assert "cost_analysis" in req_data
        assert req_data["confidence_score"] > 0.0
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")
    
    def test_feedback_processing(self):
        """Test feedback processing through orchestrator"""
        print("\n  Testing feedback processing...")
        
        # Create session and agent
        session_response = client.post("/api/sessions", json={})
        session_id = session_response.json()["session_id"]
        
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "ml_model_deployment",
            "description": "Deploy a machine learning model for real-time predictions"
        })
        agent_id = agent_response.json()["agent_id"]
        
        # Submit feedback
        feedback_response = client.post(f"/api/agents/{agent_id}/feedback", json={
            "session_id": session_id,
            "feedback_type": "clarification",
            "content": "What are the cost implications of using SageMaker vs Lambda?",
            "rating": 4
        })
        assert feedback_response.status_code == 200
        feedback_data = feedback_response.json()
        
        print(f"    ✓ Feedback processed")
        print(f"    ✓ Action: {feedback_data['action']}")
        assert feedback_data["feedback_received"] == True
        assert "action" in feedback_data
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")


class TestWorkflowPhases:
    """Test workflow phase transitions"""
    
    def test_requirements_phase(self):
        """Test requirements phase"""
        print("\n  Testing requirements phase...")
        
        session_response = client.post("/api/sessions", json={})
        session_id = session_response.json()["session_id"]
        
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "notification_system",
            "description": "Build a multi-channel notification system (email, SMS, push)"
        })
        agent_id = agent_response.json()["agent_id"]
        
        # Check initial phase
        status_response = client.get(f"/api/agents/{agent_id}/status")
        status_data = status_response.json()
        
        print(f"    ✓ Initial phase: {status_data['current_phase']}")
        assert status_data["current_phase"] == WorkflowPhase.REQUIREMENTS.value
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")
    
    def test_workflow_progress_tracking(self):
        """Test workflow progress tracking"""
        print("\n  Testing workflow progress tracking...")
        
        session_response = client.post("/api/sessions", json={})
        session_id = session_response.json()["session_id"]
        
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "content_management",
            "description": "Build a headless CMS with GraphQL API"
        })
        agent_id = agent_response.json()["agent_id"]
        
        # Check progress multiple times
        for i in range(3):
            status_response = client.get(f"/api/agents/{agent_id}/status")
            status_data = status_response.json()
            
            print(f"    ✓ Check {i+1}: Progress {status_data['progress_percentage']}%")
            assert 0 <= status_data["progress_percentage"] <= 100
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")


class TestExportIntegration:
    """Test export functionality integration"""
    
    def test_export_agent_complete(self):
        """Test exporting complete agent"""
        print("\n  Testing complete agent export...")
        
        # Create session and agent
        session_response = client.post("/api/sessions", json={})
        session_id = session_response.json()["session_id"]
        
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "analytics_dashboard",
            "description": "Build a real-time analytics dashboard with data visualization"
        })
        agent_id = agent_response.json()["agent_id"]
        
        # Export agent
        export_response = client.get(
            f"/api/agents/{agent_id}/export",
            params={"export_format": "complete", "include_tests": True}
        )
        assert export_response.status_code == 200
        export_data = export_response.json()
        
        print(f"    ✓ Export completed")
        print(f"    ✓ Files generated: {export_data.get('file_count', 0)}")
        assert "agent_id" in export_data
        assert "export_format" in export_data
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")
    
    def test_export_formats(self):
        """Test different export formats"""
        print("\n  Testing different export formats...")
        
        # Create session and agent
        session_response = client.post("/api/sessions", json={})
        session_id = session_response.json()["session_id"]
        
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "microservice",
            "description": "Build a microservice for user authentication"
        })
        agent_id = agent_response.json()["agent_id"]
        
        # Test different formats
        formats = ["code", "iac", "complete"]
        for fmt in formats:
            export_response = client.get(
                f"/api/agents/{agent_id}/export",
                params={"export_format": fmt}
            )
            assert export_response.status_code == 200
            print(f"    ✓ Export format '{fmt}' successful")
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")


class TestTestingIntegration:
    """Test testing and validation integration"""
    
    def test_execute_tests(self):
        """Test executing tests through API"""
        print("\n  Testing test execution...")
        
        # Create session and agent
        session_response = client.post("/api/sessions", json={})
        session_id = session_response.json()["session_id"]
        
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "file_storage",
            "description": "Build a secure file storage service with encryption"
        })
        agent_id = agent_response.json()["agent_id"]
        
        # Execute tests
        test_response = client.post(f"/api/agents/{agent_id}/test", json={
            "session_id": session_id,
            "test_types": ["security", "performance"]
        })
        assert test_response.status_code == 200
        test_data = test_response.json()
        
        print(f"    ✓ Tests executed")
        print(f"    ✓ Production readiness: {test_data['production_readiness_score']:.2f}")
        assert "overall_status" in test_data
        assert "production_readiness_score" in test_data
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")
    
    def test_validation_report(self):
        """Test getting validation report"""
        print("\n  Testing validation report...")
        
        # Create session and agent
        session_response = client.post("/api/sessions", json={})
        session_id = session_response.json()["session_id"]
        
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "payment_processing",
            "description": "Build a PCI-compliant payment processing system"
        })
        agent_id = agent_response.json()["agent_id"]
        
        # Get validation report
        validation_response = client.get(
            f"/api/agents/{agent_id}/validation",
            params={"include_details": True}
        )
        assert validation_response.status_code == 200
        validation_data = validation_response.json()
        
        print(f"    ✓ Validation report retrieved")
        print(f"    ✓ Confidence score: {validation_data['confidence_score']:.2f}")
        assert "overall_status" in validation_data
        assert "production_readiness_score" in validation_data
        assert "multi_source_validation" in validation_data
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")


class TestErrorRecovery:
    """Test error recovery and resilience"""
    
    def test_invalid_agent_id_handling(self):
        """Test handling of invalid agent IDs"""
        print("\n  Testing invalid agent ID handling...")
        
        endpoints = [
            "/api/agents/invalid-id/status",
            "/api/agents/invalid-id/recommendations",
            "/api/agents/invalid-id/validation"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 404
            print(f"    ✓ {endpoint} returns 404")
    
    def test_workflow_state_consistency(self):
        """Test workflow state consistency"""
        print("\n  Testing workflow state consistency...")
        
        # Create session and agent
        session_response = client.post("/api/sessions", json={})
        session_id = session_response.json()["session_id"]
        
        agent_response = client.post("/api/agents/create", json={
            "session_id": session_id,
            "use_case": "consistency_test",
            "description": "Test workflow state consistency"
        })
        agent_id = agent_response.json()["agent_id"]
        
        # Check status multiple times - should be consistent
        status1 = client.get(f"/api/agents/{agent_id}/status").json()
        status2 = client.get(f"/api/agents/{agent_id}/status").json()
        
        assert status1["current_phase"] == status2["current_phase"]
        print(f"    ✓ Workflow state is consistent")
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")


def run_integration_tests():
    """Run all integration tests"""
    print("=" * 80)
    print("INTEGRATION TESTS WITH ORCHESTRATOR")
    print("=" * 80)
    print()
    
    test_classes = [
        TestOrchestratorIntegration,
        TestWorkflowPhases,
        TestExportIntegration,
        TestTestingIntegration,
        TestErrorRecovery
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}")
        print("-" * 80)
        
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith("test_")]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(test_instance, method_name)
                method()
                print(f"  ✓ {method_name}")
                passed_tests += 1
            except AssertionError as e:
                print(f"  ✗ {method_name}: {e}")
                failed_tests += 1
            except Exception as e:
                print(f"  ✗ {method_name}: {type(e).__name__}: {e}")
                failed_tests += 1
    
    print()
    print("=" * 80)
    print(f"RESULTS: {passed_tests}/{total_tests} integration tests passed")
    if failed_tests > 0:
        print(f"FAILED: {failed_tests} tests")
        return 1
    else:
        print("ALL INTEGRATION TESTS PASSED ✓")
        return 0


if __name__ == "__main__":
    exit_code = run_integration_tests()
    sys.exit(exit_code)
