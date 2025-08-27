const Loader = ({ size = "medium", className = "" }) => {
  const sizes = {
    small: "h-4 w-4",
    medium: "h-8 w-8",
    large: "h-12 w-12",
  }

  return (
    <div className={`flex justify-center items-center ${className}`}>
      <div className={`animate-spin rounded-full border-b-2 border-snrt-blue ${sizes[size]}`}></div>
    </div>
  )
}

export default Loader
