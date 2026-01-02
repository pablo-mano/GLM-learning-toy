import api from './api'
import type { ChatResponse } from '@/types/api'

export interface SendMessageParams {
  session_id?: string
  child_id: string
  message: string
  domain_id?: string
}

export const chatService = {
  async sendMessage(params: SendMessageParams): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>('/chat/message', params)
    return response.data
  },

  async getHistory(sessionId: string): Promise<{
    session_id: string
    child_id: string
    messages: Array<{
      id: string
      role: string
      content: string
      word_id?: string
      timestamp: string
    }>
  }> {
    const response = await api.get(`/chat/sessions/${sessionId}/history`)
    return response.data
  },
}
