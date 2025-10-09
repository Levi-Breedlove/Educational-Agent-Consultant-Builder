#!/usr/bin/env python3
"""
WebSocket Implementation Validation
Simple validation script that checks the WebSocket implementation without external dependencies
"""

import sys
import os
import inspect
from typing import List, Tuple

# Add paths
sys.path.insert(0, os.path.dirname(__file__))

def validate_imports() -> Tuple[bool, List[str]]:
    """Validate that all required modules can be imported"""
    errors = []
    
    try:
        from websocket_service import (
            WebSocketManager, WebSocketConnection, MessageType, ConnectionState,
            get_websocket_manager
        )
        print("✓ websocket_service imports successful")
    except Exception as e:
        errors.append(f"✗ Failed to import websocket_service: {e}")
    
    try:
        from workflow_service import WorkflowService, get_workflow_service
        print("✓ workflow_service imports successful")
    except Exception as e:
        errors.append(f"✗ Failed to import workflow_service: {e}")
    
    try:
        # Check if main.py has WebSocket imports
        with open('main.py', 'r') as f:
            content = f.read()
            if 'WebSocket' in content and 'websocket_service' in content:
                print("✓ main.py has WebSocket imports")
            else:
                errors.append("✗ main.py missing WebSocket imports")
    except Exception as e:
        errors.append(f"✗ Failed to check main.py: {e}")
    
    return len(errors) == 0, errors


def validate_websocket_manager() -> Tuple[bool, List[str]]:
    """Validate WebSocketManager class structure"""
    errors = []
    
    try:
        from websocket_service import WebSocketManager
        
        # Check required methods
        required_methods = [
            'connect', 'disconnect', 'broadcast_to_agent',
            'broadcast_workflow_update', 'broadcast_phase_change',
            'broadcast_progress_update', 'stream_ai_response',
            'send_error', 'send_state_recovery', 'handle_client_message',
            'get_connection_count', 'get_connected_agents'
        ]
        
        manager = WebSocketManager()
        
        for method_name in required_methods:
            if not hasattr(manager, method_name):
                errors.append(f"✗ WebSocketManager missing method: {method_name}")
            else:
                method = getattr(manager, method_name)
                if not callable(method):
                    errors.append(f"✗ WebSocketManager.{method_name} is not callable")
        
        if not errors:
            print(f"✓ WebSocketManager has all {len(required_methods)} required methods")
        
        # Check attributes
        required_attrs = ['connections', 'heartbeat_interval', 'connection_timeout']
        for attr_name in required_attrs:
            if not hasattr(manager, attr_name):
                errors.append(f"✗ WebSocketManager missing attribute: {attr_name}")
        
        if not errors:
            print(f"✓ WebSocketManager has all required attributes")
        
    except Exception as e:
        errors.append(f"✗ Failed to validate WebSocketManager: {e}")
    
    return len(errors) == 0, errors


def validate_message_types() -> Tuple[bool, List[str]]:
    """Validate MessageType enum"""
    errors = []
    
    try:
        from websocket_service import MessageType
        
        required_types = [
            'HEARTBEAT', 'WORKFLOW_UPDATE', 'PHASE_CHANGE',
            'PROGRESS_UPDATE', 'AI_RESPONSE_CHUNK', 'AI_RESPONSE_COMPLETE',
            'ERROR', 'CONNECTION_ACK', 'STATE_RECOVERY'
        ]
        
        for msg_type in required_types:
            if not hasattr(MessageType, msg_type):
                errors.append(f"✗ MessageType missing: {msg_type}")
        
        if not errors:
            print(f"✓ MessageType has all {len(required_types)} required types")
        
    except Exception as e:
        errors.append(f"✗ Failed to validate MessageType: {e}")
    
    return len(errors) == 0, errors


