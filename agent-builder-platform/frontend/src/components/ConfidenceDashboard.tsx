import React from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  Stack,
  Tooltip,
  IconButton,
  Collapse,
  Alert,
  AlertTitle,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  useTheme,
} from '@mui/material'
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  Lightbulb as LightbulbIcon,
} from '@mui/icons-material'

/**
 * Confidence score breakdown by factor
 */
export interface ConfidenceFactors {
  informationCompleteness: number // 25% weight
  requirementClarity: number // 20% weight
  technicalFeasibility: number // 20% weight
  validationCoverage: number // 15% weight
  riskAssessment: number // 10% weight
  userAlignment: number // 10% weight
}

/**
 * Confidence score with transparency data
 */
export interface ConfidenceScore {
  overallConfidence: number // 0-1 (95%+ baseline)
  factors: ConfidenceFactors
  confidenceBoosters: string[] // What increases confidence
  uncertaintyFactors: string[] // What reduces confidence
  recommendedActions: string[] // How to improve confidence
  meetsBaseline: boolean // >= 95%
  timestamp: string
}

/**
 * Historical confidence data point
 */
export interface ConfidenceHistoryPoint {
  timestamp: string
  confidence: number
  phase: string
}

export interface ConfidenceDashboardProps {
  currentScore: ConfidenceScore
  history?: ConfidenceHistoryPoint[]
  showDetails?: boolean
  compact?: boolean
}

/**
 * Get color based on confidence level
 */
const getConfidenceColor = (confidence: number, theme: any): string => {
  if (confidence >= 0.95) return theme.palette.success.main
  if (confidence >= 0.85) return theme.palette.warning.main
  return theme.palette.error.main
}

/**
 * Get status icon based on confidence level
 */
const getConfidenceIcon = (confidence: number) => {
  if (confidence >= 0.95) return <CheckCircleIcon />
  if (confidence >= 0.85) return <WarningIcon />
  return <ErrorIcon />
}

/**
 * Format confidence percentage
 */
const formatConfidence = (value: number): string => {
  return `${(value * 100).toFixed(1)}%`
}

/**
 * Simple Line Chart Component for Confidence History
 */
const ConfidenceLineChart: React.FC<{ history: ConfidenceHistoryPoint[], theme: any }> = ({ history, theme }) => {
  if (history.length === 0) return null

  const width = 400
  const height = 120
  const padding = { top: 10, right: 10, bottom: 20, left: 40 }
  const chartWidth = width - padding.left - padding.right
  const chartHeight = height - padding.top - padding.bottom

  // Calculate scales
  const minConfidence = 0.8
  const maxConfidence = 1.0
  const xScale = chartWidth / (history.length - 1 || 1)
  const yScale = chartHeight / (maxConfidence - minConfidence)

  // Generate path
  const pathData = history
    .map((point, index) => {
      const x = padding.left + index * xScale
      const y = padding.top + chartHeight - (point.confidence - minConfidence) * yScale
      return `${index === 0 ? 'M' : 'L'} ${x} ${y}`
    })
    .join(' ')

  // Y-axis labels
  const yLabels = [0.80, 0.85, 0.90, 0.95, 1.00]

  return (
    <Box sx={{ width: '100%', display: 'flex', justifyContent: 'center', my: 2 }}>
      <svg width={width} height={height} style={{ overflow: 'visible' }}>
        {/* Y-axis grid lines and labels */}
        {yLabels.map((value) => {
          const y = padding.top + chartHeight - (value - minConfidence) * yScale
          return (
            <g key={value}>
              <line
                x1={padding.left}
                y1={y}
                x2={padding.left + chartWidth}
                y2={y}
                stroke={theme.palette.divider}
                strokeWidth={1}
                strokeDasharray="2,2"
              />
              <text
                x={padding.left - 5}
                y={y + 4}
                textAnchor="end"
                fontSize="10"
                fill={theme.palette.text.secondary}
              >
                {(value * 100).toFixed(0)}%
              </text>
            </g>
          )
        })}

        {/* Baseline threshold line at 95% */}
        <line
          x1={padding.left}
          y1={padding.top + chartHeight - (0.95 - minConfidence) * yScale}
          x2={padding.left + chartWidth}
          y2={padding.top + chartHeight - (0.95 - minConfidence) * yScale}
          stroke={theme.palette.success.main}
          strokeWidth={2}
          strokeDasharray="4,4"
          opacity={0.5}
        />

        {/* Line chart */}
        <path
          d={pathData}
          fill="none"
          stroke={theme.palette.primary.main}
          strokeWidth={2}
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Data points */}
        {history.map((point, index) => {
          const x = padding.left + index * xScale
          const y = padding.top + chartHeight - (point.confidence - minConfidence) * yScale
          const color = getConfidenceColor(point.confidence, theme)
          
          return (
            <circle
              key={index}
              cx={x}
              cy={y}
              r={4}
              fill={color}
              stroke={theme.palette.background.paper}
              strokeWidth={2}
            />
          )
        })}

        {/* X-axis */}
        <line
          x1={padding.left}
          y1={padding.top + chartHeight}
          x2={padding.left + chartWidth}
          y2={padding.top + chartHeight}
          stroke={theme.palette.divider}
          strokeWidth={1}
        />

        {/* Y-axis */}
        <line
          x1={padding.left}
          y1={padding.top}
          x2={padding.left}
          y2={padding.top + chartHeight}
          stroke={theme.palette.divider}
          strokeWidth={1}
        />
      </svg>
    </Box>
  )
}

