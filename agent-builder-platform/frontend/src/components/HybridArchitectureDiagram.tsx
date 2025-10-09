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

interface HybridArchitectureDiagramProps {
  services: ServiceNode[]
  connections: Connection[]
  title?: string
  width?: number
  height?: number
}

export default function HybridArchitectureDiagram({
  services,
  connections,
  title,
  height = 600,
}: HybridArchitectureDiagramProps) {
  const theme = useTheme()

  const getServiceById = (id: string) => services.find((s) => s.id === id)

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
              <polygon points="0 0, 10 3, 0 6" fill={theme.palette.primary.main} />
            </marker>
          </defs>

          {connections.map((conn, idx) => {
            const fromService = getServiceById(conn.from)
            const toService = getServiceById(conn.to)

            if (!fromService || !toService) return null

            // Calculate center points based on service type
            // AWS icons: 90px wide × 110px tall. Generic boxes: 90px wide × 45px tall
            const fromCenterX = fromService.x + (fromService.type === 'aws' ? 45 : 45)
            const fromCenterY = fromService.y + (fromService.type === 'aws' ? 55 : 22.5)
            const toCenterX = toService.x + (toService.type === 'aws' ? 45 : 45)
            const toCenterY = toService.y + (toService.type === 'aws' ? 55 : 22.5)

            return (
              <g key={idx}>
                <line
                  x1={fromCenterX}
                  y1={fromCenterY}
                  x2={toCenterX}
                  y2={toCenterY}
                  stroke={theme.palette.primary.main}
                  strokeWidth={2}
                  strokeDasharray={conn.dashed ? '5,5' : undefined}
                  markerEnd="url(#arrowhead)"
                />
                {conn.label && (
                  <text
                    x={(fromCenterX + toCenterX) / 2}
                    y={(fromCenterY + toCenterY) / 2 - 8}
                    fill={theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.4)'}
                    fontSize="11"
                    fontWeight="400"
                    textAnchor="middle"
                    style={{ userSelect: 'none' }}
                  >
                    {conn.label}
                  </text>
                )}
              </g>
            )
          })}
        </svg>

        {/* Service nodes */}
        {services.map((service) => {
          const isAWS = service.type === 'aws' && service.icon
          const IconComponent = service.icon

          return (
            <Tooltip key={service.id} title={service.description || service.name} arrow placement="top">
              {isAWS && IconComponent ? (
                // AWS Service Icon with glassmorphism
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
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px) scale(1.05)',
                      zIndex: 10,
                    },
                    '&:hover .service-label': {
                      fontWeight: 600,
                      color: 'primary.main',
                    },
                    '&:hover .icon-container svg': {
                      filter: theme.palette.mode === 'dark'
                        ? 'drop-shadow(0px 0px 20px rgba(66, 153, 225, 0.9)) drop-shadow(0px 0px 40px rgba(66, 153, 225, 0.5)) drop-shadow(0px 6px 20px rgba(0,0,0,0.6)) brightness(1.2) contrast(1.1)'
                        : 'drop-shadow(0px 0px 16px rgba(66, 153, 225, 0.7)) drop-shadow(0px 0px 32px rgba(66, 153, 225, 0.4)) drop-shadow(0px 6px 16px rgba(0,0,0,0.3)) brightness(1.1) contrast(1.15)',
                    },
                  }}
                >
                  <Box
                    className="icon-container"
                    sx={{
                      width: 80,
                      height: 80,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      transition: 'all 0.3s ease',
                      '& svg': {
                        width: '80px',
                        height: '80px',
                        filter: theme.palette.mode === 'dark'
                          ? 'drop-shadow(0px 0px 12px rgba(66, 153, 225, 0.6)) drop-shadow(0px 4px 16px rgba(0,0,0,0.4)) brightness(1.1) contrast(1.05)'
                          : 'drop-shadow(0px 0px 8px rgba(66, 153, 225, 0.4)) drop-shadow(0px 4px 12px rgba(0,0,0,0.2)) brightness(1.05) contrast(1.1)',
                        transition: 'all 0.3s ease',
                      },
                    }}
                  >
                    <IconComponent size={80} />
                  </Box>
                  <Typography
                    className="service-label"
                    variant="caption"
                    sx={{
                      mt: 1,
                      fontSize: '0.65rem',
                      textAlign: 'center',
                      lineHeight: 1.1,
                      maxWidth: '100%',
                      height: '2.2em',
                      overflow: 'hidden',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      px: 0.5,
                      fontWeight: 500,
                      transition: 'all 0.2s',
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
    </Paper>
  )
}

export type { ServiceNode, Connection }
