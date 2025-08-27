/**
 * Valide un fichier PDF
 * @param {File} file - Le fichier à valider
 * @returns {Object} - Résultat de la validation
 */
export function validatePdfFile(file) {
  if (!file) {
    return { isValid: false, error: "Aucun fichier sélectionné" }
  }

  if (file.type !== "application/pdf") {
    return { isValid: false, error: "Seuls les fichiers PDF sont acceptés" }
  }

  // Limite de taille: 50MB
  const maxSize = 50 * 1024 * 1024
  if (file.size > maxSize) {
    return { isValid: false, error: "Le fichier est trop volumineux (max 50MB)" }
  }

  return { isValid: true }
}

/**
 * Valide une question
 * @param {string} question - La question à valider
 * @returns {Object} - Résultat de la validation
 */
export function validateQuestion(question) {
  if (!question || question.trim() === "") {
    return { isValid: false, error: "La question ne peut pas être vide" }
  }

  if (question.trim().length < 3) {
    return { isValid: false, error: "La question doit contenir au moins 3 caractères" }
  }

  if (question.trim().length > 500) {
    return { isValid: false, error: "La question ne peut pas dépasser 500 caractères" }
  }

  return { isValid: true }
}
