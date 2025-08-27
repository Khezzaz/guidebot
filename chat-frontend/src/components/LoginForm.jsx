"use client"

import { useState } from "react"
import { loginAdmin } from "../services/api"
import toast from "react-hot-toast"

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await loginAdmin(username, password)
      if (response?.access_token) {
        localStorage.setItem("admin_token", response.access_token)
        onLogin()
        toast.success("Authentification réussie")
      } else {
        toast.error("Nom d'utilisateur ou mot de passe incorrect")
      }
    } catch (error) {
      toast.error("Erreur lors de l'authentification")
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleLogin} className="max-w-md mx-auto p-6 card mt-10">
      <h2 className="text-2xl font-bold mb-4 text-center">Connexion Admin</h2>
      <input
        type="text"
        className="input mb-4 w-full"
        placeholder="Nom d'utilisateur"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="password"
        className="input mb-4 w-full"
        placeholder="Mot de passe"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit" className="btn-primary w-full" disabled={loading}>
        {loading ? "Connexion..." : "Se connecter"}
      </button>
    </form>
  )
}

export default LoginForm