"use client"

import { useState, useRef, useEffect } from "react"
import { Upload, File, CheckCircle, AlertCircle, X, Trash2, Eye, Clock, Hash } from "lucide-react"
import { uploadPdf, getAllDocuments, deleteDocumentByHash, getDocumentDetails } from "../services/api"
import LoadingSpinner from "../components/LoadingSpinner"
import toast from "react-hot-toast"
import LoginForm from "../components/LoginForm"

const UploadPage = () => {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [systemName, setSystemName] = useState("")
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadStatus, setUploadStatus] = useState(null) 
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [existingDocuments, setExistingDocuments] = useState([])
  const [documentsLoading, setDocumentsLoading] = useState(false)
  const [totalDocuments, setTotalDocuments] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [documentsPerPage] = useState(10)
  const [selectedDocument, setSelectedDocument] = useState(null)
  const [documentDetails, setDocumentDetails] = useState(null)
  const fileInputRef = useRef(null)

  useEffect(() => {
    const token = localStorage.getItem("admin_token")
    if (token) {
      setIsAuthenticated(true)
      fetchDocuments()
    }
  }, [currentPage])

  const handleLoginSuccess = () => {
    setIsAuthenticated(true)
    fetchDocuments()
  }

  const fetchDocuments = async () => {
    setDocumentsLoading(true)
    try {
      const result = await getAllDocuments(currentPage, documentsPerPage)
      
      if (result.success) {
        setExistingDocuments(result.data.documents || [])
        setTotalDocuments(result.data.total || 0)
      } else {
        toast.error(result.error || "Erreur lors du chargement des documents")
        setExistingDocuments([])
        setTotalDocuments(0)
      }
    } catch (error) {
      toast.error("Erreur lors du chargement des documents existants")
      setExistingDocuments([])
      setTotalDocuments(0)
    } finally {
      setDocumentsLoading(false)
    }
  }

  const viewDocumentDetails = async (fileHash) => {
    try {
      const result = await getDocumentDetails(fileHash)
      if (result.success) {
        setDocumentDetails(result.data)
        setSelectedDocument(fileHash)
      } else {
        toast.error(result.error || "Erreur lors de la récupération des détails")
      }
    } catch (error) {
      toast.error("Erreur lors de la récupération des détails du document")
    }
  }

  const handleDelete = async (fileHash) => {
    if (!confirm("Voulez-vous vraiment supprimer ce document ?")) return

    try {
      const result = await deleteDocumentByHash(fileHash)
      if (result.success) {
        toast.success("Document supprimé avec succès")
        fetchDocuments() // Recharge la liste
      } else {
        toast.error(result.error || "Erreur lors de la suppression du document")
      }
    } catch (error) {
      toast.error("Erreur lors de la suppression du document")
    }
  }

  if (!isAuthenticated) {
    return <LoginForm onLogin={handleLoginSuccess} />
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      handleFileSelection(files[0])
    }
  }

  const handleFileSelection = (file) => {
    if (file.type !== "application/pdf") {
      toast.error("Seuls les fichiers PDF sont acceptés")
      return
    }

    if (file.size > 50 * 1024 * 1024) {
      toast.error("Le fichier ne peut pas dépasser 50MB")
      return
    }

    setSelectedFile(file)
    setUploadStatus(null)
  }

  const handleFileInput = (e) => {
    const file = e.target.files[0]
    if (file) {
      handleFileSelection(file)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile || !systemName.trim()) {
      toast.error("Veuillez fournir le nom du système concerné")
      return
    }

    setUploading(true)
    setUploadProgress(0)
    setUploadStatus(null)

    try {
      const result = await uploadPdf(selectedFile, systemName, (progress) => {
        setUploadProgress(progress)
      })

      if (result.success) {
        setUploadStatus("success")
        toast.success(`Document "${selectedFile.name}" uploadé avec succès`)
        
        // Afficher les détails de l'upload si disponibles
        if (result.data?.file_hash) {
          console.log("Document ID:", result.data.document_id)
          console.log("File hash:", result.data.file_hash)
        }
        
        fetchDocuments() // Recharge la liste
        setTimeout(() => {
          setSelectedFile(null)
          setUploadStatus(null)
          setUploadProgress(0)
          setSystemName("")
        }, 3000)
      } else {
        setUploadStatus("error")
        if (result.duplicate) {
          toast.error("⚠️ Ce fichier existe déjà dans la base de connaissances.")
        } else {
          toast.error(result.error || "Erreur lors de l'upload")
        }
      }
    } catch (error) {
      setUploadStatus("error")
      toast.error("Une erreur inattendue s'est produite")
    } finally {
      setUploading(false)
    }
  }

  const removeFile = () => {
    setSelectedFile(null)
    setUploadStatus(null)
    setUploadProgress(0)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const formatFileSize = (bytes) => {
    if (!bytes || bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  const formatDate = (dateString) => {
    if (!dateString) return "Date inconnue"
    try {
      return new Intl.DateTimeFormat("fr-FR", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }).format(new Date(dateString))
    } catch {
      return dateString
    }
  }

  const totalPages = Math.ceil(totalDocuments / documentsPerPage)

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-corporate-dark-gray mb-4">Upload de Documents</h1>
        <p className="text-lg text-corporate-gray max-w-2xl mx-auto">
          Ajoutez de nouveaux documents PDF à la base de connaissances pour enrichir l'assistant IA avec vos procédures
          et informations internes.
        </p>
      </div>

      {/* Upload Area */}
      <div className="card mb-8">
        <div
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${
            dragActive
              ? "border-snrt-primary bg-snrt-light"
              : selectedFile
              ? "border-green-300 bg-green-50"
              : "border-gray-300 hover:border-snrt-primary hover:bg-snrt-light"
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          {!selectedFile ? (
            <>
              <Upload className="h-16 w-16 text-corporate-gray mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-corporate-dark-gray mb-2">
                Glissez-déposez votre fichier PDF ici
              </h3>
              <p className="text-corporate-gray mb-6">ou cliquez pour sélectionner un fichier</p>
              <button onClick={() => fileInputRef.current?.click()} className="btn-primary" disabled={uploading}>
                Sélectionner un fichier
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf"
                onChange={handleFileInput}
                className="hidden"
              />
              <p className="text-sm text-corporate-gray mt-4">Formats acceptés: PDF • Taille maximale: 50MB</p>
            </>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-center space-x-3">
                <File className="h-8 w-8 text-snrt-primary" />
                <div className="text-left">
                  <p className="font-semibold text-corporate-dark-gray">{selectedFile.name}</p>
                  <p className="text-sm text-corporate-gray">{formatFileSize(selectedFile.size)}</p>
                </div>
                {!uploading && uploadStatus !== "success" && (
                  <button onClick={removeFile} className="p-1 hover:bg-red-100 rounded-full transition-colors">
                    <X className="h-5 w-5 text-red-500" />
                  </button>
                )}
              </div>

              <input
                type="text"
                placeholder="Nom du système concerné (obligatoire)"
                value={systemName}
                onChange={(e) => setSystemName(e.target.value)}
                className="w-full p-2 border rounded-md border-gray-300 focus:outline-none focus:ring-2 focus:ring-snrt-primary"
                required
              />

              {uploading && (
                <div className="space-y-2">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-snrt-primary h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-corporate-gray">Upload en cours... {uploadProgress}%</p>
                </div>
              )}

              {uploadStatus === "success" && (
                <div className="flex items-center justify-center space-x-2 text-green-600">
                  <CheckCircle className="h-5 w-5" />
                  <span className="font-medium">Document uploadé avec succès!</span>
                </div>
              )}

              {uploadStatus === "error" && (
                <div className="flex items-center justify-center space-x-2 text-red-600">
                  <AlertCircle className="h-5 w-5" />
                  <span className="font-medium">Erreur lors de l'upload</span>
                </div>
              )}

              {!uploading && uploadStatus !== "success" && (
                <button 
                  onClick={handleUpload} 
                  className="btn-primary" 
                  disabled={uploading || !systemName.trim()}
                >
                  Uploader le document
                </button>
              )}

              {uploading && (
                <div className="flex justify-center">
                  <LoadingSpinner text="Upload en cours..." />
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Instructions */}
      <div className="grid md:grid-cols-2 gap-8 mb-12">
        <div className="card">
          <h2 className="text-xl font-semibold text-corporate-dark-gray mb-4">Instructions d'Upload</h2>
          <ul className="space-y-3 text-corporate-gray">
            <li className="flex items-start space-x-2">
              <span className="text-snrt-primary font-bold">1.</span>
              <span>Sélectionnez un fichier PDF depuis votre ordinateur</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-snrt-primary font-bold">2.</span>
              <span>Spécifiez le nom du système concerné</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-snrt-primary font-bold">3.</span>
              <span>Vérifiez que le fichier ne dépasse pas 50MB</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-snrt-primary font-bold">4.</span>
              <span>Cliquez sur "Uploader" pour indexer le document</span>
            </li>
          </ul>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold text-corporate-dark-gray mb-4">Bonnes Pratiques</h2>
          <ul className="space-y-3 text-corporate-gray">
            <li className="flex items-start space-x-2">
              <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
              <span>Utilisez des noms de fichiers descriptifs</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
              <span>Assurez-vous que le texte est lisible</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
              <span>Organisez vos documents par système</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
              <span>Mettez à jour régulièrement vos procédures</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Documents existants */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-corporate-dark-gray">
            Documents existants ({totalDocuments})
          </h2>
          <button 
            onClick={fetchDocuments}
            className="text-sm px-3 py-1 bg-snrt-primary text-white rounded hover:bg-snrt-primary/90"
            disabled={documentsLoading}
          >
            {documentsLoading ? "Actualisation..." : "Actualiser"}
          </button>
        </div>

        {documentsLoading ? (
          <div className="text-center py-8">
            <LoadingSpinner text="Chargement des documents..." />
          </div>
        ) : existingDocuments.length === 0 ? (
          <p className="text-corporate-gray text-center py-8">Aucun document indexé.</p>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="border-b border-gray-200">
                  <tr className="text-left">
                    <th className="pb-3 font-medium text-corporate-dark-gray">Fichier</th>
                    <th className="pb-3 font-medium text-corporate-dark-gray">Système</th>
                    <th className="pb-3 font-medium text-corporate-dark-gray">Taille</th>
                    <th className="pb-3 font-medium text-corporate-dark-gray">Date</th>
                    <th className="pb-3 font-medium text-corporate-dark-gray">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {existingDocuments.map((doc) => (
                    <tr key={doc.file_hash} className="hover:bg-gray-50">
                      <td className="py-3 pr-4">
                        <div className="flex items-center space-x-3">
                          <File className="h-5 w-5 text-red-500 flex-shrink-0" />
                          <div className="min-w-0">
                            <p className="font-medium text-corporate-dark-gray truncate">
                              {doc.filename}
                            </p>
                            <p className="text-xs text-corporate-gray font-mono">
                              {doc.file_hash?.substring(0, 8)}...
                            </p>
                          </div>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className="inline-flex px-2 py-1 text-xs font-medium bg-snrt-light text-snrt-primary rounded-full">
                          {doc.system_name}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-corporate-gray">
                        {formatFileSize(doc.file_size)}
                      </td>
                      <td className="py-3 px-4 text-corporate-gray">
                        <div className="flex items-center space-x-1">
                          <Clock className="h-3 w-3" />
                          <span>{formatDate(doc.created_at)}</span>
                        </div>
                      </td>
                      <td className="py-3 pl-4">
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => viewDocumentDetails(doc.file_hash)}
                            className="p-1 text-blue-600 hover:text-blue-800 hover:bg-blue-100 rounded transition-colors"
                            title="Voir les détails"
                          >
                            <Eye className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(doc.file_hash)}
                            className="p-1 text-red-600 hover:text-red-800 hover:bg-red-100 rounded transition-colors"
                            title="Supprimer"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-between items-center mt-6 pt-4 border-t border-gray-200">
                <div className="text-sm text-corporate-gray">
                  Page {currentPage} sur {totalPages} ({totalDocuments} documents)
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                    className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Précédent
                  </button>
                  <div className="flex items-center space-x-1">
                    {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                      const pageNum = currentPage <= 3 ? i + 1 : 
                        currentPage >= totalPages - 2 ? totalPages - 4 + i : 
                        currentPage - 2 + i;
                      
                      return (
                        <button
                          key={pageNum}
                          onClick={() => setCurrentPage(pageNum)}
                          className={`px-3 py-1 text-sm rounded ${
                            pageNum === currentPage
                              ? "bg-snrt-primary text-white"
                              : "border border-gray-300 hover:bg-gray-50"
                          }`}
                        >
                          {pageNum}
                        </button>
                      );
                    })}
                  </div>
                  <button
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                    className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Suivant
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Modal de détails du document */}
      {selectedDocument && documentDetails && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold text-corporate-dark-gray">
                  Détails du document
                </h3>
                <button
                  onClick={() => {
                    setSelectedDocument(null);
                    setDocumentDetails(null);
                  }}
                  className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-corporate-gray">Nom du fichier</label>
                    <p className="text-corporate-dark-gray">{documentDetails.metadata?.filename}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-corporate-gray">Système</label>
                    <p className="text-corporate-dark-gray">{documentDetails.metadata?.system_name}</p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-corporate-gray">Date d'ajout</label>
                    <p className="text-corporate-dark-gray">{formatDate(documentDetails.metadata?.created_at)}</p>
                  </div>
                </div>

                <div>
                  <label className="text-sm font-medium text-corporate-gray">Hash du fichier</label>
                  <p className="text-corporate-dark-gray font-mono text-xs bg-gray-100 p-2 rounded">
                    {documentDetails.metadata?.file_hash}
                  </p>
                </div>
              </div>

              <div className="flex justify-end space-x-3 mt-6 pt-4 border-t border-gray-200">
                <button
                  onClick={() => {
                    setSelectedDocument(null);
                    setDocumentDetails(null);
                  }}
                  className="px-4 py-2 text-corporate-gray hover:text-corporate-dark-gray transition-colors"
                >
                  Fermer
                </button>
                <button
                  onClick={() => {
                    handleDelete(selectedDocument);
                    setSelectedDocument(null);
                    setDocumentDetails(null);
                  }}
                  className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
                >
                  Supprimer ce document
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default UploadPage