def validate_websocket_endpoint() -> Tuple[bool, List[str]]:
    """Validate WebSocket endpoint in main.py"""
    errors = []
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Check for WebSocket endpoint
        if '@app.websocket("/ws/agents/{agent_id}")' in content:
            print("✓ WebSocket endpoint defined in main.py")
        else:
            errors.append("✗ WebSocket endpoint not found in main.py")
        
        # Check for websocket_endpoint function
        if 'async def websocket_endpoint' in content:
            print("✓ websocket_endpoint function defined")
        else:
            errors.append("✗ websocket_endpoint function not found")
        
        # Check for WebSocket stats endpoint
        if '/api/websocket/stats' in content:
            print("✓ WebSocket stats endpoint defined")
        else:
            errors.append("✗ WebSocket stats endpoint not found")
        
    except Exception as e:
        errors.append(f"✗ Failed to validate WebSocket endpoint: {e}")
    
    return len(errors) == 0, errors


def validate_workflow_integration() -> Tuple[bool, List[str]]:
    """Validate WebSocket integration in workflow service"""
    errors = []
    
    try:
        with open('workflow_service.py', 'r') as f:
            content = f.read()
        
        # Check for websocket_manager attribute
        if 'self.websocket_manager' in content:
            print("✓ workflow_service has websocket_manager attribute")
        else:
            errors.append("✗ workflow_service missing websocket_manager attribute")
        
        # Check for broadcast calls
        broadcast_methods = [
            'broadcast_workflow_update',
            'broadcast_progress_update',
            'broadcast_phase_change'
        ]
        
        found_broadcasts = 0
        for method in broadcast_methods:
            if method in content:
                found_broadcasts += 1
        
        if found_broadcasts > 0:
            print(f"✓ workflow_service has {found_broadcasts} WebSocket broadcast calls")
        else:
            errors.append("✗ workflow_service has no WebSocket broadcast calls")
        
    except Exception as e:
        errors.append(f"✗ Failed to validate workflow integration: {e}")
    
    return len(errors) == 0, errors


def validate_documentation() -> Tuple[bool, List[str]]:
    """Validate documentation exists"""
    errors = []
    
    doc_path = '../docs/websocket-guide.md'
    if os.path.exists(doc_path):
        print("✓ WebSocket documentation exists")
        
        # Check documentation content
        with open(doc_path, 'r') as f:
            content = f.read()
            
        required_sections = [
            '## Overview',
            '## Features',
            '## WebSocket Endpoint',
            '## Message Types',
            '## Client Implementation'
        ]
        
        for section in required_sections:
            if section in content:
                print(f"  ✓ Documentation has {section}")
            else:
                errors.append(f"  ✗ Documentation missing {section}")
    else:
        errors.append("✗ WebSocket documentation not found")
    
    return len(errors) == 0, errors


def validate_examples() -> Tuple[bool, List[str]]:
    """Validate example client exists"""
    errors = []
    
    example_path = 'websocket_client_example.py'
    if os.path.exists(example_path):
        print("✓ WebSocket client example exists")
    else:
        errors.append("✗ WebSocket client example not found")
    
    return len(errors) == 0, errors


def main():
    """Run all validations"""
    print("="*80)
    print("WebSocket Implementation Validation")
    print("="*80 + "\n")
    
    all_passed = True
    all_errors = []
    
    # Run validations
    validations = [
        ("Imports", validate_imports),
        ("WebSocketManager Class", validate_websocket_manager),
        ("Message Types", validate_message_types),
        ("WebSocket Endpoint", validate_websocket_endpoint),
        ("Workflow Integration", validate_workflow_integration),
        ("Documentation", validate_documentation),
        ("Examples", validate_examples)
    ]
    
    for name, validation_func in validations:
        print(f"\n{name}:")
        print("-" * 40)
        passed, errors = validation_func()
        
        if not passed:
            all_passed = False
            all_errors.extend(errors)
            for error in errors:
                print(error)
    
    # Summary
    print("\n" + "="*80)
    print("Validation Summary")
    print("="*80)
    
    if all_passed:
        print("\n✓ All validations passed!")
        print("\nWebSocket implementation is complete and ready for use.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install fastapi uvicorn websockets")
        print("  2. Start the server: uvicorn main:app --reload")
        print("  3. Test with client: python websocket_client_example.py")
        return 0
    else:
        print(f"\n✗ {len(all_errors)} validation error(s) found:")
        for error in all_errors:
            print(f"  {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
