import { useState, useCallback, useRef, useEffect } from 'react'
import { useWebSocket, WebSocketHandlers } from './useWebSocket'

/**
 * Streaming message state
 */
export interface StreamingMessage {
  id: string
  content: string
  isComplete: boolean
  timestamp: string
}

/**
 * Hook for managing streaming AI responses via WebSocket
 * 
 * Requirements: 5.2, 12.2
 */
export function useStreamingResponse(agentId: string) {
  const [messages, setMessages] = useState<Map<string, StreamingMessage>>(new Map())
  const [activeMessageId, setActiveMessageId] = useState<string | null>(null)
  const messageBufferRef = useRef<Map<string, string[]>>(new Map())

  // WebSocket handlers
  const handlers: WebSocketHandlers = {
    onAIResponseChunk: useCallback((data: any) => {
      const { chunk, messageId, timestamp } = data
      
      // Buffer chunks for smoother rendering
      const buffer = messageBufferRef.current.get(messageId) || []
      buffer.push(chunk)
      messageBufferRef.current.set(messageId, buffer)
      
      // Update active message
      setActiveMessageId(messageId)
      
      // Update message content
      setMessages(prev => {
        const newMessages = new Map(prev)
        const existing = newMessages.get(messageId)
        
        newMessages.set(messageId, {
          id: messageId,
          content: (existing?.content || '') + chunk,
          isComplete: false,
          timestamp: timestamp || new Date().toISOString(),
        })
        
        return newMessages
      })
    }, []),

    onAIResponseComplete: useCallback((data: any) => {
      const { messageId } = data
      
      // Mark message as complete
      setMessages(prev => {
        const newMessages = new Map(prev)
        const existing = newMessages.get(messageId)
        
        if (existing) {
          newMessages.set(messageId, {
            ...existing,
            isComplete: true,
          })
        }
        
        return newMessages
      })
      
      // Clear buffer
      messageBufferRef.current.delete(messageId)
      
      // Clear active message if it's this one
      setActiveMessageId(current => current === messageId ? null : current)
    }, []),

    onError: useCallback((error: any) => {
      console.error('WebSocket error in streaming response:', error)
    }, []),
  }

  const { isConnected, connectionState, reconnect, sendMessage } = useWebSocket(agentId, handlers)

  // Get message by ID
  const getMessage = useCallback((messageId: string): StreamingMessage | undefined => {
    return messages.get(messageId)
  }, [messages])

  // Get all messages as array
  const getAllMessages = useCallback((): StreamingMessage[] => {
    return Array.from(messages.values()).sort((a, b) => 
      new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    )
  }, [messages])

  // Get active streaming message
  const getActiveMessage = useCallback((): StreamingMessage | undefined => {
    return activeMessageId ? messages.get(activeMessageId) : undefined
  }, [activeMessageId, messages])

  // Clear all messages
  const clearMessages = useCallback(() => {
    setMessages(new Map())
    messageBufferRef.current.clear()
    setActiveMessageId(null)
  }, [])

  // Clear messages when agent changes
  useEffect(() => {
    clearMessages()
  }, [agentId, clearMessages])

  return {
    messages: getAllMessages(),
    activeMessage: getActiveMessage(),
    getMessage,
    isConnected,
    connectionState,
    reconnect,
    sendMessage,
    clearMessages,
  }
}

export default useStreamingResponse
