#!/usr/bin/env python3
"""
Test Session Management Endpoints
Tests session creation, retrieval, and deletion
"""

import sys
import os
import pytest
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from api.main import app
from api.models import ExperienceLevel, SessionStatus, WorkflowPhase

# Create test client
client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_create_session_minimal():
    """Test creating a session with minimal data"""
    response = client.post("/api/sessions", json={})
    assert response.status_code == 201
    data = response.json()
    
    assert "session_id" in data
    assert data["session_id"].startswith("session-")
    assert data["status"] == SessionStatus.ACTIVE.value
    assert data["current_phase"] == WorkflowPhase.REQUIREMENTS.value
    assert data["experience_level"] == ExperienceLevel.BEGINNER.value
    assert "created_at" in data
    assert "updated_at" in data
    
    return data["session_id"]


def test_create_session_with_user():
    """Test creating a session with user ID and experience level"""
    request_data = {
        "user_id": "test-user-123",
        "experience_level": "intermediate"
    }
    
    response = client.post("/api/sessions", json=request_data)
    assert response.status_code == 201
    data = response.json()
    
    assert "session_id" in data
    assert data["status"] == SessionStatus.ACTIVE.value
    assert data["experience_level"] == ExperienceLevel.INTERMEDIATE.value
    
    return data["session_id"]


def test_get_session():
    """Test retrieving a session"""
    # First create a session
    create_response = client.post("/api/sessions", json={
        "user_id": "test-user-456",
        "experience_level": "expert"
    })
    assert create_response.status_code == 201
    session_id = create_response.json()["session_id"]
    
    # Now retrieve it
    get_response = client.get(f"/api/sessions/{session_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    
    assert data["session_id"] == session_id
    assert data["status"] == SessionStatus.ACTIVE.value
    assert data["experience_level"] == ExperienceLevel.EXPERT.value


def test_get_nonexistent_session():
    """Test retrieving a session that doesn't exist"""
    response = client.get("/api/sessions/nonexistent-session-id")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_delete_session():
    """Test deleting a session"""
    # First create a session
    create_response = client.post("/api/sessions", json={})
    assert create_response.status_code == 201
    session_id = create_response.json()["session_id"]
    
    # Delete it
    delete_response = client.delete(f"/api/sessions/{session_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    
    assert data["session_id"] == session_id
    assert data["message"] == "Session deleted successfully"
    assert "deleted_at" in data
    
    # Verify it's gone
    get_response = client.get(f"/api/sessions/{session_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_session():
    """Test deleting a session that doesn't exist"""
    response = client.delete("/api/sessions/nonexistent-session-id")
    assert response.status_code == 404


def test_session_workflow():
    """Test complete session workflow"""
    # 1. Create session
    create_response = client.post("/api/sessions", json={
        "user_id": "workflow-test-user",
        "experience_level": "beginner"
    })
    assert create_response.status_code == 201
    session_id = create_response.json()["session_id"]
    
    # 2. Retrieve session
    get_response = client.get(f"/api/sessions/{session_id}")
    assert get_response.status_code == 200
    session_data = get_response.json()
    assert session_data["session_id"] == session_id
    
    # 3. Delete session
    delete_response = client.delete(f"/api/sessions/{session_id}")
    assert delete_response.status_code == 200
    
    # 4. Verify deletion
    final_get = client.get(f"/api/sessions/{session_id}")
    assert final_get.status_code == 404


def test_multiple_sessions():
    """Test creating multiple sessions"""
    session_ids = []
    
    for i in range(3):
        response = client.post("/api/sessions", json={
            "user_id": f"multi-test-user-{i}",
            "experience_level": "intermediate"
        })
        assert response.status_code == 201
        session_ids.append(response.json()["session_id"])
    
    # Verify all sessions are unique
    assert len(session_ids) == len(set(session_ids))
    
    # Verify all can be retrieved
    for session_id in session_ids:
        response = client.get(f"/api/sessions/{session_id}")
        assert response.status_code == 200
    
    # Cleanup
    for session_id in session_ids:
        client.delete(f"/api/sessions/{session_id}")


def test_api_documentation():
    """Test that API documentation is accessible"""
    response = client.get("/api/docs")
    assert response.status_code == 200


if __name__ == "__main__":
    print("Running Session Management Tests...")
    print("=" * 60)
    
    # Note: These tests require DynamoDB to be available
    # For local testing, use LocalStack or AWS credentials
    
    try:
        test_health_check()
        print("✓ Health check test passed")
        
        test_create_session_minimal()
        print("✓ Create session (minimal) test passed")
        
        test_create_session_with_user()
        print("✓ Create session (with user) test passed")
        
        test_get_session()
        print("✓ Get session test passed")
        
        test_get_nonexistent_session()
        print("✓ Get nonexistent session test passed")
        
        test_delete_session()
        print("✓ Delete session test passed")
        
        test_delete_nonexistent_session()
        print("✓ Delete nonexistent session test passed")
        
        test_session_workflow()
        print("✓ Session workflow test passed")
        
        test_multiple_sessions()
        print("✓ Multiple sessions test passed")
        
        test_api_documentation()
        print("✓ API documentation test passed")
        
        print("=" * 60)
        print("All tests passed! ✓")
        
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error running tests: {e}")
        print("\nNote: These tests require DynamoDB access.")
        print("For local testing, use LocalStack or configure AWS credentials.")
        sys.exit(1)
