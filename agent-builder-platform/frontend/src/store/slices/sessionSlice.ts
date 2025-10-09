import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface SessionState {
  sessionId: string | null
  agentId: string | null
  isConnected: boolean
}

const initialState: SessionState = {
  sessionId: null,
  agentId: null,
  isConnected: false,
}

const sessionSlice = createSlice({
  name: 'session',
  initialState,
  reducers: {
    setSession: (state, action: PayloadAction<{ sessionId: string; agentId: string }>) => {
      state.sessionId = action.payload.sessionId
      state.agentId = action.payload.agentId
    },
    setConnected: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload
    },
    clearSession: (state) => {
      state.sessionId = null
      state.agentId = null
      state.isConnected = false
    },
  },
})

export const { setSession, setConnected, clearSession } = sessionSlice.actions
export default sessionSlice.reducer
