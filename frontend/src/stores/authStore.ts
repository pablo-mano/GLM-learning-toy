import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, Child } from '@/types/api'
import { authService } from '@/services/auth.service'

interface AuthState {
  user: User | null
  token: string | null
  children: Child[]
  selectedChildId: string | null
  isLoading: boolean
  error: string | null

  // Actions
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => void
  fetchChildren: () => Promise<void>
  setSelectedChildId: (childId: string) => void
  getSelectedChild: () => Child | null
  clearError: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      children: [],
      selectedChildId: null,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null })
        try {
          const response = await authService.login({ email, password })
          localStorage.setItem('token', response.access_token)
          set({ token: response.access_token })

          // Fetch user info
          const user = await authService.getMe()
          set({ user, isLoading: false })

          // Fetch children
          const children = await authService.getChildren()
          set({ children, selectedChildId: children[0]?.id || null })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Login failed',
            isLoading: false
          })
          throw error
        }
      },

      register: async (email: string, password: string) => {
        set({ isLoading: true, error: null })
        try {
          const user = await authService.register({ email, password })
          set({ user, isLoading: false })
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Registration failed',
            isLoading: false
          })
          throw error
        }
      },

      logout: () => {
        localStorage.removeItem('token')
        set({
          user: null,
          token: null,
          children: [],
          selectedChildId: null
        })
      },

      fetchChildren: async () => {
        try {
          const children = await authService.getChildren()
          const { selectedChildId } = get()
          set({
            children,
            selectedChildId: selectedChildId || children[0]?.id || null
          })
        } catch (error) {
          console.error('Failed to fetch children:', error)
        }
      },

      setSelectedChildId: (childId: string) => {
        set({ selectedChildId: childId })
      },

      getSelectedChild: () => {
        const { children, selectedChildId } = get()
        return children.find(c => c.id === selectedChildId) || null
      },

      clearError: () => set({ error: null })
    }),
    {
      name: 'learningtoy-auth',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        selectedChildId: state.selectedChildId
      })
    }
  )
)
