import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Box, Grid, Paper, Fab, Badge, Tabs, Tab } from '@mui/material'
import { Timeline, Chat, Architecture, Code, CheckCircle } from '@mui/icons-material'
import { useDispatch, useSelector } from 'react-redux'
import { useMutation } from '@tanstack/react-query'
import { sessionsApi } from '../api/sessions'
import { setSession, setConnected } from '../store/slices/sessionSlice'
import { startWorkflow } from '../store/slices/workflowSlice'
import { setActiveTab } from '../store/slices/uiSlice'
import ChatInterface from '../components/ChatInterface'
import ProgressTracker from '../components/ProgressTracker'
import ConfidenceDashboard, { type ConfidenceScore } from '../components/ConfidenceDashboard'
import TabPanel, { a11yProps } from '../components/TabPanel'
import ArchitectureTab from '../components/ArchitectureTab'
import CodeTab from '../components/CodeTab'
import ConfidenceTab from '../components/ConfidenceTab'
import DevWorkflowControls from '../components/DevWorkflowControls'
import useResponsive from '../hooks/useResponsive'
import useConfidenceUpdates from '../hooks/useConfidenceUpdates'
import { ChatInterfaceSkeleton, ProgressTrackerSkeleton } from '../components/LoadingSkeletons'
import type { RootState } from '../store'

// ⚠️ TEMPORARY: Mock confidence data for visual testing
// TODO: REMOVE BEFORE PRODUCTION - Replace with real backend data
// This mock data is used for UI development and testing only
const MOCK_CONFIDENCE_SCORE: ConfidenceScore = {
  overallConfidence: 0.96,
  factors: {
    informationCompleteness: 0.95,
    requirementClarity: 0.98,
    technicalFeasibility: 0.97,
    validationCoverage: 0.94,
    riskAssessment: 0.96,
    userAlignment: 0.95,
  },
  confidenceBoosters: [
    'Clear and detailed requirements provided',
    'Architecture validated against AWS Well-Architected Framework',
    'All technical dependencies identified and available',
    'Cost estimates within acceptable range',
  ],
  uncertaintyFactors: [
    'Performance benchmarks not yet established',
    'Integration testing pending',
  ],
  recommendedActions: [
    'Define performance SLAs for production',
    'Schedule integration testing with existing systems',
    'Review security compliance checklist',
  ],
  meetsBaseline: true,
  timestamp: new Date().toISOString(),
}

// ⚠️ TEMPORARY: Mock history data for visual testing
// TODO: REMOVE BEFORE PRODUCTION - Replace with real backend data
const MOCK_HISTORY = [
  { timestamp: new Date(Date.now() - 300000).toISOString(), confidence: 0.88, phase: 'requirements' },
  { timestamp: new Date(Date.now() - 240000).toISOString(), confidence: 0.91, phase: 'requirements' },
  { timestamp: new Date(Date.now() - 180000).toISOString(), confidence: 0.93, phase: 'architecture' },
  { timestamp: new Date(Date.now() - 120000).toISOString(), confidence: 0.95, phase: 'architecture' },
  { timestamp: new Date(Date.now() - 60000).toISOString(), confidence: 0.96, phase: 'implementation' },
]

