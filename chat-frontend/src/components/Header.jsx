"use client"

import { Link, useLocation, useNavigate } from "react-router-dom"
import { Home, Upload, MessageCircle, Menu, X, LogOut } from "lucide-react"
import { useState, useEffect } from "react"

const Header = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(localStorage.getItem("admin_token"))
  )

  const navigation = [
    { name: "Accueil", href: "/", icon: Home },
    { name: "Upload Document", href: "/upload", icon: Upload },
    { name: "Assistant IA", href: "/chat", icon: MessageCircle },
  ]

  const isActive = (path) => location.pathname === path

  // Met à jour isAuthenticated lors des changements de route
  useEffect(() => {
    setIsAuthenticated(Boolean(localStorage.getItem("admin_token")))
  }, [location])

  const handleLogout = () => {
    localStorage.removeItem("admin_token")
    setIsAuthenticated(false)
    navigate("/login")
  }

  return (
    <header className="fixed top-0 left-0 right-0 bg-white shadow-corporate z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3">
              <img
                src="src/assets/snrt_logo.svg"
                alt="SNRT Logo"
                className="h-10 w-auto"
              />
              <div className="hidden sm:block">
                <h1 className="text-xl font-bold text-snrt-primary">
                  GuideBot
                </h1>
                <p className="text-sm text-corporate-gray">
                  SNRT - Société Nationale de Radiodiffusion et de Télévision
                </p>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive(item.href)
                      ? "bg-snrt-primary text-white"
                      : "text-corporate-gray hover:bg-snrt-light hover:text-snrt-primary"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              )
            })}

            {/* Bouton Déconnexion */}
            {isAuthenticated && (
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-4 py-2 ml-4 rounded-lg text-sm font-medium bg-red-600 text-white hover:bg-red-700 transition-colors"
              >
                <LogOut className="h-4 w-4" />
                <span>Déconnexion</span>
              </button>
            )}
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="p-2 rounded-md text-corporate-gray hover:text-snrt-primary hover:bg-snrt-light"
            >
              {isMobileMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navigation.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-base font-medium transition-colors ${
                      isActive(item.href)
                        ? "bg-snrt-primary text-white"
                        : "text-corporate-gray hover:bg-snrt-light hover:text-snrt-primary"
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{item.name}</span>
                  </Link>
                )
              })}

              {/* Mobile Logout */}
              {isAuthenticated && (
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 px-3 py-2 mt-2 rounded-md text-base font-medium bg-red-600 text-white hover:bg-red-700 transition-colors"
                >
                  <LogOut className="h-5 w-5" />
                  <span>Déconnexion</span>
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  )
}

export default Header