import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { Box, Typography, LinearProgress, Chip, Stack, Paper, Divider, useTheme } from '@mui/material'
import { CheckCircle, RadioButtonUnchecked, Circle } from '@mui/icons-material'
import { RootState } from '../store'
import { updateElapsedTime, WorkflowPhase, PhaseStatus } from '../store/slices/workflowSlice'

interface PhaseInfo {
  label: string
  description: string
  estimatedMinutes: number
}

const PHASE_INFO: Record<WorkflowPhase, PhaseInfo> = {
  requirements: {
    label: 'Requirements',
    description: 'Understanding your needs',
    estimatedMinutes: 8,
  },
  architecture: {
    label: 'Architecture',
    description: 'Designing the solution',
    estimatedMinutes: 10,
  },
  implementation: {
    label: 'Implementation',
    description: 'Building your agent',
    estimatedMinutes: 15,
  },
  testing: {
    label: 'Testing',
    description: 'Validating functionality',
    estimatedMinutes: 7,
  },
  deployment: {
    label: 'Deployment',
    description: 'Preparing for production',
    estimatedMinutes: 5,
  },
}

const TOTAL_ESTIMATED_MINUTES = 45

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function getPhaseIcon(status: PhaseStatus, isDark: boolean) {
  switch (status) {
    case 'completed':
      return <CheckCircle sx={{ 
        color: isDark ? '#68d391' : 'success.main', 
        fontSize: { xs: 18, sm: 20 },
        filter: isDark ? 'drop-shadow(0 0 4px rgba(104, 211, 145, 0.6))' : 'none',
      }} />
    case 'in_progress':
      return <Circle sx={{ 
        color: 'primary.main', 
        fontSize: { xs: 18, sm: 20 },
        filter: isDark ? 'drop-shadow(0 0 4px rgba(104, 211, 145, 0.4))' : 'none',
      }} />
    case 'pending':
      return <RadioButtonUnchecked sx={{ color: 'grey.400', fontSize: { xs: 18, sm: 20 } }} />
  }
}

function getStatusColor(status: PhaseStatus): 'success' | 'primary' | 'default' {
  switch (status) {
    case 'completed':
      return 'success'
    case 'in_progress':
      return 'primary'
    case 'pending':
      return 'default'
  }
}

