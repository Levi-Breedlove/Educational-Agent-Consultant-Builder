import React from 'react'
import { Box, Paper, Typography, Tooltip, useTheme } from '@mui/material'

interface ServiceNode {
  id: string
  name: string
  icon?: React.ComponentType<{ size?: number | string; color?: string }>
  type?: 'aws' | 'generic' // AWS icon or generic text box
  description?: string
  x: number
  y: number
}

interface Connection {
  from: string
  to: string
  label?: string
  dashed?: boolean
}

interface AWSArchitectureDiagramProps {
  services: ServiceNode[]
  connections: Connection[]
  title?: string
  height?: number
}

export default function AWSArchitectureDiagram({
  services,
  connections,
  title,
  height = 600,
}: AWSArchitectureDiagramProps) {
  const theme = useTheme()
  const [zoom, setZoom] = React.useState(1)
  const [pan, setPan] = React.useState({ x: 0, y: 0 })
  const [isDragging, setIsDragging] = React.useState(false)
  const [dragStart, setDragStart] = React.useState({ x: 0, y: 0 })

  const getServiceById = (id: string) => services.find(s => s.id === id)

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

  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? 0.9 : 1.1
    setZoom(prev => Math.max(0.5, Math.min(3, prev * delta)))
  }

  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        bgcolor: 'background.default',
        border: 1,
        borderColor: 'divider',
      }}
    >
      {title && (
        <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
          {title}
        </Typography>
      )}
      
      <Box
        sx={{
          position: 'relative',
          width: '100%',
          height: height,
          bgcolor: theme.palette.mode === 'dark' ? '#000000' : 'grey.50',
          borderRadius: 1,
          overflow: 'hidden',
          cursor: isDragging ? 'grabbing' : 'grab',
        }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      >
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
            transformOrigin: 'center',
            transition: isDragging ? 'none' : 'transform 0.1s ease',
          }}
        >
          {/* SVG for connections */}
          <svg
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              pointerEvents: 'none',
            }}
          >
          <defs>
            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="10"
              refX="9"
              refY="3"
              orient="auto"
            >
              <polygon
                points="0 0, 10 3, 0 6"
                fill={theme.palette.primary.main}
              />
            </marker>
          </defs>
          
          {connections.map((conn, idx) => {
            const fromService = getServiceById(conn.from)
            const toService = getServiceById(conn.to)
            
            if (!fromService || !toService) return null
            
            // Calculate center based on node type
            // All nodes now use AWS icons with consistent sizing
            const fromIsAWS = (fromService.type === 'aws' || (!fromService.type && fromService.icon)) && fromService.icon
            const toIsAWS = (toService.type === 'aws' || (!toService.type && toService.icon)) && toService.icon
            
            // AWS icons: 90px wide container, center at 45px
            // Total height: 110px (70px icon + 40px label space), center at 55px
            const x1 = fromService.x + (fromIsAWS ? 45 : 45)
            const y1 = fromService.y + (fromIsAWS ? 55 : 22.5)
            const x2 = toService.x + (toIsAWS ? 45 : 45)
            const y2 = toService.y + (toIsAWS ? 55 : 22.5)
            
            // Calculate label position with intelligent offset to avoid icon overlap
            const midX = (x1 + x2) / 2
            const midY = (y1 + y2) / 2
            
            // Check if label would overlap with any service icon
            const labelOffset = 12 // Base offset from line
            let labelY = midY - labelOffset
            
            // Check for potential icon collisions and adjust label position
            const checkIconCollision = (x: number, y: number) => {
              return services.some(service => {
                const iconX = service.x
                const iconY = service.y
                const iconWidth = 90
                const iconHeight = 110
                
                // Check if label point is within icon bounds (with padding)
                const padding = 15
                return (
                  x >= iconX - padding &&
                  x <= iconX + iconWidth + padding &&
                  y >= iconY - padding &&
                  y <= iconY + iconHeight + padding
                )
              })
            }
            
            // If label collides with an icon, try alternative positions
            if (checkIconCollision(midX, labelY)) {
              // Try below the line
              const belowY = midY + labelOffset + 8
              if (!checkIconCollision(midX, belowY)) {
                labelY = belowY
              } else {
                // Try offset to the side
                const angle = Math.atan2(y2 - y1, x2 - x1)
                const perpX = midX + Math.cos(angle + Math.PI / 2) * 20
                const perpY = midY + Math.sin(angle + Math.PI / 2) * 20
                
                if (!checkIconCollision(perpX, perpY)) {
                  // Use perpendicular offset
                  labelY = perpY
                }
              }
            }
            
            return (
              <g key={idx}>
                <line
                  x1={x1}
                  y1={y1}
                  x2={x2}
                  y2={y2}
                  stroke={theme.palette.primary.main}
                  strokeWidth={2}
                  strokeDasharray={conn.dashed ? '5,5' : undefined}
                  markerEnd="url(#arrowhead)"
                />
                {conn.label && (
                  <>
                    {/* Background for better readability */}
                    <rect
                      x={midX - (conn.label.length * 3.5)}
                      y={labelY - 10}
                      width={conn.label.length * 7}
                      height={16}
                      fill={theme.palette.mode === 'dark' ? 'rgba(0,0,0,0.7)' : 'rgba(255,255,255,0.85)'}
                      rx={3}
                    />
                    <text
                      x={midX}
                      y={labelY}
                      fill={theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.7)' : 'rgba(0,0,0,0.6)'}
                      fontSize="11"
                      fontWeight="500"
                      textAnchor="middle"
                      style={{ userSelect: 'none' }}
                    >
                      {conn.label}
                    </text>
                  </>
                )}
              </g>
            )
          })}
        </svg>

        {/* Service nodes */}
        {services.map((service) => {
          // If type is not specified but icon exists, assume it's AWS
          const isAWS = (service.type === 'aws' || (!service.type && service.icon)) && service.icon
          const IconComponent = service.icon
          
          return (
            <Tooltip
              key={service.id}
              title={service.description || service.name}
              arrow
              placement="top"
            >
              {isAWS && IconComponent ? (
                // AWS Service Icon (clean, no box)
                <Box
                  sx={{
                    position: 'absolute',
                    left: service.x,
                    top: service.y,
                    width: 90,
                    height: 110,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'flex-start',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    '&:hover': {
                      transform: 'scale(1.05)',
                      zIndex: 10,
                    },
                    '&:hover .service-label': {
                      fontWeight: 600,
                      color: 'primary.main',
                    },
                  }}
                >
                  <Box
                    sx={{
                      width: 70,
                      height: 70,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mb: 0.5,
                      '& svg': {
                        width: '100%',
                        height: '100%',
                        filter: 'drop-shadow(0px 2px 4px rgba(0,0,0,0.1))',
                      },
                    }}
                  >
                    <IconComponent size={70} />
                  </Box>
                  <Typography
                    className="service-label"
                    variant="caption"
                    sx={{
                      fontSize: '0.7rem',
                      textAlign: 'center',
                      lineHeight: 1.2,
                      maxWidth: '100%',
                      minHeight: '2.4em',
                      overflow: 'hidden',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      px: 0.5,
                      fontWeight: 500,
                      transition: 'all 0.2s',
                      wordBreak: 'break-word',
                    }}
                  >
                    {service.name}
                  </Typography>
                </Box>
              ) : (
                // Generic Text Box (for Client, User, etc.)
                <Box
                  sx={{
                    position: 'absolute',
                    left: service.x,
                    top: service.y,
                    minWidth: 90,
                    height: 45,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    bgcolor: theme.palette.mode === 'dark' ? 'grey.800' : 'grey.100',
                    border: 2,
                    borderColor: theme.palette.mode === 'dark' ? 'grey.700' : 'grey.300',
                    borderRadius: 2,
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    px: 2,
                    '&:hover': {
                      borderColor: 'primary.main',
                      bgcolor: theme.palette.mode === 'dark' ? 'grey.700' : 'grey.200',
                      transform: 'scale(1.02)',
                      zIndex: 10,
                    },
                  }}
                >
                  <Typography
                    variant="caption"
                    sx={{
                      fontWeight: 600,
                      textAlign: 'center',
                      color: 'text.primary',
                      fontSize: '0.75rem',
                    }}
                  >
                    {service.name}
                  </Typography>
                </Box>
              )}
            </Tooltip>
          )
        })}
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
            pointerEvents: 'none',
          }}
        >
          {Math.round(zoom * 100)}%
        </Box>
      </Box>
    </Paper>
  )
}

export type { ServiceNode, Connection }
