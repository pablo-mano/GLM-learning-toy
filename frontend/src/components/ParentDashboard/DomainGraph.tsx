import { useEffect, useState } from 'react'
import ReactFlow, { useNodesState, useEdgesState, Node, Edge, Controls, MiniMap, Background } from 'reactflow'
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

// Transform LearningGraph data to ReactFlow nodes using levels array for positioning
function transformToReactFlowNodes(graph: LearningGraph): Node[] {
  const nodes: Node[] = []

  // Iterate through levels array to position nodes hierarchically
  graph.levels.forEach((level, levelIndex) => {
    level.forEach((nodeId, indexInLevel) => {
      // Find the corresponding graph node
      const graphNode = graph.nodes.find(n => n.id === nodeId)
      if (!graphNode) return

      // Get label from translations (prefer en, fallback to pl, es, or '?')
      const translations = graphNode.translations
      const label = translations.en || translations.pl || translations.es || '?'

      // Calculate position based on level structure
      // Y-axis: levelIndex × 150 (vertical spacing between levels)
      // X-axis: indexInLevel × 200 (horizontal spacing within level)
      const position = {
        x: indexInLevel * 200,
        y: levelIndex * 150
      }

      nodes.push({
        id: graphNode.id,
        type: 'wordNode',
        position,
        data: {
          label,
          difficulty: graphNode.difficulty as 'beginner' | 'intermediate' | 'advanced'
        }
      })
    })
  })

  return nodes
}

// Transform LearningGraph edges to ReactFlow edges format
function transformToReactFlowEdges(graph: LearningGraph): Edge[] {
  return graph.edges.map((edge, index) => ({
    id: `edge-${edge.from}-${edge.to}-${index}`,
    source: edge.from,
    target: edge.to
  }))
}

export default function DomainGraph({ domainId, childId }: DomainGraphProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadGraph()
  }, [domainId])

  const loadGraph = async () => {
    setIsLoading(true)
    try {
      const data = await domainService.getDomainGraph(domainId)
      const reactFlowNodes = transformToReactFlowNodes(data)
      const reactFlowEdges = transformToReactFlowEdges(data)
      setNodes(reactFlowNodes)
      setEdges(reactFlowEdges)
    } catch (error) {
      console.error('Failed to load graph:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Learning Graph</h3>

      {isLoading ? (
        <div className="animate-pulse h-64 bg-gray-100 rounded-lg" />
      ) : nodes.length > 0 ? (
        <div className="relative h-[600px] border border-gray-200 rounded-lg">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            nodeTypes={nodeTypes}
            fitView
            minZoom={0.5}
            maxZoom={1.5}
          >
            <Controls />
            <MiniMap />
            <Background />
          </ReactFlow>

          {/* Legend */}
          <div className="absolute bottom-2 left-2 flex gap-3 bg-white/90 rounded-lg px-3 py-2 text-xs shadow-md z-10">
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
