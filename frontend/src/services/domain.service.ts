import api from './api'
import type { Domain, Word, LearningGraph } from '@/types/api'

export interface CreateDomainData {
  name: string
  description?: string
  icon?: string
  color?: string
}

export interface CreateWordData {
  domain_id: string
  difficulty: string
  image_url?: string
  sort_order?: number
  translations: Array<{
    language: string
    text: string
    phonetic?: string
    example_sentence?: string
  }>
  prerequisite_ids: string[]
}

// Standalone exported functions
export async function getDomains(includeSystem = true): Promise<Domain[]> {
  const response = await api.get<Domain[]>('/domains', {
    params: { include_system: includeSystem }
  })
  return response.data
}

export async function getDomain(domainId: string): Promise<Domain> {
  const response = await api.get<Domain>(`/domains/${domainId}`)
  return response.data
}

export async function createDomain(data: CreateDomainData): Promise<Domain> {
  const response = await api.post<Domain>('/domains', data)
  return response.data
}

export async function getDomainWords(domainId: string): Promise<Word[]> {
  const response = await api.get<Word[]>(`/domains/${domainId}/words`)
  return response.data
}

export async function createWord(data: CreateWordData): Promise<Word> {
  const response = await api.post<Word>(`/domains/${data.domain_id}/words`, data)
  return response.data
}

export async function getDomainGraph(domainId: string): Promise<LearningGraph> {
  const response = await api.get<LearningGraph>(`/domains/${domainId}/graph`)
  return response.data
}

// Legacy object export for backwards compatibility
export const domainService = {
  getDomains,
  getDomain,
  createDomain,
  getDomainWords,
  createWord,
  getDomainGraph,
}
