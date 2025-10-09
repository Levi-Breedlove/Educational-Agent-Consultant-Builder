import React, { useState, useMemo } from 'react'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Stack,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Alert,
  AlertTitle,
  Divider,
  useTheme,
  SelectChangeEvent,
} from '@mui/material'
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Remove as RemoveIcon,
  FilterList as FilterListIcon,
  Timeline as TimelineIcon,
  Insights as InsightsIcon,
} from '@mui/icons-material'
import ConfidenceHistory, { type ConfidenceHistoryPoint } from './ConfidenceHistory'
import type { ConfidenceScore } from './ConfidenceDashboard'

export interface ConfidenceTabProps {
  currentScore: ConfidenceScore
  history: ConfidenceHistoryPoint[]
}

/**
 * Confidence Tab Component
 * 
 * Displays detailed confidence history with filters, trends, and insights.
 * Allows filtering by phase, factor, and date range.
 * 
 * Requirements: 20.3, 20.11
 */
export const ConfidenceTab: React.FC<ConfidenceTabProps> = ({
  currentScore,
  history,
}) => {
  const [phaseFilter, setPhaseFilter] = useState<string>('all')
  const [dateRangeFilter, setDateRangeFilter] = useState<string>('all')

  // Extract unique phases from history
  const availablePhases = useMemo(() => {
    return Array.from(new Set(history.map(p => p.phase)))
  }, [history])

  // Filter history based on selected filters
  const filteredHistory = useMemo(() => {
    let filtered = [...history]

    // Phase filter
    if (phaseFilter !== 'all') {
      filtered = filtered.filter(p => p.phase === phaseFilter)
    }

    // Date range filter
    if (dateRangeFilter !== 'all') {
      const now = Date.now()
      const ranges: Record<string, number> = {
        '1h': 60 * 60 * 1000,
        '6h': 6 * 60 * 60 * 1000,
        '24h': 24 * 60 * 60 * 1000,
        '7d': 7 * 24 * 60 * 60 * 1000,
      }
      const cutoff = now - ranges[dateRangeFilter]
      filtered = filtered.filter(p => new Date(p.timestamp).getTime() >= cutoff)
    }

    return filtered
  }, [history, phaseFilter, dateRangeFilter])

  // Calculate insights
  const insights = useMemo(() => {
    if (filteredHistory.length === 0) {
      return {
        trend: 'stable' as const,
        avgConfidence: 0,
        minConfidence: 0,
        maxConfidence: 0,
        volatility: 0,
        improvementRate: 0,
      }
    }

    const confidences = filteredHistory.map(p => p.confidence)
    const avgConfidence = confidences.reduce((sum, c) => sum + c, 0) / confidences.length
    const minConfidence = Math.min(...confidences)
    const maxConfidence = Math.max(...confidences)

    // Calculate volatility (standard deviation)
    const variance = confidences.reduce((sum, c) => sum + Math.pow(c - avgConfidence, 2), 0) / confidences.length
    const volatility = Math.sqrt(variance)

    // Calculate trend
    let trend: 'up' | 'down' | 'stable' = 'stable'
    if (filteredHistory.length >= 2) {
      const recent = filteredHistory.slice(-3)
      const avgRecent = recent.reduce((sum, p) => sum + p.confidence, 0) / recent.length
      const previous = filteredHistory.slice(-6, -3)
      if (previous.length > 0) {
        const avgPrevious = previous.reduce((sum, p) => sum + p.confidence, 0) / previous.length
        if (avgRecent > avgPrevious + 0.02) trend = 'up'
        else if (avgRecent < avgPrevious - 0.02) trend = 'down'
      }
    }

    // Calculate improvement rate (change per hour)
    let improvementRate = 0
    if (filteredHistory.length >= 2) {
      const first = filteredHistory[0]
      const last = filteredHistory[filteredHistory.length - 1]
      const timeDiff = new Date(last.timestamp).getTime() - new Date(first.timestamp).getTime()
      const hoursDiff = timeDiff / (1000 * 60 * 60)
      if (hoursDiff > 0) {
        improvementRate = (last.confidence - first.confidence) / hoursDiff
      }
    }

    return {
      trend,
      avgConfidence,
      minConfidence,
      maxConfidence,
      volatility,
      improvementRate,
    }
  }, [filteredHistory])

  // Handle filter changes
  const handlePhaseFilterChange = (event: SelectChangeEvent) => {
    setPhaseFilter(event.target.value)
  }

  const handleDateRangeFilterChange = (event: SelectChangeEvent) => {
    setDateRangeFilter(event.target.value)
  }

  // Empty state
  if (history.length === 0) {
    return (
      <Box
        sx={{
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          p: 4,
        }}
      >
        <Alert severity="info" sx={{ maxWidth: 600 }}>
          <AlertTitle>No Confidence History Yet</AlertTitle>
          Confidence tracking will appear as you progress through the agent creation workflow.
          The system tracks confidence across all phases: requirements, architecture, implementation, testing, and deployment.
        </Alert>
      </Box>
    )
  }

  return (
    <Box
      sx={{
        height: '100%',
        overflow: 'auto',
        p: 3,
      }}
    >
      <Stack spacing={3}>
        {/* Header */}
        <Box>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600 }}>
            Confidence Analysis
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Detailed confidence history with trends, insights, and filtering options.
          </Typography>
        </Box>

        {/* Filters */}
        <Card elevation={1}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <FilterListIcon />
              <Typography variant="h6">Filters</Typography>
            </Box>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth size="small">
                  <InputLabel id="phase-filter-label">Phase</InputLabel>
                  <Select
                    labelId="phase-filter-label"
                    id="phase-filter"
                    value={phaseFilter}
                    label="Phase"
                    onChange={handlePhaseFilterChange}
                  >
                    <MenuItem value="all">All Phases</MenuItem>
                    {availablePhases.map(phase => (
                      <MenuItem key={phase} value={phase}>
                        {phase.charAt(0).toUpperCase() + phase.slice(1)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth size="small">
                  <InputLabel id="date-range-filter-label">Date Range</InputLabel>
                  <Select
                    labelId="date-range-filter-label"
                    id="date-range-filter"
                    value={dateRangeFilter}
                    label="Date Range"
                    onChange={handleDateRangeFilterChange}
                  >
                    <MenuItem value="all">All Time</MenuItem>
                    <MenuItem value="1h">Last Hour</MenuItem>
                    <MenuItem value="6h">Last 6 Hours</MenuItem>
                    <MenuItem value="24h">Last 24 Hours</MenuItem>
                    <MenuItem value="7d">Last 7 Days</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Insights Summary */}
        <Card elevation={1}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <InsightsIcon />
              <Typography variant="h6">Insights</Typography>
              <Chip
                icon={
                  insights.trend === 'up' ? <TrendingUpIcon /> :
                  insights.trend === 'down' ? <TrendingDownIcon /> :
                  <RemoveIcon />
                }
                label={
                  insights.trend === 'up' ? 'Improving' :
                  insights.trend === 'down' ? 'Declining' :
                  'Stable'
                }
                size="small"
                color={
                  insights.trend === 'up' ? 'success' :
                  insights.trend === 'down' ? 'warning' :
                  'default'
                }
              />
            </Box>

            <Grid container spacing={2}>
              <Grid item xs={6} sm={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Average
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    {(insights.avgConfidence * 100).toFixed(1)}%
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Range
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    {(insights.minConfidence * 100).toFixed(1)}% - {(insights.maxConfidence * 100).toFixed(1)}%
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Volatility
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    {(insights.volatility * 100).toFixed(1)}%
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Change Rate
                  </Typography>
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: 600,
                      color: insights.improvementRate > 0 ? 'success.main' :
                             insights.improvementRate < 0 ? 'error.main' :
                             'text.primary'
                    }}
                  >
                    {insights.improvementRate > 0 ? '+' : ''}
                    {(insights.improvementRate * 100).toFixed(2)}%/hr
                  </Typography>
                </Box>
              </Grid>
            </Grid>

            <Divider sx={{ my: 2 }} />

            {/* Insights text */}
            <Stack spacing={1}>
              {insights.trend === 'up' && (
                <Alert severity="success" variant="outlined">
                  Confidence is improving over time. The system is gathering more information and validating assumptions.
                </Alert>
              )}
              {insights.trend === 'down' && (
                <Alert severity="warning" variant="outlined">
                  Confidence is declining. This may indicate new uncertainties or complexities discovered during the workflow.
                </Alert>
              )}
              {insights.volatility > 0.05 && (
                <Alert severity="info" variant="outlined">
                  High volatility detected. Confidence is fluctuating significantly, which is normal during requirements gathering and architecture design phases.
                </Alert>
              )}
              {insights.avgConfidence >= 0.95 && (
                <Alert severity="success" variant="outlined">
                  Excellent confidence level maintained above the 95% baseline. The system has high certainty in its recommendations.
                </Alert>
              )}
              {insights.avgConfidence < 0.95 && insights.avgConfidence >= 0.85 && (
                <Alert severity="warning" variant="outlined">
                  Confidence is below the 95% baseline but above 85%. The system will ask clarifying questions to improve confidence.
                </Alert>
              )}
              {insights.avgConfidence < 0.85 && (
                <Alert severity="error" variant="outlined">
                  Confidence is significantly below baseline. The system requires more information to proceed confidently.
                </Alert>
              )}
            </Stack>
          </CardContent>
        </Card>

        {/* Confidence History Chart */}
        <ConfidenceHistory history={filteredHistory} height={300} />

        {/* Current Confidence Breakdown */}
        <Card elevation={1}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <TimelineIcon />
              <Typography variant="h6">Current Confidence Factors</Typography>
            </Box>

            <Stack spacing={2}>
              <FactorDetail
                label="Information Completeness"
                value={currentScore.factors.informationCompleteness}
                weight={25}
                description="Do we have all needed information?"
              />
              <FactorDetail
                label="Requirement Clarity"
                value={currentScore.factors.requirementClarity}
                weight={20}
                description="Are requirements clear and unambiguous?"
              />
              <FactorDetail
                label="Technical Feasibility"
                value={currentScore.factors.technicalFeasibility}
                weight={20}
                description="Can we build this with available technology?"
              />
              <FactorDetail
                label="Validation Coverage"
                value={currentScore.factors.validationCoverage}
                weight={15}
                description="Have we validated all assumptions?"
              />
              <FactorDetail
                label="Risk Assessment"
                value={currentScore.factors.riskAssessment}
                weight={10}
                description="What are the identified risks?"
              />
              <FactorDetail
                label="User Alignment"
                value={currentScore.factors.userAlignment}
                weight={10}
                description="Does this match user goals?"
              />
            </Stack>
          </CardContent>
        </Card>

        {/* Active filters indicator */}
        {(phaseFilter !== 'all' || dateRangeFilter !== 'all') && (
          <Alert severity="info" variant="outlined">
            <AlertTitle>Filters Active</AlertTitle>
            Showing {filteredHistory.length} of {history.length} data points.
            {phaseFilter !== 'all' && ` Phase: ${phaseFilter}.`}
            {dateRangeFilter !== 'all' && ` Date range: ${dateRangeFilter}.`}
          </Alert>
        )}
      </Stack>
    </Box>
  )
}

