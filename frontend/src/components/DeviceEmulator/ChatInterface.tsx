import { useState, useRef, useEffect } from 'react'
import { useDeviceStore } from '@/stores/deviceStore'
import { chatService } from '@/services/chat.service'

interface ChatInterfaceProps {
  childId: string
}

export default function ChatInterface({ childId }: ChatInterfaceProps) {
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const chatMessages = useDeviceStore((state) => state.chatMessages)
  const addChatMessage = useDeviceStore((state) => state.addChatMessage)
  const sessionId = useDeviceStore((state) => state.sessionId)
  const setSessionId = useDeviceStore((state) => state.setSessionId)

  useEffect(() => {
    // Auto-scroll to bottom
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  const sendMessage = async () => {
    if (!message.trim() || isLoading) return

    const userMessage = message.trim()
    setMessage('')
    addChatMessage('user', userMessage)
    setIsLoading(true)

    try {
      const response = await chatService.sendMessage({
        session_id: sessionId || undefined,
        child_id: childId,
        message: userMessage
      })

      setSessionId(response.session_id)
      addChatMessage('assistant', response.message.content)
    } catch (error) {
      addChatMessage('system', 'Sorry, something went wrong. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const quickResponses = [
    "Help me practice!",
    "I'm stuck",
    "Let's learn!",
  ]

  return (
    <div className="h-full flex flex-col bg-gradient-to-b from-blue-50 to-purple-50">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {chatMessages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center p-4">
            <div className="text-6xl mb-4">🤖</div>
            <p className="text-gray-600 font-medium">Hi! I'm your learning buddy!</p>
            <p className="text-gray-500 text-sm">Ask me to help you practice words!</p>
          </div>
        )}

        {chatMessages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] px-4 py-2 rounded-2xl ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white rounded-br-sm'
                  : msg.role === 'system'
                  ? 'bg-red-100 text-red-600 text-sm'
                  : 'bg-white text-gray-800 shadow-sm rounded-bl-sm'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white px-4 py-2 rounded-2xl rounded-bl-sm shadow-sm">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Responses */}
      {chatMessages.length < 3 && (
        <div className="px-4 py-2 flex gap-2 overflow-x-auto">
          {quickResponses.map(response => (
            <button
              key={response}
              onClick={() => { setMessage(response); sendMessage(); }}
              className="whitespace-nowrap px-3 py-1 bg-white/80 hover:bg-white rounded-full text-sm text-gray-700 shadow-sm transition-colors"
            >
              {response}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="p-3 bg-white border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type a message..."
            className="flex-1 px-4 py-2 bg-gray-100 rounded-full outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!message.trim() || isLoading}
            className="w-10 h-10 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white rounded-full flex items-center justify-center transition-colors"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}
