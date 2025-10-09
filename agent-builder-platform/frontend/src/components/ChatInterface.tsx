import { useState, useEffect, useRef } from 'react'
import {
  Box,
  TextField,
  IconButton,
  Typography,
  Chip,
  CircularProgress,
} from '@mui/material'
import { Send, Psychology, Architecture, Code, BugReport, Build } from '@mui/icons-material'
import { useSelector, useDispatch } from 'react-redux'
import { RootState } from '../store'
import MessageList from './MessageList'
import { useWebSocket } from '../hooks/useWebSocket'
import { setPhase, completePhase, setProgress, WorkflowPhase } from '../store/slices/workflowSlice'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  agent?: 'manager' | 'solutions_architect' | 'architecture_advisor' | 'implementation_guide' | 'testing_validator'
  timestamp: Date
  confidence?: number
  assumptions?: string[]
  isStreaming?: boolean
}

const agentConfig = {
  manager: {
    name: 'Manager Agent',
    icon: Psychology,
    color: '#1976d2',
    description: 'Orchestrates the workflow',
  },
  solutions_architect: {
    name: 'AWS Solutions Architect',
    icon: Architecture,
    color: '#2e7d32',
    description: 'AWS architecture expert',
  },
  architecture_advisor: {
    name: 'Architecture Advisor',
    icon: Build,
    color: '#ed6c02',
    description: 'Well-Architected Framework specialist',
  },
  implementation_guide: {
    name: 'Implementation Guide',
    icon: Code,
    color: '#9c27b0',
    description: 'Senior developer',
  },
  testing_validator: {
    name: 'Testing Validator',
    icon: BugReport,
    color: '#d32f2f',
    description: 'DevOps & security expert',
  },
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  const dispatch = useDispatch()
  const sessionId = useSelector((state: RootState) => state.session.sessionId)
  const agentId = useSelector((state: RootState) => state.session.agentId)
  const currentPhase = useSelector((state: RootState) => state.workflow.currentPhase)

  const { sendMessage, lastMessage, isConnected } = useWebSocket(agentId || '')

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Handle incoming WebSocket messages
  useEffect(() => {
    if (!lastMessage) return

    const data = JSON.parse(lastMessage.data)

    switch (data.type) {
      case 'ai_response_chunk':
        handleStreamingChunk(data)
        break
      case 'ai_response_complete':
        handleStreamingComplete(data)
        break
      case 'workflow_update':
      case 'phase_change':
        handleWorkflowUpdate(data)
        break
      case 'progress_update':
        if (data.progress !== undefined) {
          dispatch(setProgress(data.progress))
        }
        break
      case 'error':
        handleError(data)
        break
    }
  }, [lastMessage])

  const handleStreamingChunk = (data: any) => {
    setMessages((prev) => {
      const lastMsg = prev[prev.length - 1]
      if (lastMsg && lastMsg.isStreaming) {
        return [
          ...prev.slice(0, -1),
          {
            ...lastMsg,
            content: lastMsg.content + data.content,
          },
        ]
      } else {
        return [
          ...prev,
          {
            id: data.message_id || `msg-${Date.now()}`,
            role: 'assistant',
            content: data.content,
            agent: data.agent,
            timestamp: new Date(),
            isStreaming: true,
          },
        ]
      }
    })
    setIsTyping(true)
  }

  const handleStreamingComplete = (data: any) => {
    setMessages((prev) => {
      const lastMsg = prev[prev.length - 1]
      if (lastMsg && lastMsg.isStreaming) {
        return [
          ...prev.slice(0, -1),
          {
            ...lastMsg,
            isStreaming: false,
            confidence: data.confidence,
            assumptions: data.assumptions,
          },
        ]
      }
      return prev
    })
    setIsTyping(false)
  }

  const handleWorkflowUpdate = (data: any) => {
    // Update Redux workflow state
    if (data.phase) {
      dispatch(setPhase(data.phase as WorkflowPhase))
    }
    if (data.completed_phase) {
      dispatch(completePhase(data.completed_phase as WorkflowPhase))
    }
    if (data.progress !== undefined) {
      dispatch(setProgress(data.progress))
    }

    // Add system message for workflow updates
    setMessages((prev) => [
      ...prev,
      {
        id: `system-${Date.now()}`,
        role: 'assistant',
        content: data.message || `Workflow updated: ${data.phase}`,
        timestamp: new Date(),
      },
    ])
  }

  const handleError = (data: any) => {
    setMessages((prev) => [
      ...prev,
      {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: `Error: ${data.message}`,
        timestamp: new Date(),
      },
    ])
    setIsTyping(false)
  }

  const handleSendMessage = () => {
    if (!input.trim() || !isConnected) return

    // Add user message
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: input,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])

    // Send via WebSocket
    sendMessage({
      type: 'user_message',
      content: input,
      phase: currentPhase,
      session_id: sessionId,
    })

    setInput('')
    setIsTyping(true)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <Box sx={{ p: 2.5, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="h6" sx={{ mb: 1.5 }}>Agent Consultation</Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {Object.entries(agentConfig).map(([key, config]) => {
            const Icon = config.icon
            return (
              <Chip
                key={key}
                icon={<Icon />}
                label={config.name}
                size="small"
                sx={{
                  bgcolor: `${config.color}20`,
                  color: config.color,
                  '& .MuiChip-icon': { color: config.color },
                }}
              />
            )
          })}
        </Box>
      </Box>

      {/* Messages */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        <MessageList messages={messages} agentConfig={agentConfig} />
        {isTyping && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 2 }}>
            <CircularProgress size={20} />
            <Typography variant="body2" color="text.secondary">
              Agent is thinking...
            </Typography>
          </Box>
        )}
        <div ref={messagesEndRef} />
      </Box>

      {/* Input */}
      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder="Describe your agent requirements..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={!isConnected}
          />
          <IconButton
            color="primary"
            onClick={handleSendMessage}
            disabled={!input.trim() || !isConnected}
          >
            <Send />
          </IconButton>
        </Box>
        {!isConnected && (
          <Typography variant="caption" color="error" sx={{ mt: 1, display: 'block' }}>
            Connecting to backend...
          </Typography>
        )}
      </Box>
    </Box>
  )
}