export default function ProgressTracker() {
  const dispatch = useDispatch()
  const theme = useTheme()
  const isDark = theme.palette.mode === 'dark'
  const { currentPhase, phases, startTime, elapsedTime } = useSelector(
    (state: RootState) => state.workflow
  )

  // Update elapsed time every second
  useEffect(() => {
    if (!startTime) return

    const interval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000)
      dispatch(updateElapsedTime(elapsed))
    }, 1000)

    return () => clearInterval(interval)
  }, [startTime, dispatch])

  const phaseOrder: WorkflowPhase[] = ['requirements', 'architecture', 'implementation', 'testing', 'deployment']
  const currentPhaseIndex = phaseOrder.indexOf(currentPhase)
  const completedPhases = phaseOrder.filter((phase) => phases[phase] === 'completed').length
  const overallProgress = (completedPhases / phaseOrder.length) * 100

  const estimatedRemainingMinutes = TOTAL_ESTIMATED_MINUTES - Math.floor(elapsedTime / 60)

  return (
    <Box 
      sx={{ 
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        overflow: 'hidden',
        width: '100%',
      }}
    >
      {/* Header with breathing room */}
      <Box sx={{ mb: 3, flexShrink: 0 }}>
        <Typography variant="h6" gutterBottom sx={{ fontSize: { xs: '1.1rem', sm: '1.25rem' }, mb: 0.5 }}>
          Agent Creation Progress
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ fontSize: { xs: '0.85rem', sm: '0.9rem' } }}>
          Building your production-ready agent
        </Typography>
      </Box>

      {/* Overall Progress */}
      <Paper 
        variant="outlined" 
        sx={{ 
          p: { xs: 1.5, sm: 2 }, 
          mb: 2, 
          flexShrink: 0,
          ...(isDark && {
            background: 'rgba(15, 23, 42, 0.6)',
            border: '1px solid rgba(104, 211, 145, 0.3)',
          }),
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="body2" fontWeight="medium" sx={{ fontSize: { xs: '0.85rem', sm: '0.9rem' } }}>
            Overall Progress
          </Typography>
          <Typography variant="body2" color="primary" fontWeight="bold" sx={{ fontSize: { xs: '0.85rem', sm: '0.9rem' } }}>
            {Math.round(overallProgress)}%
          </Typography>
        </Box>
        <LinearProgress
          variant="determinate"
          value={overallProgress}
          sx={{
            height: { xs: 6, sm: 8 },
            borderRadius: 4,
            backgroundColor: isDark ? 'rgba(148, 163, 184, 0.2)' : 'grey.200',
            '& .MuiLinearProgress-bar': {
              borderRadius: 4,
              background: isDark 
                ? 'linear-gradient(90deg, #68d391 0%, #48bb78 100%)'
                : 'linear-gradient(90deg, #1976d2 0%, #42a5f5 100%)',
              boxShadow: isDark ? '0 0 10px rgba(104, 211, 145, 0.6)' : 'none',
            },
          }}
        />
      </Paper>

      {/* Time Tracking */}
      <Paper 
        variant="outlined" 
        sx={{ 
          p: { xs: 1.5, sm: 2 }, 
          mb: 2, 
          flexShrink: 0,
          ...(isDark && {
            background: 'rgba(15, 23, 42, 0.6)',
            border: '1px solid rgba(104, 211, 145, 0.3)',
          }),
        }}
      >
        <Stack direction="row" spacing={{ xs: 2, sm: 3 }} justifyContent="space-between">
          <Box sx={{ minWidth: 0 }}>
            <Typography variant="caption" color="text.secondary" display="block" sx={{ fontSize: { xs: '0.75rem', sm: '0.8rem' } }}>
              Elapsed
            </Typography>
            <Typography variant="h6" color="primary" sx={{ fontSize: { xs: '1.1rem', sm: '1.25rem' } }}>
              {formatTime(elapsedTime)}
            </Typography>
          </Box>
          <Box sx={{ textAlign: 'right', minWidth: 0 }}>
            <Typography variant="caption" color="text.secondary" display="block" sx={{ fontSize: { xs: '0.75rem', sm: '0.8rem' } }}>
              Remaining
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ fontSize: { xs: '1.1rem', sm: '1.25rem' } }}>
              {estimatedRemainingMinutes > 0 ? `~${estimatedRemainingMinutes}m` : 'Done!'}
            </Typography>
          </Box>
        </Stack>
        <Divider sx={{ my: 1.5 }} />
        <Typography 
          variant="caption" 
          color="text.secondary" 
          align="center" 
          display="block"
          sx={{ fontSize: { xs: '0.75rem', sm: '0.8rem' } }}
        >
          Target: 30-45 min
        </Typography>
      </Paper>

      {/* Phase List - Larger panels, no left bar */}
      <Box sx={{ flexShrink: 0 }}>
        <Typography 
          variant="subtitle2" 
          gutterBottom 
          sx={{ mb: 1.5, fontSize: { xs: '0.9rem', sm: '0.95rem' } }}
        >
          Workflow Phases
        </Typography>
        <Stack spacing={{ xs: 1.25, sm: 1.5 }}>
          {phaseOrder.map((phase, index) => {
            const info = PHASE_INFO[phase]
            const status = phases[phase]
            const isActive = phase === currentPhase

            return (
              <Paper
                key={phase}
                variant="outlined"
                sx={{
                  p: { xs: 1.25, sm: 1.5 },
                  position: 'relative',
                  transition: 'all 0.3s ease-in-out',
                  border: 1,
                  borderColor: isActive ? (isDark ? 'rgba(104, 211, 145, 0.5)' : 'primary.main') : 'divider',
                  ...(isDark && {
                    background: isActive ? 'rgba(15, 23, 42, 0.75)' : 'rgba(15, 23, 42, 0.5)',
                    border: `1px solid ${isActive ? 'rgba(104, 211, 145, 0.5)' : 'rgba(104, 211, 145, 0.3)'}`,
                  }),
                  ...(!isDark && {
                    backgroundColor: isActive ? 'primary.50' : 'background.paper',
                  }),
                  boxShadow: isActive ? (isDark ? '0 4px 12px rgba(104, 211, 145, 0.2)' : 2) : 0,
                  overflow: 'hidden',
                }}
              >
                <Stack direction="row" spacing={{ xs: 1, sm: 1.5 }} alignItems="center">
                  {/* Icon */}
                  <Box sx={{ flexShrink: 0 }}>{getPhaseIcon(status, isDark)}</Box>

                  {/* Content */}
                  <Box sx={{ flex: 1, minWidth: 0, overflow: 'hidden' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.75, mb: 0.5, flexWrap: 'nowrap' }}>
                      <Typography 
                        variant="subtitle2" 
                        fontWeight="bold"
                        sx={{ 
                          fontSize: { xs: '0.85rem', sm: '0.9rem' },
                          lineHeight: 1.3,
                          whiteSpace: 'nowrap',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                        }}
                      >
                        {index + 1}. {info.label}
                      </Typography>
                      <Chip
                        label={status.replace('_', ' ')}
                        size="small"
                        color={getStatusColor(status)}
                        sx={{ 
                          height: { xs: 20, sm: 22 }, 
                          fontSize: { xs: '0.65rem', sm: '0.7rem' }, 
                          textTransform: 'capitalize',
                          '& .MuiChip-label': { px: 1 },
                          flexShrink: 0,
                        }}
                      />
                    </Box>
                    <Typography 
                      variant="body2" 
                      color="text.secondary" 
                      sx={{ 
                        fontSize: { xs: '0.75rem', sm: '0.8rem' },
                        lineHeight: 1.4,
                        whiteSpace: 'nowrap',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                      }}
                    >
                      {info.description} • {info.estimatedMinutes}m
                    </Typography>
                  </Box>
                </Stack>
              </Paper>
            )
          })}
        </Stack>
      </Box>

      {/* Footer */}
      <Box sx={{ mt: 2, pt: 1.5, borderTop: 1, borderColor: 'divider', flexShrink: 0 }}>
        <Typography 
          variant="caption" 
          color="text.secondary" 
          align="center" 
          display="block"
          sx={{ fontSize: { xs: '0.75rem', sm: '0.8rem' } }}
        >
          {completedPhases === phaseOrder.length
            ? '🎉 Complete!'
            : `Phase ${currentPhaseIndex + 1} of ${phaseOrder.length}`}
        </Typography>
      </Box>
    </Box>
  )
}