/**
 * Confidence Dashboard Component
 * 
 * Displays real-time confidence scores with transparent breakdowns,
 * historical trends, and actionable recommendations.
 * 
 * Requirements: 20.2, 20.3, 20.11
 */
export const ConfidenceDashboard: React.FC<ConfidenceDashboardProps> = ({
  currentScore,
  history = [],
  showDetails = true,
  compact = false,
}) => {
  const theme = useTheme()
  const [expanded, setExpanded] = React.useState(!compact)
  const [showBoosters, setShowBoosters] = React.useState(false)
  const [showUncertainties, setShowUncertainties] = React.useState(false)
  const [showActions, setShowActions] = React.useState(false)

  const confidenceColor = getConfidenceColor(currentScore.overallConfidence, theme)
  const confidenceIcon = getConfidenceIcon(currentScore.overallConfidence)

  // Calculate trend from history
  const trend = React.useMemo(() => {
    if (history.length < 2) return 'stable'
    const recent = history.slice(-3)
    const avgRecent = recent.reduce((sum, p) => sum + p.confidence, 0) / recent.length
    const previous = history.slice(-6, -3)
    if (previous.length === 0) return 'stable'
    const avgPrevious = previous.reduce((sum, p) => sum + p.confidence, 0) / previous.length
    
    if (avgRecent > avgPrevious + 0.02) return 'up'
    if (avgRecent < avgPrevious - 0.02) return 'down'
    return 'stable'
  }, [history])

  return (
    <Card
      elevation={2}
      sx={{
        transition: 'all 0.3s ease',
      }}
      role="region"
      aria-label="Confidence Dashboard"
    >
      <CardContent>
        {/* Header with overall confidence */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            mb: 2,
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Box sx={{ color: confidenceColor }}>{confidenceIcon}</Box>
            <Typography variant="h6" component="h2">
              Confidence Score
            </Typography>
            <Tooltip title="Multi-factor confidence scoring with 95% baseline">
              <IconButton size="small" aria-label="Confidence information">
                <InfoIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {trend !== 'stable' && (
              <Chip
                icon={trend === 'up' ? <TrendingUpIcon /> : <TrendingDownIcon />}
                label={trend === 'up' ? 'Improving' : 'Declining'}
                size="small"
                color={trend === 'up' ? 'success' : 'warning'}
              />
            )}
            <Typography
              variant="h4"
              component="div"
              sx={{
                color: confidenceColor,
                fontWeight: 700,
              }}
              aria-live="polite"
              aria-atomic="true"
            >
              {formatConfidence(currentScore.overallConfidence)}
            </Typography>
          </Box>
        </Box>

        {/* Baseline status alert */}
        {!currentScore.meetsBaseline && (
          <Alert severity="warning" sx={{ mb: 2 }}>
            <AlertTitle>Below Baseline Threshold</AlertTitle>
            Confidence is below the 95% baseline. The system will ask clarifying
            questions to improve confidence before proceeding.
          </Alert>
        )}

        {/* Overall progress bar */}
        <Box sx={{ mb: 3 }}>
          <LinearProgress
            variant="determinate"
            value={currentScore.overallConfidence * 100}
            sx={{
              height: 8,
              borderRadius: 4,
              backgroundColor: theme.palette.mode === 'dark' 
                ? 'rgba(255, 255, 255, 0.1)' 
                : 'rgba(0, 0, 0, 0.1)',
              '& .MuiLinearProgress-bar': {
                backgroundColor: confidenceColor,
                borderRadius: 4,
              },
            }}
            aria-label={`Overall confidence: ${formatConfidence(currentScore.overallConfidence)}`}
          />
        </Box>

        {/* Confidence History Chart */}
        {history.length > 0 && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1, textAlign: 'center' }}>
              Confidence Trend
            </Typography>
            <ConfidenceLineChart history={history} theme={theme} />
          </Box>
        )}

        {/* Expand/Collapse button */}
        {showDetails && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
            <IconButton
              onClick={() => setExpanded(!expanded)}
              aria-expanded={expanded}
              aria-label={expanded ? 'Hide details' : 'Show details'}
            >
              {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            </IconButton>
          </Box>
        )}

        {/* Detailed breakdown */}
        <Collapse in={expanded && showDetails}>
          <Stack spacing={3}>
            {/* Confidence factors breakdown */}
            <Box>
              <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
                Confidence Factors
              </Typography>
              <Stack spacing={1.5}>
                <FactorBar
                  label="Information Completeness"
                  value={currentScore.factors.informationCompleteness}
                  weight={25}
                  description="Do we have all needed information?"
                />
                <FactorBar
                  label="Requirement Clarity"
                  value={currentScore.factors.requirementClarity}
                  weight={20}
                  description="Are requirements clear and unambiguous?"
                />
                <FactorBar
                  label="Technical Feasibility"
                  value={currentScore.factors.technicalFeasibility}
                  weight={20}
                  description="Can we build this with available technology?"
                />
                <FactorBar
                  label="Validation Coverage"
                  value={currentScore.factors.validationCoverage}
                  weight={15}
                  description="Have we validated all assumptions?"
                />
                <FactorBar
                  label="Risk Assessment"
                  value={currentScore.factors.riskAssessment}
                  weight={10}
                  description="What are the identified risks?"
                />
                <FactorBar
                  label="User Alignment"
                  value={currentScore.factors.userAlignment}
                  weight={10}
                  description="Does this match user goals?"
                />
              </Stack>
            </Box>

            <Divider />

            {/* Confidence boosters */}
            {currentScore.confidenceBoosters.length > 0 && (
              <Box>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    mb: 1,
                  }}
                >
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'success.main' }}>
                    What Increases Confidence
                  </Typography>
                  <IconButton
                    size="small"
                    onClick={() => setShowBoosters(!showBoosters)}
                    aria-expanded={showBoosters}
                    aria-label={showBoosters ? 'Hide boosters' : 'Show boosters'}
                  >
                    {showBoosters ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                  </IconButton>
                </Box>
                <Collapse in={showBoosters}>
                  <List dense>
                    {currentScore.confidenceBoosters.map((booster, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={booster} />
                      </ListItem>
                    ))}
                  </List>
                </Collapse>
              </Box>
            )}

            {/* Uncertainty factors */}
            {currentScore.uncertaintyFactors.length > 0 && (
              <Box>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    mb: 1,
                  }}
                >
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'warning.main' }}>
                    What Reduces Confidence
                  </Typography>
                  <IconButton
                    size="small"
                    onClick={() => setShowUncertainties(!showUncertainties)}
                    aria-expanded={showUncertainties}
                    aria-label={showUncertainties ? 'Hide uncertainties' : 'Show uncertainties'}
                  >
                    {showUncertainties ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                  </IconButton>
                </Box>
                <Collapse in={showUncertainties}>
                  <List dense>
                    {currentScore.uncertaintyFactors.map((factor, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <WarningIcon color="warning" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={factor} />
                      </ListItem>
                    ))}
                  </List>
                </Collapse>
              </Box>
            )}

            {/* Recommended actions */}
            {currentScore.recommendedActions.length > 0 && (
              <Box>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    mb: 1,
                  }}
                >
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'info.main' }}>
                    Recommended Actions
                  </Typography>
                  <IconButton
                    size="small"
                    onClick={() => setShowActions(!showActions)}
                    aria-expanded={showActions}
                    aria-label={showActions ? 'Hide actions' : 'Show actions'}
                  >
                    {showActions ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                  </IconButton>
                </Box>
                <Collapse in={showActions}>
                  <List dense>
                    {currentScore.recommendedActions.map((action, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <LightbulbIcon color="info" fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary={action} />
                      </ListItem>
                    ))}
                  </List>
                </Collapse>
              </Box>
            )}
          </Stack>
        </Collapse>

        {/* Timestamp */}
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ display: 'block', mt: 2, textAlign: 'right' }}
        >
          Last updated: {new Date(currentScore.timestamp).toLocaleTimeString()}
        </Typography>
      </CardContent>
    </Card>
  )
}

