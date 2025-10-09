import { useState, useCallback, useEffect } from 'react'
import { useWebSocket, WebSocketHandlers } from './useWebSocket'
import type { ConfidenceScore, ConfidenceHistoryPoint } from '../components/ConfidenceDashboard'

/**
 * Hook for managing real-time confidence updates via WebSocket
 * 
 * Requirements: 20.2, 20.3, 20.11
 */
export function useConfidenceUpdates(agentId: string) {
  const [currentScore, setCurrentScore] = useState<ConfidenceScore | null>(null)
  const [history, setHistory] = useState<ConfidenceHistoryPoint[]>([])
  const [currentPhase, setCurrentPhase] = useState<string>('requirements')

  // WebSocket handlers
  const handlers: WebSocketHandlers = {
    onConfidenceUpdate: useCallback((data: any) => {
      const score: ConfidenceScore = {
        overallConfidence: data.overallConfidence,
        factors: data.factors,
        confidenceBoosters: data.confidenceBoosters,
        uncertaintyFactors: data.uncertaintyFactors,
        recommendedActions: data.recommendedActions,
        meetsBaseline: data.meetsBaseline,
        timestamp: data.timestamp,
      }
      
      setCurrentScore(score)
      
      // Add to history
      setHistory(prev => [
        ...prev,
        {
          timestamp: data.timestamp,
          confidence: data.overallConfidence,
          phase: currentPhase,
        },
      ])
    }, [currentPhase]),

    onPhaseChange: useCallback((data: any) => {
      setCurrentPhase(data.phase)
    }, []),

    onWorkflowUpdate: useCallback((data: any) => {
      if (data.phase) {
        setCurrentPhase(data.phase)
      }
    }, []),

    onError: useCallback((error: any) => {
      console.error('WebSocket error in confidence updates:', error)
    }, []),
  }

  const { isConnected, connectionState, reconnect } = useWebSocket(agentId, handlers)

  // Clear history when agent changes
  useEffect(() => {
    setHistory([])
    setCurrentScore(null)
    setCurrentPhase('requirements')
  }, [agentId])

  return {
    currentScore,
    history,
    currentPhase,
    isConnected,
    connectionState,
    reconnect,
  }
}

export default useConfidenceUpdates
