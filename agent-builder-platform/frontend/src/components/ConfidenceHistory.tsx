import React from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  useTheme,
  Chip,
  Stack,
} from '@mui/material'
import {
  Timeline as TimelineIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Remove as RemoveIcon,
} from '@mui/icons-material'

/**
 * Historical confidence data point
 */
export interface ConfidenceHistoryPoint {
  timestamp: string
  confidence: number
  phase: string
}

export interface ConfidenceHistoryProps {
  history: ConfidenceHistoryPoint[]
  height?: number
}

/**
 * Get phase color
 */
const getPhaseColor = (phase: string, theme: any): string => {
  const phaseColors: Record<string, string> = {
    requirements: theme.palette.info.main,
    architecture: theme.palette.secondary.main,
    implementation: theme.palette.primary.main,
    testing: theme.palette.warning.main,
    deployment: theme.palette.success.main,
  }
  return phaseColors[phase.toLowerCase()] || theme.palette.text.secondary
}

/**
 * Confidence History Chart Component
 * 
 * Displays confidence trends over time with phase markers.
 * Simple line chart visualization without external dependencies.
 * 
 * Requirements: 20.11
 */
export const ConfidenceHistory: React.FC<ConfidenceHistoryProps> = ({
  history,
  height = 200,
}) => {
  const theme = useTheme()

  if (history.length === 0) {
    return (
      <Card elevation={1}>
        <CardContent>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              mb: 2,
            }}
          >
            <TimelineIcon />
            <Typography variant="h6">Confidence History</Typography>
          </Box>
          <Typography variant="body2" color="text.secondary">
            No historical data available yet. Confidence tracking will appear as you progress.
          </Typography>
        </CardContent>
      </Card>
    )
  }

  // Calculate statistics
  const minConfidence = Math.min(...history.map(p => p.confidence))
  const maxConfidence = Math.max(...history.map(p => p.confidence))
  const avgConfidence = history.reduce((sum, p) => sum + p.confidence, 0) / history.length
  const currentConfidence = history[history.length - 1].confidence
  const previousConfidence = history.length > 1 ? history[history.length - 2].confidence : currentConfidence
  const trend = currentConfidence > previousConfidence + 0.01 ? 'up' 
    : currentConfidence < previousConfidence - 0.01 ? 'down' 
    : 'stable'

  // Prepare chart data - use pixel values for proper text rendering
  const chartWidth = 800 // pixels
  const chartHeight = height
  const paddingLeft = 50 // More space for Y-axis labels
  const paddingRight = 20
  const paddingTop = 20
  const paddingBottom = 30
  const plotWidth = chartWidth - paddingLeft - paddingRight
  const plotHeight = chartHeight - paddingTop - paddingBottom

  // Use fixed scale from 80% to 100% for consistency
  const minY = 0.80
  const maxY = 1.00

  // Scale functions
  const xScale = (index: number) => {
    return paddingLeft + (index / Math.max(history.length - 1, 1)) * plotWidth
  }

  const yScale = (confidence: number) => {
    const normalized = (confidence - minY) / (maxY - minY)
    return chartHeight - paddingBottom - (normalized * plotHeight)
  }

  // Y-axis labels
  const yAxisLabels = [0.80, 0.85, 0.90, 0.95, 1.00]

  // Generate SVG path
  const pathData = history
    .map((point, index) => {
      const x = xScale(index)
      const y = yScale(point.confidence)
      return index === 0 ? `M ${x} ${y}` : `L ${x} ${y}`
    })
    .join(' ')

  // Generate area path (for gradient fill)
  const areaData = `${pathData} L ${xScale(history.length - 1)} ${chartHeight - paddingBottom} L ${paddingLeft} ${chartHeight - paddingBottom} Z`

  return (
    <Card elevation={1}>
      <CardContent>
        {/* Header */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            mb: 2,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <TimelineIcon />
            <Typography variant="h6">Confidence History</Typography>
          </Box>
          <Chip
            icon={
              trend === 'up' ? <TrendingUpIcon /> :
              trend === 'down' ? <TrendingDownIcon /> :
              <RemoveIcon />
            }
            label={
              trend === 'up' ? 'Trending Up' :
              trend === 'down' ? 'Trending Down' :
              'Stable'
            }
            size="small"
            color={
              trend === 'up' ? 'success' :
              trend === 'down' ? 'warning' :
              'default'
            }
          />
        </Box>

        {/* Statistics */}
        <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Current
            </Typography>
            <Typography variant="body2" fontWeight={600}>
              {(currentConfidence * 100).toFixed(1)}%
            </Typography>
          </Box>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Average
            </Typography>
            <Typography variant="body2" fontWeight={600}>
              {(avgConfidence * 100).toFixed(1)}%
            </Typography>
          </Box>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Min
            </Typography>
            <Typography variant="body2" fontWeight={600}>
              {(minConfidence * 100).toFixed(1)}%
            </Typography>
          </Box>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Max
            </Typography>
            <Typography variant="body2" fontWeight={600}>
              {(maxConfidence * 100).toFixed(1)}%
            </Typography>
          </Box>
        </Stack>

        {/* Chart */}
        <Box
          sx={{
            position: 'relative',
            width: '100%',
            height: chartHeight,
            backgroundColor: theme.palette.mode === 'dark' 
              ? 'rgba(255, 255, 255, 0.02)' 
              : 'rgba(0, 0, 0, 0.02)',
            borderRadius: 2,
            overflow: 'hidden',
          }}
          role="img"
          aria-label={`Confidence history chart showing trend from ${(minConfidence * 100).toFixed(1)}% to ${(currentConfidence * 100).toFixed(1)}%`}
        >
          <svg
            width="100%"
            height={chartHeight}
            viewBox={`0 0 ${chartWidth} ${chartHeight}`}
            preserveAspectRatio="xMidYMid meet"
          >
            {/* Y-axis grid lines and labels */}
            {yAxisLabels.map((value) => {
              const y = yScale(value)
              return (
                <g key={value}>
                  {/* Grid line */}
                  <line
                    x1={paddingLeft}
                    y1={y}
                    x2={chartWidth - paddingRight}
                    y2={y}
                    stroke={theme.palette.divider}
                    strokeWidth="1"
                    strokeDasharray="4,4"
                    opacity={0.3}
                  />
                  {/* Y-axis label */}
                  <text
                    x={paddingLeft - 10}
                    y={y + 5}
                    textAnchor="end"
                    fill={theme.palette.text.secondary}
                    fontSize="12"
                    fontFamily="Inter, sans-serif"
                    fontWeight={value === 0.95 ? 600 : 400}
                  >
                    {(value * 100).toFixed(0)}%
                  </text>
                </g>
              )
            })}

            {/* Baseline reference line at 95% - thicker */}
            <line
              x1={paddingLeft}
              y1={yScale(0.95)}
              x2={chartWidth - paddingRight}
              y2={yScale(0.95)}
              stroke={theme.palette.success.main}
              strokeWidth="2"
              strokeDasharray="8,4"
              opacity={0.6}
            />

            {/* Area gradient */}
            <defs>
              <linearGradient id="confidenceGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop
                  offset="0%"
                  stopColor={theme.palette.primary.main}
                  stopOpacity={0.3}
                />
                <stop
                  offset="100%"
                  stopColor={theme.palette.primary.main}
                  stopOpacity={0.05}
                />
              </linearGradient>
            </defs>

            {/* Area fill */}
            <path
              d={areaData}
              fill="url(#confidenceGradient)"
            />

            {/* Line */}
            <path
              d={pathData}
              fill="none"
              stroke={theme.palette.primary.main}
              strokeWidth="3"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* Data points */}
            {history.map((point, index) => (
              <g key={index}>
                <circle
                  cx={xScale(index)}
                  cy={yScale(point.confidence)}
                  r="5"
                  fill={getPhaseColor(point.phase, theme)}
                  stroke={theme.palette.background.paper}
                  strokeWidth="2"
                />
              </g>
            ))}
          </svg>
        </Box>

        {/* Phase legend */}
        <Stack direction="row" spacing={1} sx={{ mt: 2, flexWrap: 'wrap' }}>
          {Array.from(new Set(history.map(p => p.phase))).map(phase => (
            <Chip
              key={phase}
              label={phase}
              size="small"
              sx={{
                backgroundColor: getPhaseColor(phase, theme),
                color: theme.palette.getContrastText(getPhaseColor(phase, theme)),
                fontSize: '0.75rem',
              }}
            />
          ))}
        </Stack>
      </CardContent>
    </Card>
  )
}

export default ConfidenceHistory
