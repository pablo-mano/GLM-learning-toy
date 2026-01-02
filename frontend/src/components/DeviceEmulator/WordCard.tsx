import { useEffect, useState } from 'react'
import { useDeviceStore } from '@/stores/deviceStore'
import { progressService } from '@/services/progress.service'
import { domainService } from '@/services/domain.service'
import type { Word, WordProgress } from '@/types/api'

interface WordCardProps {
  childId: string
  domainId?: string
}

export default function WordCard({ childId, domainId = '' }: WordCardProps) {
  const [words, setWords] = useState<Word[]>([])
  const [wordProgress, setWordProgress] = useState<WordProgress | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const setCurrentWord = useDeviceStore((state) => state.setCurrentWord)
  const setCurrentWordProgress = useDeviceStore((state) => state.setCurrentWordProgress)
  const showTranslation = useDeviceStore((state) => state.showTranslation)
  const toggleTranslation = useDeviceStore((state) => state.toggleTranslation)

  useEffect(() => {
    if (domainId) {
      loadWords()
    }
  }, [domainId])

  const loadWords = async () => {
    try {
      const allWords = await domainService.getDomainWords(domainId)
      setWords(allWords)

      // Get next recommended word
      const nextWords = await progressService.getNextWords({
        childId,
        domainId,
        limit: 1
      })

      if (nextWords.words.length > 0) {
        const progress = nextWords.words[0]
        const word = allWords.find(w => w.id === progress.word_id)
        if (word) {
          setCurrentWord(word)
          setWordProgress(progress)
        }
      }
    } catch (error) {
      console.error('Failed to load words:', error)
    }
  }

  const handlePractice = async (correct: boolean) => {
    if (!wordProgress || !childId) return

    setIsLoading(true)
    try {
      await progressService.recordAttempt({
        childId,
        wordId: wordProgress.word_id,
        correct
      })

      // Load next word
      await loadWords()
    } catch (error) {
      console.error('Failed to record attempt:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const currentWord = useDeviceStore((state) => state.currentWord)

  if (!currentWord) {
    return (
      <div className="h-full flex items-center justify-center p-8">
        <p className="text-gray-600 text-center">Select a domain above to start learning!</p>
      </div>
    )
  }

  // Get English and target language translations
  const enTranslation = currentWord.translations.find(t => t.language === 'en')
  const plTranslation = currentWord.translations.find(t => t.language === 'pl')
  const esTranslation = currentWord.translations.find(t => t.language === 'es')
  const targetTrans = plTranslation || esTranslation

  const statusColors = {
    locked: 'bg-gray-100 text-gray-400',
    unlocked: 'bg-blue-100 text-blue-600',
    in_progress: 'bg-yellow-100 text-yellow-600',
    practicing: 'bg-orange-100 text-orange-600',
    mastered: 'bg-green-100 text-green-600'
  }

  return (
    <div className="h-full flex flex-col">
      {/* Word Display */}
      <div className="flex-1 flex flex-col items-center justify-center p-6">
        {/* Image placeholder */}
        <div className="w-32 h-32 bg-gradient-to-br from-blue-200 to-purple-200 rounded-2xl mb-6 flex items-center justify-center text-6xl">
          {currentWord.image_url ? (
            <img src={currentWord.image_url} alt="" className="w-full h-full object-cover rounded-2xl" />
          ) : (
            '📚'
          )}
        </div>

        {/* Status Badge */}
        {wordProgress && (
          <div className={`px-3 py-1 rounded-full text-xs font-semibold mb-4 ${
            statusColors[wordProgress.status as keyof typeof statusColors]
          }`}>
            {wordProgress.status.replace('_', ' ')}
          </div>
        )}

        {/* English Word */}
        <h2 className="text-4xl font-bold text-gray-800 mb-2">
          {enTranslation?.text || 'Loading...'}
        </h2>
        {enTranslation?.phonetic && (
          <p className="text-gray-500 text-sm mb-4">{enTranslation.phonetic}</p>
        )}

        {/* Translation (toggle to reveal) */}
        <div className="min-h-[60px] flex items-center justify-center">
          {showTranslation ? (
            <div className="text-center">
              <p className="text-2xl font-semibold text-blue-600">
                {targetTrans?.text || ''}
              </p>
              {targetTrans?.phonetic && (
                <p className="text-gray-500 text-sm">{targetTrans.phonetic}</p>
              )}
            </div>
          ) : (
            <button
              onClick={toggleTranslation}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          )}
        </div>

        {/* Example Sentence */}
        {enTranslation?.example_sentence && showTranslation && (
          <p className="text-gray-600 text-sm mt-4 text-center px-4">
            "{enTranslation.example_sentence}"
          </p>
        )}
      </div>

      {/* Practice Buttons */}
      <div className="p-4 bg-gray-50 border-t border-gray-200">
        {!showTranslation ? (
          <button
            onClick={toggleTranslation}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-xl font-semibold transition-colors"
          >
            Show Translation
          </button>
        ) : (
          <div className="flex gap-3">
            <button
              onClick={() => handlePractice(false)}
              disabled={isLoading}
              className="flex-1 bg-red-500 hover:bg-red-600 disabled:bg-red-300 text-white py-3 rounded-xl font-semibold transition-colors"
            >
              Practice More
            </button>
            <button
              onClick={() => handlePractice(true)}
              disabled={isLoading}
              className="flex-1 bg-green-500 hover:bg-green-600 disabled:bg-green-300 text-white py-3 rounded-xl font-semibold transition-colors"
            >
              I Know This!
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
