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

export const domainService = {
  async getDomains(includeSystem = true): Promise<Domain[]> {
    const response = await api.get<Domain[]>('/domains', {
      params: { include_system: includeSystem }
    })
    return response.data
  },

  async getDomain(domainId: string): Promise<Domain> {
    const response = await api.get<Domain>(`/domains/${domainId}`)
    return response.data
  },

  async createDomain(data: CreateDomainData): Promise<Domain> {
    const response = await api.post<Domain>('/domains', data)
    return response.data
  },

  async getDomainWords(domainId: string): Promise<Word[]> {
    const response = await api.get<Word[]>(`/domains/${domainId}/words`)
    return response.data
  },

  async createWord(data: CreateWordData): Promise<Word> {
    const response = await api.post<Word>(`/domains/${data.domain_id}/words`, data)
    return response.data
  },

  async getDomainGraph(domainId: string): Promise<LearningGraph> {
    const response = await api.get<LearningGraph>(`/domains/${domainId}/graph`)
    return response.data
  },
}

// Named exports for direct imports
export const getDomains = domainService.getDomains
export const getDomain = domainService.getDomain
export const createDomain = domainService.createDomain
export const getDomainWords = domainService.getDomainWords
export const createWord = domainService.createWord
export const getDomainGraph = domainService.getDomainGraph
