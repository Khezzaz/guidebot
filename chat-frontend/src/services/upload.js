import api from "./api"

/**
 * Upload un fichier PDF vers le backend FastAPI
 * @param {File} file - Le fichier PDF à uploader
 * @returns {Promise} - Promesse avec la réponse du serveur
 */
export async function uploadPdf(file) {
  try {
    // Validation du fichier
    if (!file) {
      throw new Error("Aucun fichier sélectionné")
    }

    if (file.type !== "application/pdf") {
      throw new Error("Seuls les fichiers PDF sont acceptés")
    }

    // Création du FormData pour l'upload
    const formData = new FormData()
    formData.append("file", file)

    // Appel API avec configuration spéciale pour l'upload
    const response = await api.post("/uploadPDF", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        console.log(`Upload progress: ${percentCompleted}%`)
      },
    })

    return {
      success: true,
      data: response.data,
      message: `Fichier '${file.name}' uploadé et indexé avec succès.`,
    }
  } catch (error) {
    console.error("Erreur lors de l'upload:", error)

    let errorMessage = "Erreur lors de l'upload du fichier"

    if (error.response) {
      // Erreur du serveur
      errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage
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
    }
  }
}
