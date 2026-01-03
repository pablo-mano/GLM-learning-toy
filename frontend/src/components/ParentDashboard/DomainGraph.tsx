import { useEffect, useState } from 'react'
import ReactFlow, { useNodesState, useEdgesState, Node, Edge } from 'reactflow'
import 'reactflow/dist/style.css'
import { domainService } from '@/services/domain.service'
import type { LearningGraph } from '@/types/api'

interface DomainGraphProps {
  domainId: string
  childId: string
}

// Custom WordNode component
interface WordNodeData {
  label: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
}

function WordNode({ data }: { data: WordNodeData }) {
  const getNodeColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 border-green-400 text-green-700'
      case 'intermediate': return 'bg-yellow-100 border-yellow-400 text-yellow-700'
      case 'advanced': return 'bg-red-100 border-red-400 text-red-700'
      default: return 'bg-gray-100 border-gray-400 text-gray-700'
    }
  }

  const getNodeSize = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'w-20 h-20'
      case 'intermediate': return 'w-16 h-16'
      case 'advanced': return 'w-14 h-14'
      default: return 'w-16 h-16'
    }
  }

  return (
    <div className={`${getNodeColor(data.difficulty)} ${getNodeSize(data.difficulty)} rounded-full border-2 flex items-center justify-center p-2 text-xs font-medium text-center`}>
      {data.label}
    </div>
  )
}

// NodeTypes object for ReactFlow
const nodeTypes = {
  wordNode: WordNode
}

export default function DomainGraph({ domainId, childId }: DomainGraphProps) {
  const [graph, setGraph] = useState<LearningGraph | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadGraph()
  }, [domainId])

  const loadGraph = async () => {
    setIsLoading(true)
    try {
      const data = await domainService.getDomainGraph(domainId)
      setGraph(data)
    } catch (error) {
      console.error('Failed to load graph:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const getNodeColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 border-green-400 text-green-700'
      case 'intermediate': return 'bg-yellow-100 border-yellow-400 text-yellow-700'
      case 'advanced': return 'bg-red-100 border-red-400 text-red-700'
      default: return 'bg-gray-100 border-gray-400 text-gray-700'
    }
  }

  const getNodeSize = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'w-20 h-20'
      case 'intermediate': return 'w-16 h-16'
      case 'advanced': return 'w-14 h-14'
      default: return 'w-16 h-16'
    }
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Learning Graph</h3>

      {isLoading ? (
        <div className="animate-pulse h-64 bg-gray-100 rounded-lg" />
      ) : graph ? (
        <div className="relative h-80 overflow-auto">
          {/* Simple SVG visualization of the graph */}
          <svg className="w-full h-full min-w-[500px]" viewBox="0 0 500 300">
            {/* Edges */}
            {graph.edges.map((edge, i) => {
              const fromNode = graph.nodes.find(n => n.id === edge.from)
              const toNode = graph.nodes.find(n => n.id === edge.to)
              if (!fromNode || !toNode) return null

              const fromX = (graph.nodes.indexOf(fromNode) % 5) * 100 + 50
              const fromY = Math.floor(graph.nodes.indexOf(fromNode) / 5) * 80 + 40
              const toX = (graph.nodes.indexOf(toNode) % 5) * 100 + 50
              const toY = Math.floor(graph.nodes.indexOf(toNode) / 5) * 80 + 40

              return (
                <line
                  key={i}
                  x1={fromX}
                  y1={fromY}
                  x2={toX}
                  y2={toY}
                  stroke="#cbd5e1"
                  strokeWidth="2"
                  markerEnd="url(#arrowhead)"
                />
              )
            })}

            {/* Arrow marker definition */}
            <defs>
              <marker
                id="arrowhead"
                markerWidth="10"
                markerHeight="7"
                refX="9"
                refY="3.5"
                orient="auto"
              >
                <polygon points="0 0, 10 3.5, 0 7" fill="#cbd5e1" />
              </marker>
            </defs>

            {/* Nodes */}
            {graph.nodes.map((node, i) => {
              const x = (i % 5) * 100 + 50
              const y = Math.floor(i / 5) * 80 + 40

              const translations = node.translations
              const label = translations.en || translations.pl || translations.es || '?'

              return (
                <g key={node.id}>
                  <circle
                    cx={x}
                    cy={y}
                    r={node.difficulty === 'beginner' ? 28 : node.difficulty === 'intermediate' ? 24 : 20}
                    fill={node.difficulty === 'beginner' ? '#dcfce7' : node.difficulty === 'intermediate' ? '#fef9c3' : '#fecaca'}
                    stroke={node.difficulty === 'beginner' ? '#4ade80' : node.difficulty === 'intermediate' ? '#facc15' : '#f87171'}
                    strokeWidth="2"
                  />
                  <text
                    x={x}
                    y={y + 4}
                    textAnchor="middle"
                    className="text-xs font-medium"
                    fill="#374151"
                  >
                    {label.slice(0, 8)}
                  </text>
                </g>
              )
            })}
          </svg>

          {/* Legend */}
          <div className="absolute bottom-2 left-2 flex gap-3 bg-white/90 rounded-lg px-3 py-2 text-xs">
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-green-200 border border-green-400" />
              Beginner
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-yellow-200 border border-yellow-400" />
              Intermediate
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-red-200 border border-red-400" />
              Advanced
            </span>
          </div>
        </div>
      ) : (
        <p className="text-gray-500 text-center py-8">No graph data available</p>
      )}
    </div>
  )
}
