import { useEffect, useRef } from 'react'
import { Box } from '@mui/material'

interface LiveRegionProps {
  message: string
  priority?: 'polite' | 'assertive'
  clearAfter?: number
}

export const LiveRegion = ({ message, priority = 'polite', clearAfter = 5000 }: LiveRegionProps) => {
  const timeoutRef = useRef<ReturnType<typeof setTimeout>>()

  useEffect(() => {
    if (clearAfter && message) {
      timeoutRef.current = setTimeout(() => {
        // Message will be cleared by parent component
      }, clearAfter)
    }

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [message, clearAfter])

  if (!message) return null

  return (
    <Box
      role="status"
      aria-live={priority}
      aria-atomic="true"
      sx={{
        position: 'absolute',
        left: '-10000px',
        width: '1px',
        height: '1px',
        overflow: 'hidden',
      }}
    >
      {message}
    </Box>
  )
}

export default LiveRegion
