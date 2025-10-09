#!/usr/bin/env python3
"""
WebSocket Client Example
Demonstrates how to connect to the WebSocket endpoint and handle real-time updates
"""

import asyncio
import json
import websockets
from datetime import datetime


class AgentWebSocketClient:
    """Example WebSocket client for agent workflow updates"""
    
    def __init__(self, base_url: str = "ws://localhost:8000"):
        self.base_url = base_url
        self.websocket = None
        self.connected = False
        self.heartbeat_task = None
        
    async def connect(self, agent_id: str, session_id: str = None):
        """
        Connect to WebSocket endpoint
        
        Args:
            agent_id: Agent identifier
            session_id: Optional session identifier
        """
        url = f"{self.base_url}/ws/agents/{agent_id}"
        if session_id:
            url += f"?session_id={session_id}"
        
        print(f"Connecting to {url}...")
        
        try:
            self.websocket = await websockets.connect(url)
            self.connected = True
            print("✓ Connected successfully")
            
            # Start heartbeat task
            self.heartbeat_task = asyncio.create_task(self._heartbeat_loop())
            
            # Wait for connection acknowledgment
            ack = await self.websocket.recv()
            ack_data = json.loads(ack)
            
            if ack_data.get("type") == "connection_ack":
                print(f"✓ Connection acknowledged")
                print(f"  Agent ID: {ack_data.get('agent_id')}")
                print(f"  Session ID: {ack_data.get('session_id')}")
                print(f"  Heartbeat interval: {ack_data.get('heartbeat_interval')}s")
            
            return True
            
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from WebSocket"""
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
        
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            print("✓ Disconnected")
    
    async def listen(self):
        """
        Listen for messages from server
        Handles all message types and displays them
        """
        if not self.connected:
            print("✗ Not connected")
            return
        
        print("\nListening for messages (Ctrl+C to stop)...\n")
        
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self._handle_message(data)
                
        except websockets.exceptions.ConnectionClosed:
            print("\n✗ Connection closed by server")
            self.connected = False
        except KeyboardInterrupt:
            print("\n\nStopping...")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    async def _handle_message(self, data: dict):
        """Handle incoming message based on type"""
        msg_type = data.get("type")
        timestamp = data.get("timestamp", "")
        
        if msg_type == "heartbeat":
            # Silent heartbeat (don't print)
            pass
        
        elif msg_type == "connection_ack":
            print(f"[{timestamp}] CONNECTION ACK")
            print(f"  Agent: {data.get('agent_id')}")
        
        elif msg_type == "workflow_update":
            print(f"[{timestamp}] WORKFLOW UPDATE")
            update_data = data.get("data", {})
            for key, value in update_data.items():
                print(f"  {key}: {value}")
        
        elif msg_type == "phase_change":
            print(f"[{timestamp}] PHASE CHANGE")
            phase_data = data.get("data", {})
            print(f"  {phase_data.get('old_phase')} → {phase_data.get('new_phase')}")
            print(f"  Progress: {phase_data.get('progress_percentage')}%")
        
        elif msg_type == "progress_update":
            print(f"[{timestamp}] PROGRESS UPDATE")
            progress_data = data.get("data", {})
            print(f"  Status: {progress_data.get('status')}")
            print(f"  Progress: {progress_data.get('progress_percentage')}%")
            print(f"  Message: {progress_data.get('message')}")
        
        elif msg_type == "ai_response_chunk":
            # Print chunk without newline for streaming effect
            chunk_data = data.get("data", {})
            print(chunk_data.get("chunk"), end="", flush=True)
        
        elif msg_type == "ai_response_complete":
            print()  # Newline after streaming complete
            print(f"[{timestamp}] AI RESPONSE COMPLETE")
        
        elif msg_type == "state_recovery":
            print(f"[{timestamp}] STATE RECOVERY")
            state_data = data.get("data", {})
            for key, value in state_data.items():
                print(f"  {key}: {value}")
        
        elif msg_type == "error":
            print(f"[{timestamp}] ERROR")
            error_data = data.get("data", {})
            print(f"  Message: {error_data.get('message')}")
            print(f"  Code: {error_data.get('code')}")
        
        else:
            print(f"[{timestamp}] UNKNOWN MESSAGE TYPE: {msg_type}")
            print(f"  Data: {data}")
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeat to server"""
        while self.connected:
            try:
                await asyncio.sleep(25)  # Send every 25s (server expects 30s)
                
                if self.connected and self.websocket:
                    heartbeat = {
                        "type": "heartbeat",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    await self.websocket.send(json.dumps(heartbeat))
                    
            except Exception as e:
                print(f"Heartbeat error: {e}")
                break


async def main():
    """Example usage"""
    print("="*80)
    print("Agent Builder Platform - WebSocket Client Example")
    print("="*80 + "\n")
    
    # Create client
    client = AgentWebSocketClient("ws://localhost:8000")
    
    # Connect to agent workflow
    agent_id = "agent-test-123"
    session_id = "session-test-456"
    
    connected = await client.connect(agent_id, session_id)
    
    if connected:
        # Listen for messages
        await client.listen()
        
        # Disconnect
        await client.disconnect()
    
    print("\nExample complete!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
