import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { useDeviceStore } from '@/stores/deviceStore'
import DeviceFrame from '@/components/DeviceEmulator/DeviceFrame'
import WordCard from '@/components/DeviceEmulator/WordCard'
import ChatInterface from '@/components/DeviceEmulator/ChatInterface'

export default function DevicePage() {
  const navigate = useNavigate()
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const selectedChild = useAuthStore((state) => state.getSelectedChild())
  const children = useAuthStore((state) => state.children)
  const setSelectedChildId = useAuthStore((state) => state.setSelectedChildId)

  const [mode, setMode] = useState<'learn' | 'chat'>('learn')

  const currentWord = useDeviceStore((state) => state.currentWord)
  const isPracticeMode = useDeviceStore((state) => state.isPracticeMode)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (!user) {
    navigate('/login')
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-100 to-orange-100 flex items-center justify-center p-4">
      {/* Header */}
      <div className="absolute top-4 left-4 right-4 flex items-center justify-between">
        <button
          onClick={() => navigate('/dashboard')}
          className="bg-white/80 hover:bg-white px-4 py-2 rounded-lg font-medium shadow-sm transition-colors"
        >
          ← Dashboard
        </button>
        {children.length > 1 && (
          <select
            value={selectedChild?.id || ''}
            onChange={(e) => setSelectedChildId(e.target.value)}
            className="bg-white/80 px-4 py-2 rounded-lg shadow-sm"
          >
            {children.map(child => (
              <option key={child.id} value={child.id}>{child.name}</option>
            ))}
          </select>
        )}
      </div>

      {/* Device Emulator */}
      <DeviceFrame>
        {/* Mode Selector */}
        <div className="flex gap-2 p-4 bg-gray-100 rounded-t-3xl">
          <button
            onClick={() => setMode('learn')}
            className={`flex-1 py-2 rounded-xl font-semibold transition-colors ${
              mode === 'learn'
                ? 'bg-blue-500 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
          >
            Learn
          </button>
          <button
            onClick={() => setMode('chat')}
            className={`flex-1 py-2 rounded-xl font-semibold transition-colors ${
              mode === 'chat'
                ? 'bg-green-500 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
          >
            Chat
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-hidden">
          {mode === 'learn' ? (
            currentWord ? (
              <WordCard childId={selectedChild?.id || ''} />
            ) : (
              <div className="h-full flex items-center justify-center p-8">
                <div className="text-center">
                  <p className="text-gray-600 mb-4">Welcome to LearningToy!</p>
                  <p className="text-sm text-gray-500">Select a domain to start learning words</p>
                </div>
              </div>
            )
          ) : (
            <ChatInterface childId={selectedChild?.id || ''} />
          )}
        </div>
      </DeviceFrame>

      {/* Domain Selector for Learn Mode */}
      {mode === 'learn' && (
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-2">
          <button
            onClick={() => {/* TODO: Select Animals domain */}}
            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-full font-medium shadow-lg transition-colors"
          >
            🦁 Animals
          </button>
          <button
            onClick={() => {/* TODO: Select Food domain */}}
            className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-full font-medium shadow-lg transition-colors"
          >
            🍎 Food & Home
          </button>
        </div>
      )}
    </div>
  )
}
