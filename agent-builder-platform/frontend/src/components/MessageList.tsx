import { Box, Avatar, Typography, Paper, Chip } from '@mui/material'
import { Person, CheckCircle, Warning } from '@mui/icons-material'
import { Message } from './ChatInterface'
import CodeBlock from './CodeBlock'
import MermaidDiagram from './MermaidDiagram'

interface MessageListProps {
  messages: Message[]
  agentConfig: any
}

export default function MessageList({ messages, agentConfig }: MessageListProps) {
  const parseMessageContent = (content: string) => {
    const parts: Array<{ type: 'text' | 'code' | 'mermaid'; content: string; language?: string }> = []
    
    // Match code blocks with language
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g
    let lastIndex = 0
    let match

    while ((match = codeBlockRegex.exec(content)) !== null) {
      // Add text before code block
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: content.substring(lastIndex, match.index),
        })
      }

      const language = match[1] || 'text'
      const code = match[2]

      // Check if it's a mermaid diagram
      if (language === 'mermaid') {
        parts.push({
          type: 'mermaid',
          content: code,
        })
      } else {
        parts.push({
          type: 'code',
          content: code,
          language,
        })
      }

      lastIndex = match.index + match[0].length
    }

    // Add remaining text
    if (lastIndex < content.length) {
      parts.push({
        type: 'text',
        content: content.substring(lastIndex),
      })
    }

    return parts.length > 0 ? parts : [{ type: 'text' as const, content }]
  }

  return (
    <>
      {messages.map((message) => {
        const isUser = message.role === 'user'
        const agent = message.agent ? agentConfig[message.agent] : null
        const AgentIcon = agent?.icon
        const parts = parseMessageContent(message.content)

        return (
          <Box
            key={message.id}
            sx={{
              display: 'flex',
              gap: 2,
              mb: 3,
              flexDirection: isUser ? 'row-reverse' : 'row',
            }}
          >
            {/* Avatar */}
            <Avatar
              sx={{
                bgcolor: isUser ? 'primary.main' : agent?.color || 'secondary.main',
                width: 40,
                height: 40,
              }}
            >
              {isUser ? <Person /> : AgentIcon ? <AgentIcon /> : null}
            </Avatar>

            {/* Message Content */}
            <Box sx={{ flex: 1, maxWidth: '80%' }}>
              {/* Agent Name */}
              {!isUser && agent && (
                <Typography variant="caption" color="text.secondary" sx={{ mb: 0.5, display: 'block' }}>
                  {agent.name}
                </Typography>
              )}

              {/* Message Bubble */}
              <Paper
                elevation={1}
                sx={{
                  p: 2,
                  bgcolor: isUser ? 'primary.light' : 'background.paper',
                  color: isUser ? 'primary.contrastText' : 'text.primary',
                }}
              >
                {parts.map((part, index) => {
                  if (part.type === 'code') {
                    return <CodeBlock key={index} code={part.content} language={part.language || 'text'} />
                  } else if (part.type === 'mermaid') {
                    return <MermaidDiagram key={index} chart={part.content} />
                  } else {
                    return (
                      <Typography
                        key={index}
                        variant="body1"
                        sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}
                      >
                        {part.content}
                      </Typography>
                    )
                  }
                })}

                {/* Confidence Badge */}
                {message.confidence !== undefined && (
                  <Box sx={{ mt: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                    {message.confidence >= 0.95 ? (
                      <CheckCircle sx={{ fontSize: 16, color: 'success.main' }} />
                    ) : (
                      <Warning sx={{ fontSize: 16, color: 'warning.main' }} />
                    )}
                    <Typography variant="caption" color="text.secondary">
                      Confidence: {(message.confidence * 100).toFixed(0)}%
                    </Typography>
                  </Box>
                )}

                {/* Assumptions */}
                {message.assumptions && message.assumptions.length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
                      Assumptions:
                    </Typography>
                    {message.assumptions.map((assumption, idx) => (
                      <Chip
                        key={idx}
                        label={assumption}
                        size="small"
                        icon={<Warning />}
                        sx={{ mr: 0.5, mb: 0.5 }}
                        color="warning"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                )}
              </Paper>

              {/* Timestamp */}
              <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                {message.timestamp.toLocaleTimeString()}
              </Typography>
            </Box>
          </Box>
        )
      })}
    </>
  )
}
