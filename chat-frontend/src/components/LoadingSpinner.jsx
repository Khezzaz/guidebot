import { Loader2 } from "lucide-react"

const LoadingSpinner = ({ size = "medium", text = "Chargement..." }) => {
  const sizeClasses = {
    small: "h-4 w-4",
    medium: "h-8 w-8",
    large: "h-12 w-12",
  }

  return (
    <div className="flex flex-col items-center justify-center space-y-2">
      <Loader2 className={`animate-spin text-snrt-primary ${sizeClasses[size]}`} />
      {text && <p className="text-sm text-corporate-gray">{text}</p>}
    </div>
  )
}

export default LoadingSpinner
