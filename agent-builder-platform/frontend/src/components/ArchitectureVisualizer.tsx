import { useEffect, useRef, useState, useCallback } from 'react'
import {
  Box,
  Paper,
  CircularProgress,
  Alert,
  IconButton,
  Tooltip,
  Stack,
  Menu,
  MenuItem,
  Divider,
  Typography,
} from '@mui/material'
import {
  ZoomIn,
  ZoomOut,
  ZoomOutMap,
  Download,
  Fullscreen,
  FullscreenExit,
  Refresh,
} from '@mui/icons-material'
import mermaid from 'mermaid'

interface ArchitectureVisualizerProps {
  chart: string
  title?: string
  onServiceClick?: (serviceName: string) => void
}

interface DiagramTemplate {
  id: string
  name: string
  description: string
  diagram: string
}

// Initialize mermaid with enhanced settings
mermaid.initialize({
  startOnLoad: false,
  theme: 'default',
  securityLevel: 'loose',
  fontFamily: 'Inter, sans-serif',
  flowchart: {
    useMaxWidth: false,
    htmlLabels: true,
    curve: 'basis',
  },
})

export default function ArchitectureVisualizer({
  chart,
  title,
  onServiceClick,
}: ArchitectureVisualizerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const svgRef = useRef<SVGElement | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [isDragging, setIsDragging] = useState(false)
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 })
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [exportMenuAnchor, setExportMenuAnchor] = useState<null | HTMLElement>(null)

  // Render diagram
  const renderDiagram = useCallback(async () => {
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
        
        // Get SVG element reference
        const svgElement = containerRef.current.querySelector('svg')
        if (svgElement) {
          svgRef.current = svgElement
          
          // Make interactive - add click handlers to nodes
          if (onServiceClick) {
            const nodes = svgElement.querySelectorAll('.node')
            nodes.forEach((node) => {
              const textElement = node.querySelector('text')
              if (textElement) {
                const serviceName = textElement.textContent || ''
                node.addEventListener('click', () => {
                  onServiceClick(serviceName)
                })
                // Add cursor pointer style
                ;(node as HTMLElement).style.cursor = 'pointer'
              }
            })
          }
        }
      }

      setLoading(false)
    } catch (err) {
      console.error('Mermaid rendering error:', err)
      setError('Failed to render diagram. Please check the diagram syntax.')
      setLoading(false)
    }
  }, [chart, onServiceClick])

  useEffect(() => {
    renderDiagram()
  }, [renderDiagram])

  // Zoom controls
  const handleZoomIn = () => {
    setZoom((prev) => Math.min(prev + 0.2, 3))
  }

  const handleZoomOut = () => {
    setZoom((prev) => Math.max(prev - 0.2, 0.5))
  }

  const handleResetZoom = () => {
    setZoom(1)
    setPan({ x: 0, y: 0 })
  }

  // Pan controls
  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true)
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y })
  }

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      setPan({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y,
      })
    }
  }

  const handleMouseUp = () => {
    setIsDragging(false)
  }

  // Fullscreen toggle
  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen)
  }

  // Export functionality
  const handleExportClick = (event: React.MouseEvent<HTMLElement>) => {
    setExportMenuAnchor(event.currentTarget)
  }

  const handleExportClose = () => {
    setExportMenuAnchor(null)
  }

  const exportAsPNG = async () => {
    if (!svgRef.current) return

    try {
      const svgData = new XMLSerializer().serializeToString(svgRef.current)
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      const img = new Image()

      const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' })
      const url = URL.createObjectURL(svgBlob)

      img.onload = () => {
        canvas.width = img.width * 2 // 2x for better quality
        canvas.height = img.height * 2
        ctx?.scale(2, 2)
        ctx?.drawImage(img, 0, 0)
        URL.revokeObjectURL(url)

        canvas.toBlob((blob) => {
          if (blob) {
            const link = document.createElement('a')
            link.download = `architecture-diagram-${Date.now()}.png`
            link.href = URL.createObjectURL(blob)
            link.click()
          }
        })
      }

      img.src = url
    } catch (err) {
      console.error('Export PNG error:', err)
    }
    handleExportClose()
  }

  const exportAsSVG = () => {
    if (!svgRef.current) return

    try {
      const svgData = new XMLSerializer().serializeToString(svgRef.current)
      const blob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' })
      const link = document.createElement('a')
      link.download = `architecture-diagram-${Date.now()}.svg`
      link.href = URL.createObjectURL(blob)
      link.click()
    } catch (err) {
      console.error('Export SVG error:', err)
    }
    handleExportClose()
  }

  const exportAsPDF = async () => {
    // Note: For PDF export, you would typically use a library like jsPDF
    // For now, we'll just show an alert
    alert('PDF export requires additional setup. Use PNG or SVG export for now.')
    handleExportClose()
  }

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
        bgcolor: 'background.default',
        border: 1,
        borderColor: 'divider',
        position: isFullscreen ? 'fixed' : 'relative',
        top: isFullscreen ? 0 : 'auto',
        left: isFullscreen ? 0 : 'auto',
        right: isFullscreen ? 0 : 'auto',
        bottom: isFullscreen ? 0 : 'auto',
        zIndex: isFullscreen ? 1300 : 'auto',
        display: 'flex',
        flexDirection: 'column',
        minHeight: isFullscreen ? '100vh' : 400,
      }}
    >
      {/* Title and Controls */}
      <Box
        sx={{
          p: 2,
          borderBottom: 1,
          borderColor: 'divider',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        {title && (
          <Typography variant="h6" component="h3">
            {title}
          </Typography>
        )}
        <Stack direction="row" spacing={1}>
          <Tooltip title="Zoom In">
            <IconButton size="small" onClick={handleZoomIn} disabled={zoom >= 3}>
              <ZoomIn />
            </IconButton>
          </Tooltip>
          <Tooltip title="Zoom Out">
            <IconButton size="small" onClick={handleZoomOut} disabled={zoom <= 0.5}>
              <ZoomOut />
            </IconButton>
          </Tooltip>
          <Tooltip title="Reset View">
            <IconButton size="small" onClick={handleResetZoom}>
              <ZoomOutMap />
            </IconButton>
          </Tooltip>
          <Divider orientation="vertical" flexItem />
          <Tooltip title="Refresh Diagram">
            <IconButton size="small" onClick={renderDiagram}>
              <Refresh />
            </IconButton>
          </Tooltip>
          <Tooltip title="Export">
            <IconButton size="small" onClick={handleExportClick}>
              <Download />
            </IconButton>
          </Tooltip>
          <Tooltip title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}>
            <IconButton size="small" onClick={toggleFullscreen}>
              {isFullscreen ? <FullscreenExit /> : <Fullscreen />}
            </IconButton>
          </Tooltip>
        </Stack>
      </Box>

      {/* Export Menu */}
      <Menu
        anchorEl={exportMenuAnchor}
        open={Boolean(exportMenuAnchor)}
        onClose={handleExportClose}
      >
        <MenuItem onClick={exportAsPNG}>Export as PNG</MenuItem>
        <MenuItem onClick={exportAsSVG}>Export as SVG</MenuItem>
        <MenuItem onClick={exportAsPDF}>Export as PDF</MenuItem>
      </Menu>

      {/* Diagram Container */}
      <Box
        sx={{
          flex: 1,
          position: 'relative',
          overflow: 'hidden',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: isDragging ? 'grabbing' : 'grab',
        }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        {loading && (
          <CircularProgress
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
            }}
          />
        )}
        <Box
          ref={containerRef}
          sx={{
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
            transformOrigin: 'center',
            transition: isDragging ? 'none' : 'transform 0.2s ease',
            display: loading ? 'none' : 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            '& svg': {
              maxWidth: '100%',
              height: 'auto',
            },
          }}
        />
      </Box>

      {/* Zoom indicator */}
      <Box
        sx={{
          position: 'absolute',
          bottom: 16,
          right: 16,
          bgcolor: 'background.paper',
          px: 2,
          py: 1,
          borderRadius: 1,
          border: 1,
          borderColor: 'divider',
          fontSize: '0.875rem',
        }}
      >
        {Math.round(zoom * 100)}%
      </Box>
    </Paper>
  )
}
