"use client"

import React from "react"
import { AlertTriangle, RefreshCw } from "lucide-react"

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught by boundary:", error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-corporate-light-gray flex items-center justify-center p-4">
          <div className="card max-w-md w-full text-center">
            <AlertTriangle className="h-16 w-16 text-snrt-accent mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-corporate-dark-gray mb-2">Une erreur s'est produite</h1>
            <p className="text-corporate-gray mb-6">
              Nous nous excusons pour ce désagrément. Une erreur technique s'est produite.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="btn-primary flex items-center space-x-2 mx-auto"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Recharger la page</span>
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export { ErrorBoundary }
