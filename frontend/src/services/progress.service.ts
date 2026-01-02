import api from './api'
import type { ProgressOverview, WordProgress } from '@/types/api'

export interface NextWordsParams {
  childId: string
  domainId: string
  limit?: number
}

export interface RecordAttemptParams {
  childId: string
  wordId: string
  correct: boolean
}

export interface AttemptResult {
  id: string
  word_id: string
  status: string
  attempts: number
  correct_count: number
  streak_count: number
  accuracy: number
  last_practiced_at?: string
  mastered_at?: string
}

export const progressService = {
  async getOverview(childId: string): Promise<ProgressOverview> {
    const response = await api.get<ProgressOverview>(`/progress/child/${childId}/overview`)
    return response.data
  },

  async getNextWords(params: NextWordsParams): Promise<{ words: WordProgress[] }> {
    const response = await api.get<{ words: WordProgress[] }>(
      `/progress/child/${params.childId}/next-words`,
      { params: { domain_id: params.domainId, limit: params.limit || 5 } }
    )
    return response.data
  },

  async recordAttempt(params: RecordAttemptParams): Promise<AttemptResult> {
    const response = await api.post<AttemptResult>(
      `/progress/child/${params.childId}/word/${params.wordId}/attempt`,
      { correct: params.correct }
    )
    return response.data
  },
}
