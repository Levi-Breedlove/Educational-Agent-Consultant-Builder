import { apiClient } from './client'

export interface AgentCreateRequest {
  description: string
  requirements?: string[]
}

export interface AgentStatus {
  agent_id: string
  phase: string
  status: string
  progress: number
  current_step: string
}

export interface AgentRecommendation {
  type: string
  content: string
  confidence: number
  alternatives?: string[]
}

export const agentsApi = {
  create: async (data: AgentCreateRequest): Promise<{ agent_id: string }> => {
    const response = await apiClient.post('/api/agents/create', data)
    return response.data
  },

  submitRequirements: async (agentId: string, requirements: string[]): Promise<void> => {
    await apiClient.post(`/api/agents/${agentId}/requirements`, { requirements })
  },

  submitFeedback: async (agentId: string, feedback: string): Promise<void> => {
    await apiClient.post(`/api/agents/${agentId}/feedback`, { feedback })
  },

  getStatus: async (agentId: string): Promise<AgentStatus> => {
    const response = await apiClient.get(`/api/agents/${agentId}/status`)
    return response.data
  },

  getRecommendations: async (agentId: string): Promise<AgentRecommendation[]> => {
    const response = await apiClient.get(`/api/agents/${agentId}/recommendations`)
    return response.data
  },
}
