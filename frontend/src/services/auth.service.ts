import api from './api'
import type { User, Child } from '@/types/api'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
}

export interface CreateChildData {
  name: string
  preferred_language?: string
  birth_date?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/login', credentials)
    return response.data
  },

  async register(data: RegisterData): Promise<User> {
    const response = await api.post<User>('/auth/register', data)
    return response.data
  },

  async getMe(): Promise<User> {
    const response = await api.get<User>('/auth/me')
    return response.data
  },

  async getChildren(): Promise<Child[]> {
    const response = await api.get<Child[]>('/auth/children')
    return response.data
  },

  async createChild(data: CreateChildData): Promise<Child> {
    const response = await api.post<Child>('/auth/children', data)
    return response.data
  },
}
