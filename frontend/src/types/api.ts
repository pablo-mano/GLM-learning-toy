export interface User {
  id: string
  email: string
  role: string
  created_at: string
}

export interface Child {
  id: string
  user_id: string
  name: string
  preferred_language: string
  birth_date?: string
  avatar_url?: string
  created_at: string
}

export interface WordTranslation {
  id: string
  language: string
  text: string
  phonetic?: string
  example_sentence?: string
}

export interface Word {
  id: string
  domain_id: string
  difficulty: string
  image_url?: string
  sort_order: number
  translations: WordTranslation[]
  prerequisite_ids: string[]
  created_at: string
}

export interface Domain {
  id: string
  user_id?: string
  name: string
  description?: string
  icon?: string
  color?: string
  is_system: boolean
  word_count: number
  created_at: string
}

export interface WordProgress {
  word_id: string
  word_text: Record<string, string>
  status: 'locked' | 'unlocked' | 'in_progress' | 'practicing' | 'mastered'
  difficulty: string
}

export interface ProgressOverview {
  total_words: number
  mastered: number
  practicing: number
  in_progress: number
  unlocked: number
  locked: number
  total_attempts: number
  total_correct: number
  accuracy: number
}

export interface GraphNode {
  id: string
  domain_id: string
  difficulty: string
  image_url?: string
  translations: Record<string, string>
  sort_order: number
}

export interface GraphEdge {
  from: string
  to: string
}

export interface LearningGraph {
  domain_id: string
  domain_name: string
  nodes: GraphNode[]
  edges: GraphEdge[]
  levels: string[][]
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  word_id?: string
  timestamp: string
}

export interface ChatResponse {
  session_id: string
  message: ChatMessage
}