/**
 * Factor detail display component
 */
interface FactorDetailProps {
  label: string
  value: number
  weight: number
  description: string
}

const FactorDetail: React.FC<FactorDetailProps> = ({ label, value, weight, description }) => {
  const theme = useTheme()
  
  const getColor = (val: number): string => {
    if (val >= 0.95) return theme.palette.success.main
    if (val >= 0.85) return theme.palette.warning.main
    return theme.palette.error.main
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
        <Box>
          <Typography variant="body1" sx={{ fontWeight: 600 }}>
            {label}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {description} • {weight}% weight
          </Typography>
        </Box>
        <Typography
          variant="h6"
          sx={{
            fontWeight: 700,
            color: getColor(value),
          }}
        >
          {(value * 100).toFixed(1)}%
        </Typography>
      </Box>
      <Box
        sx={{
          width: '100%',
          height: 8,
          backgroundColor: theme.palette.mode === 'dark' 
            ? 'rgba(255, 255, 255, 0.1)' 
            : 'rgba(0, 0, 0, 0.1)',
          borderRadius: 4,
          overflow: 'hidden',
        }}
      >
        <Box
          sx={{
            width: `${value * 100}%`,
            height: '100%',
            backgroundColor: getColor(value),
            transition: 'width 0.3s ease',
          }}
        />
      </Box>
    </Box>
  )
}

export default ConfidenceTab
