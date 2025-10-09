import { apiClient } from './client'

export interface Session {
  session_id: string
  agent_id: string
  created_at: string
  state: Record<string, unknown>
}

export interface CreateSessionRequest {
  user_id?: string
  metadata?: Record<string, unknown>
}

export const sessionsApi = {
  create: async (data: CreateSessionRequest): Promise<Session> => {
    const response = await apiClient.post('/api/sessions', data)
    return response.data
  },

  get: async (sessionId: string): Promise<Session> => {
    const response = await apiClient.get(`/api/sessions/${sessionId}`)
    return response.data
  },

  delete: async (sessionId: string): Promise<void> => {
    await apiClient.delete(`/api/sessions/${sessionId}`)
  },
}
