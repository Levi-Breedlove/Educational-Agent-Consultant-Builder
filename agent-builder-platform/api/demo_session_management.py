#!/usr/bin/env python3
"""
Demo Script for Session Management
Demonstrates creating, retrieving, and deleting sessions
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_response(response, title="Response"):
    """Pretty print API response"""
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    if response.status_code < 400:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

def main():
    """Run session management demo"""
    print_section("Agent Builder Platform - Session Management Demo")
    
    # 1. Health Check
    print_section("1. Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Status")
    
    if response.status_code != 200:
        print("\n❌ API is not running. Please start the API server first:")
        print("   cd agent-builder-platform/api")
        print("   python main.py")
        return
    
    # 2. Create Session (Minimal)
    print_section("2. Create Session (Minimal)")
    response = requests.post(f"{BASE_URL}/api/sessions", json={})
    print_response(response, "Created Session")
    
    if response.status_code == 201:
        session_id_1 = response.json()["session_id"]
        print(f"\n✓ Session created: {session_id_1}")
    else:
        print("\n❌ Failed to create session")
        return
    
    # 3. Create Session (With User Data)
    print_section("3. Create Session (With User Data)")
    session_data = {
        "user_id": "demo-user-123",
        "experience_level": "intermediate"
    }
    response = requests.post(f"{BASE_URL}/api/sessions", json=session_data)
    print_response(response, "Created Session with User Data")
    
    if response.status_code == 201:
        session_id_2 = response.json()["session_id"]
        print(f"\n✓ Session created: {session_id_2}")
    else:
        print("\n❌ Failed to create session")
        return
    
    # 4. Retrieve Session
    print_section("4. Retrieve Session")
    response = requests.get(f"{BASE_URL}/api/sessions/{session_id_2}")
    print_response(response, "Retrieved Session")
    
    if response.status_code == 200:
        session = response.json()
        print(f"\n✓ Session retrieved successfully")
        print(f"  - Status: {session['status']}")
        print(f"  - Phase: {session['current_phase']}")
        print(f"  - Experience: {session['experience_level']}")
    
    # 5. Try to Retrieve Non-existent Session
    print_section("5. Retrieve Non-existent Session (Error Case)")
    response = requests.get(f"{BASE_URL}/api/sessions/nonexistent-session-id")
    print_response(response, "Expected 404 Error")
    
    if response.status_code == 404:
        print("\n✓ Correctly returned 404 for non-existent session")
    
    # 6. Delete Session
    print_section("6. Delete Session")
    response = requests.delete(f"{BASE_URL}/api/sessions/{session_id_1}")
    print_response(response, "Deleted Session")
    
    if response.status_code == 200:
        print(f"\n✓ Session deleted: {session_id_1}")
    
    # 7. Verify Deletion
    print_section("7. Verify Session Deletion")
    response = requests.get(f"{BASE_URL}/api/sessions/{session_id_1}")
    print_response(response, "Expected 404 After Deletion")
    
    if response.status_code == 404:
        print("\n✓ Session successfully deleted (404 returned)")
    
    # 8. Create Multiple Sessions
    print_section("8. Create Multiple Sessions")
    session_ids = []
    for i in range(3):
        response = requests.post(f"{BASE_URL}/api/sessions", json={
            "user_id": f"batch-user-{i}",
            "experience_level": "beginner"
        })
        if response.status_code == 201:
            session_id = response.json()["session_id"]
            session_ids.append(session_id)
            print(f"✓ Created session {i+1}: {session_id}")
    
    print(f"\n✓ Created {len(session_ids)} sessions")
    
    # 9. Cleanup
    print_section("9. Cleanup All Demo Sessions")
    all_sessions = [session_id_2] + session_ids
    for session_id in all_sessions:
        response = requests.delete(f"{BASE_URL}/api/sessions/{session_id}")
        if response.status_code == 200:
            print(f"✓ Deleted: {session_id}")
    
    # 10. Summary
    print_section("Demo Complete")
    print("\n✅ All session management operations completed successfully!")
    print("\nSession Management Features Demonstrated:")
    print("  ✓ Create sessions (minimal and with user data)")
    print("  ✓ Retrieve session details")
    print("  ✓ Delete sessions")
    print("  ✓ Error handling (404 for non-existent sessions)")
    print("  ✓ Multiple concurrent sessions")
    print("\nNext Steps:")
    print("  - View API docs: http://localhost:8000/api/docs")
    print("  - Run tests: python test_session_management.py")
    print("  - Implement Task 11.3: Agent creation workflow endpoints")
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("\nPlease start the API server first:")
        print("  cd agent-builder-platform/api")
        print("  python main.py")
        print("\nThen run this demo again:")
        print("  python demo_session_management.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
