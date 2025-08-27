"use client"

const Alert = ({ type = "info", message, onClose }) => {
  const types = {
    success: "bg-green-50 border-green-200 text-green-800",
    error: "bg-red-50 border-red-200 text-red-800",
    warning: "bg-yellow-50 border-yellow-200 text-yellow-800",
    info: "bg-blue-50 border-blue-200 text-blue-800",
  }

  const icons = {
    success: "✓",
    error: "✕",
    warning: "⚠",
    info: "ℹ",
  }

  return (
    <div className={`border rounded-lg p-4 ${types[type]} relative`}>
      <div className="flex items-center">
        <span className="mr-2 font-bold">{icons[type]}</span>
        <span>{message}</span>
        {onClose && (
          <button onClick={onClose} className="ml-auto text-lg font-bold hover:opacity-70">
            ×
          </button>
        )}
      </div>
    </div>
  )
}

export default Alert
