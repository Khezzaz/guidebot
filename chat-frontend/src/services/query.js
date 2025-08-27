import api from "./api"

/**
 * Envoie une question au backend FastAPI pour interroger les documents
 * @param {string} question - La question à poser
 * @param {number} topK - Nombre de documents à récupérer (défaut: 5)
 * @returns {Promise} - Promesse avec la réponse du serveur
 */
export async function sendQuestion(question, topK = 5) {
  try {
    // Validation des paramètres
    if (!question || question.trim() === "") {
      throw new Error("La question ne peut pas être vide")
    }

    if (topK < 1 || topK > 20) {
      throw new Error("Le nombre de documents doit être entre 1 et 20")
    }

    // Préparation des données
    const requestData = {
      question: question.trim(),
      top_k: topK,
    }

    // Appel API
    const response = await api.post("/query", requestData)

    return {
      success: true,
      data: response.data,
      question: question,
      topK: topK,
    }
  } catch (error) {
    console.error("Erreur lors de la requête:", error)

    let errorMessage = "Erreur lors de l'envoi de la question"

    if (error.response) {
      // Erreur du serveur
      if (error.response.status === 404) {
        errorMessage = "Aucune information trouvée pour cette question"
      } else {
        errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage
      }
    } else if (error.request) {
      // Erreur réseau
      errorMessage = "Impossible de contacter le serveur"
    } else {
      // Erreur de validation ou autre
      errorMessage = error.message
    }

    return {
      success: false,
      error: errorMessage,
      question: question,
      topK: topK,
    }
  }
}
