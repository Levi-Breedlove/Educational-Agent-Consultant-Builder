import { useEffect, useRef, useState } from 'react'
import { Box, Paper, CircularProgress, Alert } from '@mui/material'
import mermaid from 'mermaid'

interface MermaidDiagramProps {
  chart: string
}

// Initialize mermaid
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  fontFamily: 'Inter, sans-serif',
})

export default function MermaidDiagram({ chart }: MermaidDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const renderDiagram = async () => {
      if (!containerRef.current) return

      try {
        setLoading(true)
        setError(null)

        // Generate unique ID for this diagram
        const id = `mermaid-${Math.random().toString(36).substring(2, 11)}`

        // Render the diagram
        const { svg } = await mermaid.render(id, chart)

        // Insert the SVG
        if (containerRef.current) {
          containerRef.current.innerHTML = svg
        }

        setLoading(false)
      } catch (err) {
        console.error('Mermaid rendering error:', err)
        setError('Failed to render diagram')
        setLoading(false)
      }
    }

    renderDiagram()
  }, [chart])

  if (error) {
    return (
      <Alert severity="error" sx={{ my: 2 }}>
        {error}
      </Alert>
    )
  }

  return (
    <Paper
      elevation={0}
      sx={{
        my: 2,
        p: 2,
        bgcolor: 'background.default',
        border: 1,
        borderColor: 'divider',
        position: 'relative',
        minHeight: 200,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {loading && <CircularProgress />}
      <Box
        ref={containerRef}
        sx={{
          width: '100%',
          display: loading ? 'none' : 'flex',
          justifyContent: 'center',
          '& svg': {
            maxWidth: '100%',
            height: 'auto',
          },
        }}
      />
    </Paper>
  )
}
