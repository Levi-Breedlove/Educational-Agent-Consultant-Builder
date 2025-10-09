#!/usr/bin/env python3
"""
WebSocket Endpoint Tests
Tests WebSocket connection, heartbeat, message broadcasting, and state recovery
"""

import asyncio
import json
import sys
import os
import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Import the services
from websocket_service import (
    WebSocketManager, WebSocketConnection, MessageType, ConnectionState,
    get_websocket_manager
)


class TestWebSocketService:
    """Test WebSocket service functionality"""
    
    def test_websocket_manager_initialization(self):
        """Test WebSocket manager initialization"""
        manager = WebSocketManager()
        
        assert manager.connections == {}
        assert manager.heartbeat_interval == 30
        assert manager.connection_timeout == 90
        assert manager.get_connection_count() == 0
        assert manager.get_connected_agents() == []
    
    @pytest.mark.asyncio
    async def test_websocket_connection_lifecycle(self):
        """Test WebSocket connection and disconnection"""
        manager = WebSocketManager()
        
        # Mock WebSocket
        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()
        mock_ws.send_json = AsyncMock()
        
        # Connect
        connection = await manager.connect(mock_ws, "agent-123", "session-456")
        
        assert connection.agent_id == "agent-123"
        assert connection.session_id == "session-456"
        assert connection.state == ConnectionState.CONNECTED
        assert manager.get_connection_count() == 1
        assert "agent-123" in manager.get_connected_agents()
        
        # Verify connection acknowledgment was sent
        mock_ws.send_json.assert_called_once()
        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == MessageType.CONNECTION_ACK
        assert call_args["agent_id"] == "agent-123"
        
        # Disconnect
        await manager.disconnect(connection)
        
        assert connection.state == ConnectionState.DISCONNECTED
        assert manager.get_connection_count() == 0
        assert "agent-123" not in manager.get_connected_agents()
    
    @pytest.mark.asyncio
    async def test_multiple_connections_per_agent(self):
        """Test multiple WebSocket connections for same agent"""
        manager = WebSocketManager()
        
        # Create two connections for same agent
        mock_ws1 = AsyncMock(spec=WebSocket)
        mock_ws1.accept = AsyncMock()
        mock_ws1.send_json = AsyncMock()
        
        mock_ws2 = AsyncMock(spec=WebSocket)
        mock_ws2.accept = AsyncMock()
        mock_ws2.send_json = AsyncMock()
        
        connection1 = await manager.connect(mock_ws1, "agent-123", "session-1")
        connection2 = await manager.connect(mock_ws2, "agent-123", "session-2")
        
        assert manager.get_connection_count() == 2
        assert manager.get_connection_count("agent-123") == 2
        
        # Disconnect one
        await manager.disconnect(connection1)
        
        assert manager.get_connection_count() == 1
        assert manager.get_connection_count("agent-123") == 1
    
    @pytest.mark.asyncio
    async def test_broadcast_to_agent(self):
        """Test broadcasting messages to agent connections"""
        manager = WebSocketManager()
        
        # Create two connections for same agent
        mock_ws1 = AsyncMock(spec=WebSocket)
        mock_ws1.accept = AsyncMock()
        mock_ws1.send_json = AsyncMock()
        
        mock_ws2 = AsyncMock(spec=WebSocket)
        mock_ws2.accept = AsyncMock()
        mock_ws2.send_json = AsyncMock()
        
        await manager.connect(mock_ws1, "agent-123", "session-1")
        await manager.connect(mock_ws2, "agent-123", "session-2")
        
        # Reset mocks to clear connection ack calls
        mock_ws1.send_json.reset_mock()
        mock_ws2.send_json.reset_mock()
        
        # Broadcast message
        test_message = {
            "type": MessageType.WORKFLOW_UPDATE,
            "data": {"status": "processing"}
        }
        
        await manager.broadcast_to_agent("agent-123", test_message)
        
        # Both connections should receive the message
        assert mock_ws1.send_json.call_count == 1
        assert mock_ws2.send_json.call_count == 1
        
        # Verify message content
        call_args1 = mock_ws1.send_json.call_args[0][0]
        assert call_args1["type"] == MessageType.WORKFLOW_UPDATE
        assert "timestamp" in call_args1
    
    @pytest.mark.asyncio
    async def test_workflow_update_broadcast(self):
        """Test workflow update broadcasting"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()
        mock_ws.send_json = AsyncMock()
        
        await manager.connect(mock_ws, "agent-123", "session-1")
        mock_ws.send_json.reset_mock()
        
        # Broadcast workflow update
        update_data = {
            "event": "requirements_complete",
            "progress": 25
        }
        
        await manager.broadcast_workflow_update("agent-123", update_data)
        
        # Verify message
        assert mock_ws.send_json.call_count == 1
        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == MessageType.WORKFLOW_UPDATE
        assert call_args["agent_id"] == "agent-123"
        assert call_args["data"] == update_data
    
    @pytest.mark.asyncio
    async def test_phase_change_broadcast(self):
        """Test phase change broadcasting"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()
        mock_ws.send_json = AsyncMock()
        
        await manager.connect(mock_ws, "agent-123", "session-1")
        mock_ws.send_json.reset_mock()
        
        # Broadcast phase change
        await manager.broadcast_phase_change(
            "agent-123",
            "requirements",
            "architecture",
            40.0
        )
        
        # Verify message
        assert mock_ws.send_json.call_count == 1
        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == MessageType.PHASE_CHANGE
        assert call_args["data"]["old_phase"] == "requirements"
        assert call_args["data"]["new_phase"] == "architecture"
        assert call_args["data"]["progress_percentage"] == 40.0
    
    @pytest.mark.asyncio
    async def test_progress_update_broadcast(self):
        """Test progress update broadcasting"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()
        mock_ws.send_json = AsyncMock()
        
        await manager.connect(mock_ws, "agent-123", "session-1")
        mock_ws.send_json.reset_mock()
        
        # Broadcast progress update
        await manager.broadcast_progress_update(
            "agent-123",
            65.5,
            "implementation",
            "Generating code files..."
        )
        
        # Verify message
        assert mock_ws.send_json.call_count == 1
        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == MessageType.PROGRESS_UPDATE
        assert call_args["data"]["progress_percentage"] == 65.5
        assert call_args["data"]["status"] == "implementation"
        assert call_args["data"]["message"] == "Generating code files..."
    
    @pytest.mark.asyncio
    async def test_ai_response_streaming(self):
        """Test AI response streaming"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()
        mock_ws.send_json = AsyncMock()
        
        await manager.connect(mock_ws, "agent-123", "session-1")
        mock_ws.send_json.reset_mock()
        
        # Stream response chunks
        response_id = "resp-123"
        chunks = ["Hello ", "world", "!"]
        
        for i, chunk in enumerate(chunks):
            is_complete = (i == len(chunks) - 1)
            await manager.stream_ai_response("agent-123", response_id, chunk, is_complete)
        
        # Verify all chunks were sent
        assert mock_ws.send_json.call_count == 3
        
        # Verify last message is marked complete
        last_call = mock_ws.send_json.call_args_list[-1][0][0]
        assert last_call["type"] == MessageType.AI_RESPONSE_COMPLETE
        assert last_call["data"]["is_complete"] is True
    
    @pytest.mark.asyncio
    async def test_error_broadcasting(self):
        """Test error message broadcasting"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()
        mock_ws.send_json = AsyncMock()
        
        await manager.connect(mock_ws, "agent-123", "session-1")
        mock_ws.send_json.reset_mock()
        
        # Send error
        await manager.send_error("agent-123", "Something went wrong", "ERROR_CODE_123")
        
        # Verify error message
        assert mock_ws.send_json.call_count == 1
        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == MessageType.ERROR
        assert call_args["data"]["message"] == "Something went wrong"
        assert call_args["data"]["code"] == "ERROR_CODE_123"
    
    @pytest.mark.asyncio
    async def test_state_recovery(self):
        """Test state recovery for reconnected clients"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()
        mock_ws.send_json = AsyncMock()
        
        connection = await manager.connect(mock_ws, "agent-123", "session-1")
        mock_ws.send_json.reset_mock()
        
        # Send state recovery
        state_data = {
            "status": "architecture",
            "progress_percentage": 45,
            "last_update": "2025-10-03T10:00:00Z"
        }
        
        await manager.send_state_recovery(connection, state_data)
        
        # Verify state recovery message
        assert mock_ws.send_json.call_count == 1
        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == MessageType.STATE_RECOVERY
        assert call_args["data"] == state_data
    
    @pytest.mark.asyncio
    async def test_heartbeat_handling(self):
        """Test heartbeat message handling"""
        manager = WebSocketManager()
        
        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()
        mock_ws.send_json = AsyncMock()
        
        connection = await manager.connect(mock_ws, "agent-123", "session-1")
        mock_ws.send_json.reset_mock()
        
        # Simulate heartbeat from client
        heartbeat_message = {"type": MessageType.HEARTBEAT}
        
        old_heartbeat = connection.last_heartbeat
        await asyncio.sleep(0.1)  # Small delay
        
        await manager.handle_client_message(connection, heartbeat_message)
        
        # Verify heartbeat was updated
        assert connection.last_heartbeat > old_heartbeat
        
        # Verify heartbeat response was sent
        assert mock_ws.send_json.call_count == 1
        call_args = mock_ws.send_json.call_args[0][0]
        assert call_args["type"] == MessageType.HEARTBEAT
    
    @pytest.mark.asyncio
    async def test_connection_cleanup_on_error(self):
        """Test connection cleanup when send fails"""
        manager = WebSocketManager()
        
        # Mock WebSocket that works for accept but fails on subsequent sends
        mock_ws = AsyncMock(spec=WebSocket)
        mock_ws.accept = AsyncMock()
        
        # First call (connection ack) succeeds, second call fails
        mock_ws.send_json = AsyncMock(side_effect=[None, Exception("Connection lost")])
        
        connection = await manager.connect(mock_ws, "agent-123", "session-1")
        
        # Connection should be established
        assert manager.get_connection_count() == 1
        
        # Try to broadcast (should fail and cleanup)
        await manager.broadcast_to_agent("agent-123", {"type": "test"})
        
        # Connection should be removed after failed broadcast
        assert manager.get_connection_count() == 0


class TestWebSocketEndpoint:
    """Test WebSocket endpoint integration"""
    
    def test_websocket_manager_singleton(self):
        """Test WebSocket manager singleton pattern"""
        manager1 = get_websocket_manager()
        manager2 = get_websocket_manager()
        
        assert manager1 is manager2
        assert isinstance(manager1, WebSocketManager)


def run_tests():
    """Run all WebSocket tests"""
    print("Running WebSocket tests...")
    print("\n" + "="*80)
    print("WebSocket Service Tests")
    print("="*80 + "\n")
    
    # Run pytest
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
