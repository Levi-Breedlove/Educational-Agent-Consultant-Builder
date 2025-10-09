import { createSlice, PayloadAction } from '@reduxjs/toolkit'

export type WorkflowPhase = 'requirements' | 'architecture' | 'implementation' | 'testing' | 'deployment'
export type PhaseStatus = 'pending' | 'in_progress' | 'completed'

interface WorkflowState {
  currentPhase: WorkflowPhase
  phases: Record<WorkflowPhase, PhaseStatus>
  progress: number
  startTime: number | null
  elapsedTime: number
}

const initialState: WorkflowState = {
  currentPhase: 'requirements',
  phases: {
    requirements: 'in_progress',
    architecture: 'pending',
    implementation: 'pending',
    testing: 'pending',
    deployment: 'pending',
  },
  progress: 0,
  startTime: null,
  elapsedTime: 0,
}

const workflowSlice = createSlice({
  name: 'workflow',
  initialState,
  reducers: {
    setPhase: (state, action: PayloadAction<WorkflowPhase>) => {
      state.currentPhase = action.payload
      state.phases[action.payload] = 'in_progress'
    },
    completePhase: (state, action: PayloadAction<WorkflowPhase>) => {
      state.phases[action.payload] = 'completed'
    },
    setProgress: (state, action: PayloadAction<number>) => {
      state.progress = action.payload
    },
    startWorkflow: (state) => {
      state.startTime = Date.now()
    },
    updateElapsedTime: (state, action: PayloadAction<number>) => {
      state.elapsedTime = action.payload
    },
    resetWorkflow: () => initialState,
  },
})

export const { setPhase, completePhase, setProgress, startWorkflow, updateElapsedTime, resetWorkflow } = workflowSlice.actions
export default workflowSlice.reducer
