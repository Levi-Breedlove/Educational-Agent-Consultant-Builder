import { useEffect, useRef, useState, useCallback } from 'react'

/**
 * WebSocket message types from backend
 */
export enum WebSocketMessageType {
  HEARTBEAT = 'heartbeat',
  WORKFLOW_UPDATE = 'workflow_update',
  PHASE_CHANGE = 'phase_change',
  PROGRESS_UPDATE = 'progress_update',
  AI_RESPONSE_CHUNK = 'ai_response_chunk',
  AI_RESPONSE_COMPLETE = 'ai_response_complete',
  CONFIDENCE_UPDATE = 'confidence_update',
  ERROR = 'error',
  CONNECTION_ACK = 'connection_ack',
  STATE_RECOVERY = 'state_recovery',
}

/**
 * Confidence update message
 */
export interface ConfidenceUpdateMessage {
  type: WebSocketMessageType.CONFIDENCE_UPDATE
  data: {
    overallConfidence: number
    factors: {
      informationCompleteness: number
      requirementClarity: number
      technicalFeasibility: number
      validationCoverage: number
      riskAssessment: number
      userAlignment: number
    }
    confidenceBoosters: string[]
    uncertaintyFactors: string[]
    recommendedActions: string[]
    meetsBaseline: boolean
    timestamp: string
  }
}

/**
 * AI response chunk message (streaming)
 */
export interface AIResponseChunkMessage {
  type: WebSocketMessageType.AI_RESPONSE_CHUNK
  data: {
    chunk: string
    messageId: string
    timestamp: string
  }
}

/**
 * Workflow update message
 */
export interface WorkflowUpdateMessage {
  type: WebSocketMessageType.WORKFLOW_UPDATE
  data: {
    phase: string
    status: string
    message: string
    timestamp: string
  }
}

/**
 * Generic WebSocket message
 */
export type WebSocketMessage =
  | ConfidenceUpdateMessage
  | AIResponseChunkMessage
  | WorkflowUpdateMessage
  | { type: string; data: any }

/**
 * WebSocket event handlers
 */
export interface WebSocketHandlers {
  onConfidenceUpdate?: (data: ConfidenceUpdateMessage['data']) => void
  onAIResponseChunk?: (data: AIResponseChunkMessage['data']) => void
  onAIResponseComplete?: (data: any) => void
  onWorkflowUpdate?: (data: WorkflowUpdateMessage['data']) => void
  onPhaseChange?: (data: any) => void
  onProgressUpdate?: (data: any) => void
  onError?: (error: any) => void
}

interface UseWebSocketReturn {
  sendMessage: (data: any) => void
  lastMessage: MessageEvent | null
  isConnected: boolean
  reconnect: () => void
  connectionState: 'connecting' | 'connected' | 'disconnected' | 'error'
}

export function useWebSocket(
  agentId: string,
  handlers?: WebSocketHandlers
): UseWebSocketReturn {
  const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [connectionState, setConnectionState] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected')
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<number>()
  const reconnectAttemptsRef = useRef(0)
  const heartbeatIntervalRef = useRef<number>()
  const maxReconnectAttempts = 5
  const heartbeatInterval = 30000 // 30 seconds

  // Start heartbeat to keep connection alive
  const startHeartbeat = useCallback(() => {
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current)
    }

    heartbeatIntervalRef.current = setInterval(() => {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ type: 'heartbeat' }))
      }
    }, heartbeatInterval)
  }, [])

  // Stop heartbeat
  const stopHeartbeat = useCallback(() => {
    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current)
      heartbeatIntervalRef.current = undefined
    }
  }, [])

  // Handle incoming messages
  const handleMessage = useCallback((event: MessageEvent) => {
    try {
      const message: WebSocketMessage = JSON.parse(event.data)
      
      // Route message to appropriate handler
      switch (message.type) {
        case WebSocketMessageType.CONFIDENCE_UPDATE:
          handlers?.onConfidenceUpdate?.(message.data)
          break
        
        case WebSocketMessageType.AI_RESPONSE_CHUNK:
          handlers?.onAIResponseChunk?.(message.data)
          break
        
        case WebSocketMessageType.AI_RESPONSE_COMPLETE:
          handlers?.onAIResponseComplete?.(message.data)
          break
        
        case WebSocketMessageType.WORKFLOW_UPDATE:
          handlers?.onWorkflowUpdate?.(message.data)
          break
        
        case WebSocketMessageType.PHASE_CHANGE:
          handlers?.onPhaseChange?.(message.data)
          break
        
        case WebSocketMessageType.PROGRESS_UPDATE:
          handlers?.onProgressUpdate?.(message.data)
          break
        
        case WebSocketMessageType.ERROR:
          handlers?.onError?.(message.data)
          break
        
        case WebSocketMessageType.HEARTBEAT:
          // Heartbeat acknowledged, connection is alive
          break
        
        case WebSocketMessageType.CONNECTION_ACK:
          console.log('Connection acknowledged by server')
          break
        
        case WebSocketMessageType.STATE_RECOVERY:
          console.log('State recovered:', message.data)
          break
        
        default:
          console.log('Unknown message type:', message.type)
      }
      
      setLastMessage(event)
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error)
    }
  }, [handlers])

  const connect = useCallback(() => {
    if (!agentId) return

    try {
      setConnectionState('connecting')
      
      // Use the proxy configured in vite.config.ts
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const wsUrl = `${protocol}//${window.location.host}/ws/agents/${agentId}`
      
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        console.log('WebSocket connected')
        setIsConnected(true)
        setConnectionState('connected')
        reconnectAttemptsRef.current = 0
        startHeartbeat()
      }

      ws.onmessage = handleMessage

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setConnectionState('error')
        handlers?.onError?.(error)
      }

      ws.onclose = () => {
        console.log('WebSocket disconnected')
        setIsConnected(false)
        setConnectionState('disconnected')
        wsRef.current = null
        stopHeartbeat()

        // Attempt to reconnect
        if (reconnectAttemptsRef.current < maxReconnectAttempts) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000)
          console.log(`Reconnecting in ${delay}ms... (attempt ${reconnectAttemptsRef.current + 1}/${maxReconnectAttempts})`)
          
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current++
            connect()
          }, delay) as unknown as number
        } else {
          console.error('Max reconnection attempts reached')
          setConnectionState('error')
        }
      }

      wsRef.current = ws
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
      setConnectionState('error')
    }
  }, [agentId, handleMessage, startHeartbeat, stopHeartbeat, handlers])

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
    }
    stopHeartbeat()
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    setConnectionState('disconnected')
  }, [stopHeartbeat])

  const sendMessage = useCallback((data: any) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }, [])

  const reconnect = useCallback(() => {
    disconnect()
    reconnectAttemptsRef.current = 0
    connect()
  }, [disconnect, connect])

  useEffect(() => {
    connect()
    return () => disconnect()
  }, [connect, disconnect])

  return {
    sendMessage,
    lastMessage,
    isConnected,
    reconnect,
    connectionState,
  }
}
