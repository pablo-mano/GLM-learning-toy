import { create } from 'zustand'
import type { WordProgress, Word } from '@/types/api'

interface DeviceState {
  currentWord: Word | null
  currentWordProgress: WordProgress | null
  showTranslation: boolean
  isPracticeMode: boolean
  sessionId: string | null
  chatMessages: Array<{ role: string; content: string }>

  // Actions
  setCurrentWord: (word: Word | null) => void
  setCurrentWordProgress: (progress: WordProgress | null) => void
  toggleTranslation: () => void
  setPracticeMode: (isPractice: boolean) => void
  addChatMessage: (role: string, content: string) => void
  clearChatMessages: () => void
  setSessionId: (id: string | null) => void
}

export const useDeviceStore = create<DeviceState>()((set) => ({
  currentWord: null,
  currentWordProgress: null,
  showTranslation: false,
  isPracticeMode: false,
  sessionId: null,
  chatMessages: [],

  setCurrentWord: (word) => set({ currentWord: word, showTranslation: false }),
  setCurrentWordProgress: (progress) => set({ currentWordProgress: progress }),
  toggleTranslation: () => set((state) => ({ showTranslation: !state.showTranslation })),
  setPracticeMode: (isPractice) => set({ isPracticeMode: isPractice }),
  addChatMessage: (role, content) => set((state) => ({
    chatMessages: [...state.chatMessages, { role, content }]
  })),
  clearChatMessages: () => set({ chatMessages: [] }),
  setSessionId: (id) => set({ sessionId: id })
}))
