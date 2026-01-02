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

// Standalone exported functions
export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>('/auth/login', credentials)
  return response.data
}

export async function register(data: RegisterData): Promise<User> {
  const response = await api.post<User>('/auth/register', data)
  return response.data
}

export async function getMe(): Promise<User> {
  const response = await api.get<User>('/auth/me')
  return response.data
}

export async function getChildren(): Promise<Child[]> {
  const response = await api.get<Child[]>('/auth/children')
  return response.data
}

export async function createChild(data: CreateChildData): Promise<Child> {
  const response = await api.post<Child>('/auth/children', data)
  return response.data
}

// Legacy object export for backwards compatibility
export const authService = {
  login,
  register,
  getMe,
  getChildren,
  createChild,
}
