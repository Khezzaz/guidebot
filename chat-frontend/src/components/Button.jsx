"use client"

const Button = ({
  children,
  onClick,
  disabled = false,
  loading = false,
  variant = "primary",
  type = "button",
  className = "",
}) => {
  const baseClasses =
    "px-4 py-2 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2"

  const variants = {
    primary: "bg-snrt-blue text-white hover:bg-snrt-dark-blue focus:ring-snrt-blue disabled:bg-gray-400",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500 disabled:bg-gray-100",
    danger: "bg-snrt-red text-white hover:bg-red-700 focus:ring-snrt-red disabled:bg-gray-400",
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`${baseClasses} ${variants[variant]} ${className} ${
        disabled || loading ? "cursor-not-allowed opacity-50" : ""
      }`}
    >
      {loading ? (
        <div className="flex items-center">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
          Chargement...
        </div>
      ) : (
        children
      )}
    </button>
  )
}

export default Button
