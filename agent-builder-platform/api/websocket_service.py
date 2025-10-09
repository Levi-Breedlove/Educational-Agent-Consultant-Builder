#!/usr/bin/env python3
"""
WebSocket Service for Real-Time Updates
Manages WebSocket connections, heartbeat, message broadcasting, and state recovery
"""

import asyncio
import json
import logging
from typing import Dict, Set, Optional, Any
from datetime import datetime, timezone
from fastapi import WebSocket, WebSocketDisconnect
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """WebSocket message types"""
    HEARTBEAT = "heartbeat"
    WORKFLOW_UPDATE = "workflow_update"
    PHASE_CHANGE = "phase_change"
    PROGRESS_UPDATE = "progress_update"
    AI_RESPONSE_CHUNK = "ai_response_chunk"
    AI_RESPONSE_COMPLETE = "ai_response_complete"
    ERROR = "error"
    CONNECTION_ACK = "connection_ack"
    STATE_RECOVERY = "state_recovery"


class ConnectionState(str, Enum):
    """WebSocket connection states"""
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"


class WebSocketConnection:
    """Represents a single WebSocket connection"""
    
    def __init__(self, websocket: WebSocket, agent_id: str, session_id: str):
        self.websocket = websocket
        self.agent_id = agent_id
        self.session_id = session_id
        self.connected_at = datetime.now(timezone.utc)
        self.last_heartbeat = datetime.now(timezone.utc)
        self.state = ConnectionState.CONNECTING
        self.message_queue: asyncio.Queue = asyncio.Queue()
        
    async def send_json(self, data: Dict[str, Any]):
        """Send JSON message to client"""
        try:
            await self.websocket.send_json(data)
            logger.debug(f"Sent message to {self.agent_id}: {data.get('type')}")
        except Exception as e:
            logger.error(f"Error sending message to {self.agent_id}: {e}")
            self.state = ConnectionState.DISCONNECTED
            raise
    
    async def receive_json(self) -> Dict[str, Any]:
        """Receive JSON message from client"""
        try:
            data = await self.websocket.receive_json()
            logger.debug(f"Received message from {self.agent_id}: {data.get('type')}")
            return data
        except Exception as e:
            logger.error(f"Error receiving message from {self.agent_id}: {e}")
            self.state = ConnectionState.DISCONNECTED
            raise
    
    def update_heartbeat(self):
        """Update last heartbeat timestamp"""
        self.last_heartbeat = datetime.now(timezone.utc)


