import { Box, Button, ButtonGroup, Paper, Typography, Chip, IconButton, Collapse, Alert } from '@mui/material'
import { ExpandMore, ExpandLess, Warning } from '@mui/icons-material'
import { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setPhase, completePhase } from '../store/slices/workflowSlice'
import type { RootState } from '../store'
import type { WorkflowPhase } from '../store/slices/workflowSlice'

/**
 * DEV ONLY: Helper component to manually control workflow phases for testing
 * 
 * ⚠️ IMPORTANT FOR DEVELOPERS:
 * - This component uses TEST/MOCK data for the confidence dashboard
 * - The mock data must be removed before production deployment
 * - This component controls code visualization functionality
 * - Remove this component entirely before production deployment
 * 
 * See: AgentBuilderPage.tsx (MOCK_CONFIDENCE_SCORE and MOCK_HISTORY)
 */
export default function DevWorkflowControls() {
  const dispatch = useDispatch()
  const currentPhase = useSelector((state: RootState) => state.workflow.currentPhase)
  const phases = useSelector((state: RootState) => state.workflow.phases)
  const [isExpanded, setIsExpanded] = useState(false)
  const [position, setPosition] = useState({ x: window.innerWidth - 416, y: 80 })
  const [isDragging, setIsDragging] = useState(false)
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 })

  const handleMouseDown = (e: React.MouseEvent) => {
    // Only start drag if clicking on the header area
    if ((e.target as HTMLElement).closest('.drag-handle')) {
      setIsDragging(true)
      setDragOffset({
        x: e.clientX - position.x,
        y: e.clientY - position.y,
      })
    }
  }

  const handleMouseMove = (e: MouseEvent) => {
    if (isDragging) {
      setPosition({
        x: e.clientX - dragOffset.x,
        y: e.clientY - dragOffset.y,
      })
    }
  }

  const handleMouseUp = () => {
    setIsDragging(false)
  }

  // Add/remove event listeners for dragging
  useEffect(() => {
    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove)
      window.addEventListener('mouseup', handleMouseUp)
      return () => {
        window.removeEventListener('mousemove', handleMouseMove)
        window.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [isDragging, dragOffset])

  const handleSetPhase = (phase: WorkflowPhase) => {
    dispatch(setPhase(phase))
  }

  const handleCompletePhase = (phase: WorkflowPhase) => {
    dispatch(completePhase(phase))
  }

  const handleCompleteImplementation = () => {
    // Complete all phases up to and including implementation
    dispatch(completePhase('requirements'))
    dispatch(completePhase('architecture'))
    dispatch(completePhase('implementation'))
    dispatch(setPhase('testing'))
  }

  const handleReset = () => {
    // Reset to initial state
    window.location.reload()
  }

  return (
    <Paper
      onMouseDown={handleMouseDown}
      sx={{
        position: 'fixed',
        top: position.y,
        left: position.x,
        p: 2,
        zIndex: 9999,
        maxWidth: 400,
        bgcolor: 'rgba(99, 102, 241, 0.15)',
        backdropFilter: 'blur(10px)',
        border: 1,
        borderColor: 'rgba(99, 102, 241, 0.3)',
        boxShadow: '0 4px 12px rgba(99, 102, 241, 0.2)',
        cursor: isDragging ? 'grabbing' : 'default',
        userSelect: 'none',
      }}
    >
      <Box 
        className="drag-handle"
        sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between', 
          mb: 1,
          cursor: 'grab',
          '&:active': {
            cursor: 'grabbing',
          },
        }}
      >
        <Typography variant="subtitle2" sx={{ fontWeight: 'bold', color: 'primary.main', pointerEvents: 'none' }}>
          🛠️ DEV WORKFLOW CONTROLS (Draggable)
        </Typography>
        <IconButton
          size="small"
          onClick={() => setIsExpanded(!isExpanded)}
          aria-label={isExpanded ? 'Collapse' : 'Expand'}
        >
          {isExpanded ? <ExpandLess /> : <ExpandMore />}
        </IconButton>
      </Box>

      <Alert severity="warning" icon={<Warning />} sx={{ mb: 2, fontSize: '0.75rem' }}>
        <Typography variant="caption" display="block" sx={{ fontWeight: 600 }}>
          ⚠️ REMOVE BEFORE PRODUCTION
        </Typography>
        <Typography variant="caption" display="block">
          • Using TEST data for confidence dashboard
        </Typography>
        <Typography variant="caption" display="block">
          • Controls code visualization sync
        </Typography>
      </Alert>

      <Typography variant="caption" display="block" gutterBottom>
        Current Phase: <Chip label={currentPhase} size="small" color="primary" />
      </Typography>

      <Collapse in={isExpanded}>

      <Box sx={{ mt: 2 }}>
        <Typography variant="caption" display="block" gutterBottom>
          Quick Actions:
        </Typography>
        <ButtonGroup size="small" orientation="vertical" fullWidth>
          <Button
            variant="contained"
            color="success"
            onClick={handleCompleteImplementation}
          >
            ✅ Complete Implementation (Show Code)
          </Button>
          <Button variant="outlined" onClick={handleReset}>
            🔄 Reset to Initial State
          </Button>
        </ButtonGroup>
      </Box>

      <Box sx={{ mt: 2 }}>
        <Typography variant="caption" display="block" gutterBottom>
          Phase Status:
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
          {Object.entries(phases).map(([phase, status]) => (
            <Box key={phase} sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
              <Chip
                label={phase}
                size="small"
                color={status === 'completed' ? 'success' : status === 'in_progress' ? 'primary' : 'default'}
                sx={{ minWidth: 120 }}
              />
              <ButtonGroup size="small">
                <Button
                  onClick={() => handleSetPhase(phase as WorkflowPhase)}
                  disabled={status === 'in_progress'}
                >
                  Start
                </Button>
                <Button
                  onClick={() => handleCompletePhase(phase as WorkflowPhase)}
                  disabled={status === 'completed'}
                >
                  Complete
                </Button>
              </ButtonGroup>
            </Box>
          ))}
        </Box>
      </Box>
      </Collapse>
    </Paper>
  )
}