/**
 * Individual factor progress bar
 */
interface FactorBarProps {
  label: string
  value: number
  weight: number
  description: string
}

const FactorBar: React.FC<FactorBarProps> = ({ label, value, weight, description }) => {
  const theme = useTheme()
  const color = getConfidenceColor(value, theme)

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
        <Tooltip title={description}>
          <Typography variant="body2" sx={{ fontSize: '0.875rem' }}>
            {label}
            <Typography
              component="span"
              variant="caption"
              sx={{ ml: 1, color: 'text.secondary' }}
            >
              ({weight}% weight)
            </Typography>
          </Typography>
        </Tooltip>
        <Typography variant="body2" sx={{ fontWeight: 600, color }}>
          {formatConfidence(value)}
        </Typography>
      </Box>
      <LinearProgress
        variant="determinate"
        value={value * 100}
        sx={{
          height: 6,
          borderRadius: 3,
          backgroundColor: theme.palette.mode === 'dark' 
            ? 'rgba(255, 255, 255, 0.1)' 
            : 'rgba(0, 0, 0, 0.1)',
          '& .MuiLinearProgress-bar': {
            backgroundColor: color,
            borderRadius: 3,
          },
        }}
        aria-label={`${label}: ${formatConfidence(value)}`}
      />
    </Box>
  )
}

export default ConfidenceDashboard