class WebSocketManager:
    """Manages all WebSocket connections and message broadcasting"""
    
    def __init__(self):
        # Map of agent_id -> set of connections (supports multiple connections per agent)
        self.connections: Dict[str, Set[WebSocketConnection]] = {}
        # Heartbeat interval in seconds
        self.heartbeat_interval = 30
        # Connection timeout in seconds
        self.connection_timeout = 90
        # Background tasks
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._cleanup_task: Optional[asyncio.Task] = None
        
    async def connect(self, websocket: WebSocket, agent_id: str, session_id: str) -> WebSocketConnection:
        """
        Accept WebSocket connection and register it
        
        Args:
            websocket: FastAPI WebSocket instance
            agent_id: Agent identifier
            session_id: Session identifier
            
        Returns:
            WebSocketConnection instance
        """
        await websocket.accept()
        
        connection = WebSocketConnection(websocket, agent_id, session_id)
        
        # Add to connections map
        if agent_id not in self.connections:
            self.connections[agent_id] = set()
        self.connections[agent_id].add(connection)
        
        connection.state = ConnectionState.CONNECTED
        
        # Send connection acknowledgment
        await connection.send_json({
            "type": MessageType.CONNECTION_ACK,
            "agent_id": agent_id,
            "session_id": session_id,
            "connected_at": connection.connected_at.isoformat(),
            "heartbeat_interval": self.heartbeat_interval,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        logger.info(f"WebSocket connected: agent_id={agent_id}, session_id={session_id}")
        
        # Start background tasks if not running
        if self._heartbeat_task is None or self._heartbeat_task.done():
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        if self._cleanup_task is None or self._cleanup_task.done():
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        
        return connection
    
    async def disconnect(self, connection: WebSocketConnection):
        """
        Disconnect and unregister a WebSocket connection
        
        Args:
            connection: WebSocketConnection to disconnect
        """
        agent_id = connection.agent_id
        
        # Remove from connections
        if agent_id in self.connections:
            self.connections[agent_id].discard(connection)
            if not self.connections[agent_id]:
                del self.connections[agent_id]
        
        connection.state = ConnectionState.DISCONNECTED
        
        logger.info(f"WebSocket disconnected: agent_id={agent_id}")
    
    async def broadcast_to_agent(self, agent_id: str, message: Dict[str, Any]):
        """
        Broadcast message to all connections for a specific agent
        
        Args:
            agent_id: Agent identifier
            message: Message data to broadcast
        """
        if agent_id not in self.connections:
            logger.warning(f"No connections found for agent_id={agent_id}")
            return
        
        # Add timestamp if not present
        if "timestamp" not in message:
            message["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        # Send to all connections for this agent
        disconnected = []
        for connection in self.connections[agent_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send to connection: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            await self.disconnect(connection)
    
    async def broadcast_workflow_update(self, agent_id: str, update_data: Dict[str, Any]):
        """
        Broadcast workflow update to agent connections
        
        Args:
            agent_id: Agent identifier
            update_data: Workflow update data
        """
        message = {
            "type": MessageType.WORKFLOW_UPDATE,
            "agent_id": agent_id,
            "data": update_data
        }
        await self.broadcast_to_agent(agent_id, message)
    
    async def broadcast_phase_change(self, agent_id: str, old_phase: str, new_phase: str, progress: float):
        """
        Broadcast phase change notification
        
        Args:
            agent_id: Agent identifier
            old_phase: Previous phase
            new_phase: New phase
            progress: Progress percentage
        """
        message = {
            "type": MessageType.PHASE_CHANGE,
            "agent_id": agent_id,
            "data": {
                "old_phase": old_phase,
                "new_phase": new_phase,
                "progress_percentage": progress
            }
        }
        await self.broadcast_to_agent(agent_id, message)
    
    async def broadcast_progress_update(self, agent_id: str, progress: float, status: str, message_text: str):
        """
        Broadcast progress update
        
        Args:
            agent_id: Agent identifier
            progress: Progress percentage (0-100)
            status: Current status
            message_text: Progress message
        """
        message = {
            "type": MessageType.PROGRESS_UPDATE,
            "agent_id": agent_id,
            "data": {
                "progress_percentage": progress,
                "status": status,
                "message": message_text
            }
        }
        await self.broadcast_to_agent(agent_id, message)
    
    async def stream_ai_response(self, agent_id: str, response_id: str, chunk: str, is_complete: bool = False):
        """
        Stream AI agent response chunks for real-time display
        
        Args:
            agent_id: Agent identifier
            response_id: Unique response identifier
            chunk: Text chunk to stream
            is_complete: Whether this is the final chunk
        """
        message_type = MessageType.AI_RESPONSE_COMPLETE if is_complete else MessageType.AI_RESPONSE_CHUNK
        
        message = {
            "type": message_type,
            "agent_id": agent_id,
            "data": {
                "response_id": response_id,
                "chunk": chunk,
                "is_complete": is_complete
            }
        }
        await self.broadcast_to_agent(agent_id, message)
    
    async def send_error(self, agent_id: str, error_message: str, error_code: Optional[str] = None):
        """
        Send error message to agent connections
        
        Args:
            agent_id: Agent identifier
            error_message: Error message
            error_code: Optional error code
        """
        message = {
            "type": MessageType.ERROR,
            "agent_id": agent_id,
            "data": {
                "message": error_message,
                "code": error_code
            }
        }
        await self.broadcast_to_agent(agent_id, message)
    
    async def send_state_recovery(self, connection: WebSocketConnection, state_data: Dict[str, Any]):
        """
        Send state recovery data to a reconnected client
        
        Args:
            connection: WebSocketConnection instance
            state_data: State data to recover
        """
        message = {
            "type": MessageType.STATE_RECOVERY,
            "agent_id": connection.agent_id,
            "data": state_data
        }
        await connection.send_json(message)
    
    async def handle_client_message(self, connection: WebSocketConnection, message: Dict[str, Any]):
        """
        Handle incoming message from client
        
        Args:
            connection: WebSocketConnection instance
            message: Message data from client
        """
        message_type = message.get("type")
        
        if message_type == MessageType.HEARTBEAT:
            # Update heartbeat timestamp
            connection.update_heartbeat()
            # Send heartbeat response
            await connection.send_json({
                "type": MessageType.HEARTBEAT,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        else:
            logger.debug(f"Received client message: {message_type}")
    
    async def _heartbeat_loop(self):
        """Background task to send periodic heartbeats"""
        while True:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                
                # Send heartbeat to all connections
                for agent_id, connections in list(self.connections.items()):
                    for connection in list(connections):
                        try:
                            await connection.send_json({
                                "type": MessageType.HEARTBEAT,
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            })
                        except Exception as e:
                            logger.error(f"Heartbeat failed for {agent_id}: {e}")
                            await self.disconnect(connection)
                
            except Exception as e:
                logger.error(f"Error in heartbeat loop: {e}")
    
    async def _cleanup_loop(self):
        """Background task to clean up stale connections"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                now = datetime.now(timezone.utc)
                
                # Check for stale connections
                for agent_id, connections in list(self.connections.items()):
                    for connection in list(connections):
                        time_since_heartbeat = (now - connection.last_heartbeat).total_seconds()
                        
                        if time_since_heartbeat > self.connection_timeout:
                            logger.warning(f"Connection timeout for {agent_id}, disconnecting")
                            await self.disconnect(connection)
                
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
    
    def get_connection_count(self, agent_id: Optional[str] = None) -> int:
        """
        Get number of active connections
        
        Args:
            agent_id: Optional agent_id to filter by
            
        Returns:
            Number of active connections
        """
        if agent_id:
            return len(self.connections.get(agent_id, set()))
        return sum(len(conns) for conns in self.connections.values())
    
    def get_connected_agents(self) -> list:
        """
        Get list of agent IDs with active connections
        
        Returns:
            List of agent IDs
        """
        return list(self.connections.keys())


# Global WebSocket manager instance
_websocket_manager: Optional[WebSocketManager] = None


def get_websocket_manager() -> WebSocketManager:
    """Get WebSocket manager instance (singleton)"""
    global _websocket_manager
    if _websocket_manager is None:
        _websocket_manager = WebSocketManager()
    return _websocket_manager
