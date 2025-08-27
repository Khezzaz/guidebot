import axios from "axios"
import toast from "react-hot-toast"

const API_BASE_URL = "http://localhost:8000"

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
  },
})

// Ajouter token JWT automatiquement
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("admin_token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Gérer les erreurs globales
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Si token expiré ou invalide
      localStorage.removeItem("admin_token")
      toast.error("Session expirée. Veuillez vous reconnecter.")
      window.location.href = "/login"
    } else {
      console.error("API Error:", error)
    }
    return Promise.reject(error)
  }
)

// ===== AUTHENTIFICATION =====
export const loginAdmin = async (username, password) => {
  try {
    const response = await api.post("/auth/login", { username, password })
    return response.data
  } catch (error) {
    console.error("Erreur d'authentification:", error)
    throw error
  }
}

export const getCurrentUser = async () => {
  try {
    const response = await api.get("/auth/me")
    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || "Erreur lors de la récupération des informations utilisateur",
    }
  }
}

export const logout = async () => {
  try {
    await api.post("/auth/logout")
    localStorage.removeItem("admin_token")
    return { success: true }
  } catch (error) {
    // Même en cas d'erreur, on supprime le token local
    localStorage.removeItem("admin_token")
    return { success: true }
  }
}

export const validateToken = async () => {
  try {
    const response = await api.post("/auth/validate-token")
    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || "Token invalide",
    }
  }
}

// ===== DOCUMENTS =====
export const uploadPdf = async (file, system_name, onProgress) => {
  const formData = new FormData()
  formData.append("file", file)
  formData.append("system_name", system_name)

  try {
    const response = await api.post("/documents/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(percent)
        }
      },
    })

    return {
      success: true,
      data: response.data,
      error: null,
      duplicate: false
    }
  } catch (error) {
    // Cas doublon détecté côté serveur
    if (
      error.response?.status === 400 &&
      typeof error.response.data?.detail === "string" &&
      error.response.data.detail.includes("déjà été vectorisé")
    ) {
      return {
        success: false,
        error: "Ce document a déjà été vectorisé auparavant.",
        duplicate: true
      }
    }
    // Autres erreurs
    return {
      success: false,
      error: error.response?.data?.detail || error.message,
      duplicate: false
    }
  }
}

export const getAllDocuments = async (page = 1, limit = 10) => {
  try {
    const response = await api.get("/documents/", {
      params: {
        page: page,
        limit: limit
      }
    })
    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    console.error("Erreur récupération des documents :", error)
    return {
      success: false,
      error: error.response?.data?.detail || "Erreur lors de la récupération des documents",
      data: { documents: [], total: 0 }
    }
  }
}

export const getDocumentDetails = async (fileHash) => {
  try {
    const response = await api.get(`/documents/${fileHash}`)
    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || "Erreur lors de la récupération des détails du document",
    }
  }
}

export const deleteDocumentByHash = async (fileHash) => {
  try {
    const response = await api.delete(`/documents/${fileHash}`)

    toast.success("Document supprimé avec succès")
    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    let errorMessage = "Erreur lors de la suppression du document"

    if (error.response?.status === 404) {
      errorMessage = "Document introuvable"
    } else if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail
    } else {
      errorMessage = error.message
    }

    toast.error(errorMessage)
    return {
      success: false,
      error: errorMessage,
    }
  }
}

export const checkDocumentsHealth = async () => {
  try {
    const response = await api.get("/documents/health/check")
    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || "Services indisponibles",
    }
  }
}

// ===== RECHERCHE & QUESTIONS =====
export const sendQuery = async (question, topK = 5, filters = null) => {
  try {
    if (!question || question.trim() === "") {
      throw new Error("La question ne peut pas être vide")
    }

    const requestBody = {
      question: question.trim(),
      top_k: topK,
    }

    if (filters) {
      requestBody.filters = filters
    }

    const response = await api.post("/search/query", requestBody)

    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    let errorMessage = "Erreur lors de l'envoi de la question"

    if (error.response) {
      if (error.response.status === 404) {
        errorMessage = "Aucune information pertinente trouvée dans la base de connaissances"
      } else {
        errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage
      }
    } else if (error.request) {
      errorMessage = "Impossible de contacter le serveur"
    } else {
      errorMessage = error.message
    }

    return {
      success: false,
      error: errorMessage,
    }
  }
}

export const semanticSearch = async (question, topK = 5, filters = null) => {
  try {
    if (!question || question.trim() === "") {
      throw new Error("La question ne peut pas être vide")
    }

    const requestBody = {
      question: question.trim(),
      top_k: topK,
    }

    if (filters) {
      requestBody.filters = filters
    }

    const response = await api.post("/search/semantic", requestBody)

    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || "Erreur lors de la recherche sémantique",
    }
  }
}

export const getSuggestions = async () => {
  try {
    const response = await api.get("/search/suggestions")
    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || "Erreur lors de la génération de suggestions",
    }
  }
}

export const getSearchStats = async () => {
  try {
    const response = await api.get("/search/stats")
    return {
      success: true,
      data: response.data,
    }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || "Erreur lors de la récupération des statistiques",
    }
  }
}

export default api