export default function AgentBuilderPage() {
  const { agentId } = useParams()
  const dispatch = useDispatch()
  const { isMobile } = useResponsive()
  const [showProgress, setShowProgress] = useState(!isMobile)
  const activeTab = useSelector((state: RootState) => state.ui.activeTab)
  const sessionAgentId = useSelector((state: RootState) => state.session.agentId)

  // Get real-time confidence updates
  const { currentScore, history } = useConfidenceUpdates(sessionAgentId || '')
  
  // ⚠️ TEMPORARY: Use mock data for visual testing
  // TODO: REMOVE BEFORE PRODUCTION - This should use real backend data
  // See DevWorkflowControls.tsx for related dev-only component
  const displayScore = currentScore || MOCK_CONFIDENCE_SCORE
  const displayHistory = history.length > 0 ? history : MOCK_HISTORY

  const createSessionMutation = useMutation({
    mutationFn: sessionsApi.create,
    onSuccess: (data) => {
      dispatch(setSession({ sessionId: data.session_id, agentId: data.agent_id }))
      dispatch(setConnected(true))
      dispatch(startWorkflow())
    },
  })

  useEffect(() => {
    if (!agentId) {
      createSessionMutation.mutate({})
    }
  }, [agentId])

  // Auto-hide progress tracker on mobile
  useEffect(() => {
    setShowProgress(!isMobile)
  }, [isMobile])

  // Handle tab change
  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    dispatch(setActiveTab(newValue))
  }

  // Keyboard navigation for tabs
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'ArrowLeft' && activeTab > 0) {
      dispatch(setActiveTab(activeTab - 1))
    } else if (event.key === 'ArrowRight' && activeTab < 3) {
      dispatch(setActiveTab(activeTab + 1))
    }
  }

  if (createSessionMutation.isPending) {
    return (
      <Box sx={{ height: '100%', width: '100%' }}>
        <Grid container spacing={2} sx={{ height: '100%' }}>
          <Grid item xs={12} md={8} sx={{ height: '100%' }}>
            <ChatInterfaceSkeleton />
          </Grid>
          <Grid item xs={12} md={4} sx={{ height: '100%' }}>
            <ProgressTrackerSkeleton />
          </Grid>
        </Grid>
      </Box>
    )
  }

  return (
    <Box 
      sx={{ 
        height: '100%', 
        width: '100%', 
        position: 'relative', 
        pt: { xs: 1, sm: 2, md: 3 }, 
        pb: { xs: 1, sm: 2 }, 
        px: { xs: 1, sm: 2 }, 
        boxSizing: 'border-box',
        overflowY: 'auto',
        overflowX: 'hidden',
      }}
    >
      <Grid 
        container 
        spacing={{ xs: 1, sm: 2 }} 
        sx={{ 
          height: { xs: 'auto', md: '100%' },
          minHeight: { xs: 'calc(100vh - 80px)', md: 'auto' },
        }}
      >
        {/* Main Content Area with Tabs - Full width on mobile, 8 cols on desktop */}
        <Grid
          item
          xs={12}
          md={8}
          sx={{
            display: isMobile && showProgress ? 'none' : 'flex',
            height: { xs: 'auto', md: '100%' },
            minHeight: { xs: '500px', md: 'auto' },
          }}
        >
          <Paper
            sx={{
              width: '100%',
              height: { xs: 'auto', md: '100%' },
              minHeight: { xs: '500px', md: 'auto' },
              display: 'flex',
              flexDirection: 'column',
              overflow: 'hidden',
            }}
          >
            {/* Tabs Navigation */}
            <Box
              sx={{
                borderBottom: 1,
                borderColor: 'divider',
                bgcolor: 'background.paper',
              }}
              onKeyDown={handleKeyDown}
            >
              <Tabs
                value={activeTab}
                onChange={handleTabChange}
                aria-label="agent builder tabs"
                variant={isMobile ? 'scrollable' : 'standard'}
                scrollButtons={isMobile ? 'auto' : false}
                sx={{
                  minHeight: 48,
                  '& .MuiTab-root': {
                    minHeight: 48,
                    textTransform: 'none',
                    fontSize: '0.875rem',
                    fontWeight: 500,
                  },
                }}
              >
                <Tab
                  icon={<Chat />}
                  iconPosition="start"
                  label="Chat"
                  {...a11yProps(0)}
                />
                <Tab
                  icon={<Architecture />}
                  iconPosition="start"
                  label="Architecture"
                  {...a11yProps(1)}
                />
                <Tab
                  icon={<Code />}
                  iconPosition="start"
                  label="Code"
                  {...a11yProps(2)}
                />
                <Tab
                  icon={<CheckCircle />}
                  iconPosition="start"
                  label="Confidence"
                  {...a11yProps(3)}
                />
              </Tabs>
            </Box>

            {/* Tab Panels */}
            <Box 
              sx={{ 
                flexGrow: 1, 
                overflow: { xs: 'auto', md: 'hidden' }, 
                display: 'flex', 
                flexDirection: 'column',
                minHeight: { xs: '400px', md: 'auto' },
              }}
            >
              <TabPanel value={activeTab} index={0}>
                <ChatInterface />
              </TabPanel>
              <TabPanel value={activeTab} index={1}>
                <ArchitectureTab />
              </TabPanel>
              <TabPanel value={activeTab} index={2}>
                <CodeTab agentId={sessionAgentId || undefined} />
              </TabPanel>
              <TabPanel value={activeTab} index={3}>
                <ConfidenceTab
                  currentScore={displayScore}
                  history={displayHistory}
                />
              </TabPanel>
            </Box>
          </Paper>
        </Grid>

        {/* Right Sidebar - Progress Tracker + Confidence Dashboard */}
        <Grid
          item
          xs={12}
          md={4}
          sx={{
            display: isMobile && !showProgress ? 'none' : 'flex',
            height: { xs: 'auto', md: '100%' },
            minHeight: { xs: '300px', md: 'auto' },
          }}
        >
          <Box
            sx={{
              width: '100%',
              height: { xs: 'auto', md: '100%' },
              display: 'flex',
              flexDirection: 'column',
              gap: { xs: 1, sm: 2 },
              overflow: 'auto',
              pb: { xs: 2, md: 0 },
            }}
          >
            {/* Progress Tracker */}
            <Paper
              sx={{
                p: { xs: 1, sm: 1.5, md: 2 },
                flexShrink: 0,
              }}
            >
              <ProgressTracker />
            </Paper>

            {/* Confidence Dashboard */}
            {displayScore && (
              <Box sx={{ flexShrink: 0, mb: { xs: 8, md: 0 } }}>
                <ConfidenceDashboard
                  currentScore={displayScore}
                  history={displayHistory}
                  showDetails={!isMobile}
                  compact={isMobile}
                />
              </Box>
            )}
          </Box>
        </Grid>
      </Grid>

      {/* Floating Action Button for mobile to toggle progress tracker */}
      {isMobile && (
        <Fab
          color="primary"
          aria-label="toggle progress"
          onClick={() => setShowProgress(!showProgress)}
          sx={{
            position: 'fixed',
            bottom: { xs: 16, sm: 20 },
            right: { xs: 16, sm: 20 },
            zIndex: 1000,
            width: { xs: 48, sm: 56 },
            height: { xs: 48, sm: 56 },
          }}
        >
          <Badge badgeContent={showProgress ? '×' : ''} color="secondary">
            <Timeline sx={{ fontSize: { xs: 20, sm: 24 } }} />
          </Badge>
        </Fab>
      )}

      {/* DEV ONLY: Workflow controls for testing */}
      {import.meta.env.DEV && <DevWorkflowControls />}
    </Box>
  )
}
