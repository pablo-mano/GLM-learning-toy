import { create } from 'zustand'
import type { Domain, LearningGraph } from '@/types/api'
import * as domainService from '@/services/domain.service'

interface DomainState {
  domains: Domain[]
  currentDomain: Domain | null
  currentGraph: LearningGraph | null
  isLoading: boolean
  error: string | null

  // Actions
  fetchDomains: () => Promise<void>
  fetchDomain: (id: string) => Promise<void>
  fetchDomainGraph: (id: string) => Promise<void>
  clearCurrentDomain: () => void
}

export const useDomainStore = create<DomainState>()((set, get) => ({
  domains: [],
  currentDomain: null,
  currentGraph: null,
  isLoading: false,
  error: null,

  fetchDomains: async () => {
    set({ isLoading: true, error: null })
    try {
      const domains = await domainService.getDomains()
      set({ domains, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch domains',
        isLoading: false
      })
    }
  },

  fetchDomain: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      const domain = await domainService.getDomain(id)
      set({ currentDomain: domain, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch domain',
        isLoading: false
      })
    }
  },

  fetchDomainGraph: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      const graph = await domainService.getDomainGraph(id)
      set({ currentGraph: graph, isLoading: false })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch graph',
        isLoading: false
      })
    }
  },

  clearCurrentDomain: () => {
    set({ currentDomain: null, currentGraph: null })
  }
}))
