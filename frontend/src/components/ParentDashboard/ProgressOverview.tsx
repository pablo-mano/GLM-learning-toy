import { useEffect, useState } from 'react'
import { progressService } from '@/services/progress.service'

interface ProgressOverviewProps {
  childId: string
  domainId: string
}

export default function ProgressOverview({ childId, domainId }: ProgressOverviewProps) {
  const [overview, setOverview] = useState({
    total_words: 0,
    mastered: 0,
    practicing: 0,
    in_progress: 0,
    unlocked: 0,
    locked: 0,
    total_attempts: 0,
    total_correct: 0,
    accuracy: 0
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadOverview()
  }, [childId, domainId])

  const loadOverview = async () => {
    setIsLoading(true)
    try {
      const data = await progressService.getOverview(childId)
      setOverview(data)
    } catch (error) {
      console.error('Failed to load overview:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const stats = [
    { label: 'Mastered', value: overview.mastered, color: 'bg-green-500', textColor: 'text-green-600' },
    { label: 'Practicing', value: overview.practicing, color: 'bg-orange-500', textColor: 'text-orange-600' },
    { label: 'In Progress', value: overview.in_progress, color: 'bg-yellow-500', textColor: 'text-yellow-600' },
    { label: 'Unlocked', value: overview.unlocked, color: 'bg-blue-500', textColor: 'text-blue-600' },
  ]

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm mb-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Progress Overview</h3>

      {isLoading ? (
        <div className="animate-pulse flex gap-4">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="flex-1 h-20 bg-gray-200 rounded-lg" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-4 gap-4">
          {stats.map(stat => (
            <div key={stat.label} className="text-center">
              <div className={`text-3xl font-bold ${stat.textColor}`}>{stat.value}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
              <div className="mt-2 h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className={`h-full ${stat.color} rounded-full`}
                  style={{ width: `${overview.total_words > 0 ? (stat.value / overview.total_words) * 100 : 0}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Overall Stats */}
      <div className="mt-4 pt-4 border-t border-gray-100 flex justify-between text-sm">
        <span className="text-gray-600">
          Total Attempts: <span className="font-semibold">{overview.total_attempts}</span>
        </span>
        <span className="text-gray-600">
          Accuracy: <span className={`font-semibold ${overview.accuracy >= 0.7 ? 'text-green-600' : 'text-yellow-600'}`}>
            {Math.round(overview.accuracy * 100)}%
          </span>
        </span>
      </div>
    </div>
  )
}
