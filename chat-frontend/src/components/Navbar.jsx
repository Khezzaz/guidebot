import { Link, useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  // State pour forcer le re-render après login/logout
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(localStorage.getItem("admin_token"))
  );

  // Chaque fois que la route change, on relit le token
  useEffect(() => {
    setIsAuthenticated(Boolean(localStorage.getItem("admin_token")));
  }, [location]);

  const handleLogout = () => {
    localStorage.removeItem("admin_token");
    setIsAuthenticated(false);
    navigate("/login");
  };

  return (
    <nav className="fixed top-0 left-0 right-0 bg-snrt-blue shadow-lg z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo SNRT */}
          <div className="flex items-center">
            <img
              className="h-8 w-auto"
              src="src/assets/snrt_logo.svg"
              alt="SNRT Logo"
            />
            <h1 className="ml-3 text-white text-xl font-bold">
              SNRT Assistant IA
            </h1>
          </div>

          {/* Liens de navigation */}
          <div className="flex items-center space-x-4">
            <Link
              to="/upload"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                location.pathname === "/upload"
                  ? "bg-snrt-red text-white"
                  : "text-gray-300 hover:bg-snrt-dark-blue hover:text-white"
              }`}
            >
              Upload PDF
            </Link>
            <Link
              to="/chat"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                location.pathname === "/chat"
                  ? "bg-snrt-red text-white"
                  : "text-gray-300 hover:bg-snrt-dark-blue hover:text-white"
              }`}
            >
              Chat
            </Link>

            {/* SEUL le bouton Déconnexion s'affiche si authentifié */}
            {isAuthenticated && (
              <button
                onClick={handleLogout}
                className="ml-4 px-3 py-2 bg-red-600 text-white rounded-md text-sm font-medium hover:bg-red-700 transition-colors"
              >
                Déconnexion
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
