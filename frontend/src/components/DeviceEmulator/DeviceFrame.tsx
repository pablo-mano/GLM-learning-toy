import { ReactNode } from 'react'

interface DeviceFrameProps {
  children: ReactNode
}

export default function DeviceFrame({ children }: DeviceFrameProps) {
  return (
    <div className="relative">
      {/* Device Frame */}
      <div className="bg-gray-800 rounded-[3rem] p-4 shadow-2xl">
        {/* Screen Bezel */}
        <div className="bg-black rounded-[2.5rem] p-2">
          {/* Screen */}
          <div className="bg-white rounded-[2rem] overflow-hidden"
               style={{ width: '360px', height: '480px' }}>
            {children}
          </div>
        </div>

        {/* Home Button */}
        <div className="flex justify-center mt-3">
          <div className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center">
            <div className="w-4 h-4 bg-gray-600 rounded-full" />
          </div>
        </div>
      </div>

      {/* Speaker Grills */}
      <div className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-2 flex flex-col gap-1">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="w-1 h-3 bg-gray-600 rounded-full" />
        ))}
      </div>
      <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-2 flex flex-col gap-1">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={i} className="w-1 h-3 bg-gray-600 rounded-full" />
        ))}
      </div>
    </div>
  )
}
