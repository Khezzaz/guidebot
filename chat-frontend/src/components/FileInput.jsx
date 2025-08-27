"use client"

const FileInput = ({ onChange, accept, disabled = false, className = "" }) => {
  return (
    <div className={`relative ${className}`}>
      <input
        type="file"
        accept={accept}
        onChange={onChange}
        disabled={disabled}
        className="block w-full text-sm text-gray-500
          file:mr-4 file:py-2 file:px-4
          file:rounded-lg file:border-0
          file:text-sm file:font-medium
          file:bg-snrt-blue file:text-white
          hover:file:bg-snrt-dark-blue
          file:cursor-pointer cursor-pointer
          disabled:opacity-50 disabled:cursor-not-allowed"
      />
    </div>
  )
}

export default FileInput
