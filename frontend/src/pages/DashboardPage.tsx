import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import { useDomainStore } from '@/stores/domainStore'
import DomainGraph from '@/components/ParentDashboard/DomainGraph'
import ProgressOverview from '@/components/ParentDashboard/ProgressOverview'

export default function DashboardPage() {
  const navigate = useNavigate()
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)
  const children = useAuthStore((state) => state.children)
  const selectedChildId = useAuthStore((state) => state.selectedChildId)
  const setSelectedChildId = useAuthStore((state) => state.setSelectedChildId)
  const fetchChildren = useAuthStore((state) => state.fetchChildren)

  const domains = useDomainStore((state) => state.domains)
  const fetchDomains = useDomainStore((state) => state.fetchDomains)

  const [selectedDomainId, setSelectedDomainId] = useState<string | null>(null)

  useEffect(() => {
    if (!user) {
      navigate('/login')
      return
    }
    fetchDomains()
    fetchChildren()
  }, [user]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const selectedChild = children.find(c => c.id === selectedChildId)
  const selectedDomain = domains.find(d => d.id === selectedDomainId)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold text-blue-600">LearningToy</h1>
            {user && <span className="text-gray-600">{user.email}</span>}
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/device')}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
            >
              Device Mode
            </button>
            <button
              onClick={handleLogout}
              className="text-gray-600 hover:text-gray-800"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Child Selector */}
        {children.length > 0 && (
          <div className="mb-6 bg-white rounded-xl p-4 shadow-sm">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Child
            </label>
            <div className="flex gap-2">
              {children.map(child => (
                <button
                  key={child.id}
                  onClick={() => setSelectedChildId(child.id)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    selectedChildId === child.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {child.name}
                </button>
              ))}
            </div>
          </div>
        )}

        {selectedChild ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Domain List */}
            <div className="lg:col-span-1">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Domains</h2>
              <div className="space-y-2">
                {domains.map(domain => (
                  <button
                    key={domain.id}
                    onClick={() => setSelectedDomainId(domain.id)}
                    className={`w-full text-left p-4 rounded-xl transition-all ${
                      selectedDomainId === domain.id
                        ? 'bg-blue-600 text-white shadow-md'
                        : 'bg-white hover:bg-gray-100 shadow-sm'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      {domain.icon && <span className="text-2xl">{domain.icon}</span>}
                      <div>
                        <div className="font-semibold">{domain.name}</div>
                        <div className={`text-sm ${selectedDomainId === domain.id ? 'text-blue-100' : 'text-gray-500'}`}>
                          {domain.word_count} words
                        </div>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Content Area */}
            <div className="lg:col-span-2">
              {selectedDomain ? (
                <>
                  <ProgressOverview childId={selectedChild.id} domainId={selectedDomain.id} />
                  <DomainGraph domainId={selectedDomain.id} childId={selectedChild.id} />
                </>
              ) : (
                <div className="bg-white rounded-xl p-8 shadow-sm text-center">
                  <p className="text-gray-500">Select a domain to view progress</p>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-xl p-8 shadow-sm text-center">
            <p className="text-gray-500 mb-4">No children added yet. Add a child to get started!</p>
            <p className="text-sm text-gray-400">(Child creation coming soon)</p>
          </div>
        )}
      </main>
    </div>
  )
}
