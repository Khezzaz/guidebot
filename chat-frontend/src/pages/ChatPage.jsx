"use client"

import { useState, useRef, useEffect } from "react"
import { Send, Bot, User, Trash2, Copy, Clock, FileText } from "lucide-react"
import ReactMarkdown from 'react-markdown'
import { sendQuery } from "../services/api"
import LoadingSpinner from "../components/LoadingSpinner"
import toast from "react-hot-toast"

const ChatPage = () => {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [topK, setTopK] = useState(5)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!inputValue.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      type: "user",
      content: inputValue.trim(),
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsLoading(true)

    try {
      const result = await sendQuery(inputValue.trim(), topK)

      if (result.success) {
        // Nettoyer la réponse en supprimant les balises <think>
        const cleanAnswer = cleanThinkTags(result.data.answer)
        
        const assistantMessage = {
          id: Date.now() + 1,
          type: "assistant",
          content: cleanAnswer,
          timestamp: new Date(),
          success: true,
          // Nouvelles données du backend
          sourcesCount: result.data.sources_count,
          chunksUsed: result.data.chunks_used || [],
          processingTime: result.data.processing_time,
          originalQuestion: result.data.question,
        }

        setMessages((prev) => [...prev, assistantMessage])

        // Afficher des infos supplémentaires si disponibles
        if (result.data.sources_count > 0) {
          toast.success(`Réponse générée à partir de ${result.data.sources_count} source(s)`)
        }
      } else {
        const errorMessage = {
          id: Date.now() + 1,
          type: "assistant",
          content: result.error || "Une erreur s'est produite lors du traitement de votre question.",
          timestamp: new Date(),
          success: false,
        }

        setMessages((prev) => [...prev, errorMessage])
        toast.error(result.error || "Aucune information pertinente trouvée")
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: "assistant",
        content: "Une erreur technique s'est produite. Veuillez réessayer.",
        timestamp: new Date(),
        success: false,
      }
      setMessages((prev) => [...prev, errorMessage])
      toast.error("Erreur de connexion")
    } finally {
      setIsLoading(false)
    }
  }

  const clearConversation = () => {
    setMessages([])
    toast.success("Conversation effacée")
  }

  const copyMessage = (content) => {
    navigator.clipboard.writeText(content)
    toast.success("Message copié")
  }

  const formatTime = (date) => {
    return new Intl.DateTimeFormat("fr-FR", {
      hour: "2-digit",
      minute: "2-digit",
    }).format(date)
  }

  const formatProcessingTime = (seconds) => {
    if (!seconds) return ""
    return seconds < 1 ? `${Math.round(seconds * 1000)}ms` : `${seconds.toFixed(2)}s`
  }

  // Fonction pour nettoyer les balises <think>
  const cleanThinkTags = (text) => {
    if (!text) return ""
    
    // Supprimer les balises <think>...</think> et leur contenu
    let cleanedText = text.replace(/<think>[\s\S]*?<\/think>/gi, "")
    
    // Nettoyer les espaces multiples et sauts de ligne en trop
    cleanedText = cleanedText.replace(/\n\s*\n\s*\n/g, "\n\n")
    cleanedText = cleanedText.trim()
    
    return cleanedText
  }

  // Composants personnalisés pour ReactMarkdown
  const markdownComponents = {
    // Titres
    h1: ({ children }) => (
      <h1 className="text-xl font-bold mb-3 text-corporate-dark-gray">{children}</h1>
    ),
    h2: ({ children }) => (
      <h2 className="text-lg font-semibold mb-2 text-corporate-dark-gray">{children}</h2>
    ),
    h3: ({ children }) => (
      <h3 className="text-base font-semibold mb-2 text-corporate-dark-gray">{children}</h3>
    ),
    
    // Paragraphes
    p: ({ children }) => (
      <p className="mb-2 leading-relaxed">{children}</p>
    ),
    
    // Listes
    ul: ({ children }) => (
      <ul className="list-disc list-inside mb-3 space-y-1 ml-4">{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal list-inside mb-3 space-y-1 ml-4">{children}</ol>
    ),
    li: ({ children }) => (
      <li className="leading-relaxed">{children}</li>
    ),
    
    // Code
    code: ({ inline, children }) => {
      if (inline) {
        return (
          <code className="bg-gray-100 text-gray-800 px-1.5 py-0.5 rounded text-sm font-mono">
            {children}
          </code>
        )
      }
      return (
        <pre className="bg-gray-50 border border-gray-200 rounded-lg p-3 mb-3 overflow-x-auto">
          <code className="text-sm font-mono text-gray-800">{children}</code>
        </pre>
      )
    },
    
    // Citations
    blockquote: ({ children }) => (
      <blockquote className="border-l-4 border-snrt-primary bg-snrt-light pl-4 py-2 mb-3 italic">
        {children}
      </blockquote>
    ),
    
    // Texte en gras et italique
    strong: ({ children }) => (
      <strong className="font-semibold text-corporate-dark-gray">{children}</strong>
    ),
    em: ({ children }) => (
      <em className="italic">{children}</em>
    ),
    
    // Liens (au cas où)
    a: ({ href, children }) => (
      <a 
        href={href} 
        className="text-snrt-primary hover:underline" 
        target="_blank" 
        rel="noopener noreferrer"
      >
        {children}
      </a>
    ),
  }

return (
  <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 h-[calc(100vh-8rem)]">
    <div className="flex flex-col h-full">
      
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-corporate-dark-gray">Assistant IA SNRT</h1>
          <p className="text-corporate-gray">
            Posez vos questions sur les procédures et documents internes
          </p>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-corporate-gray">Documents à analyser:</label>
            <select
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              className="px-3 py-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-snrt-primary"
            >
              {[...Array(10)].map((_, i) => (
                <option key={i + 1} value={i + 1}>
                  {i + 1}
                </option>
              ))}
            </select>
          </div>

          {messages.length > 0 && (
            <button
              onClick={clearConversation}
              className="flex items-center space-x-2 px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              <Trash2 className="h-4 w-4" />
              <span className="text-sm">Effacer</span>
            </button>
          )}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 bg-white rounded-xl shadow-corporate border border-gray-100 flex flex-col">
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          
          {/* Empty Chat Welcome */}
          {messages.length === 0 ? (
            <div className="text-center py-12">
              <Bot className="h-16 w-16 text-corporate-gray mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-corporate-dark-gray mb-2">
                Bienvenue dans l'Assistant IA SNRT
              </h3>
              <p className="text-corporate-gray max-w-md mx-auto mb-4">
                Posez vos questions sur les procédures internes, les documents uploadés ou toute information
                disponible dans la base de connaissances.
              </p>
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`flex space-x-3 max-w-4xl ${message.type === "user" ? "flex-row-reverse space-x-reverse" : ""}`}
                >
                  {/* Avatar */}
                  <div
                    className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                      message.type === "user"
                        ? "bg-snrt-primary text-white"
                        : message.success === false
                        ? "bg-red-100 text-red-600"
                        : "bg-snrt-light text-snrt-primary"
                    }`}
                  >
                    {message.type === "user" ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
                  </div>

                  {/* Message Bubble */}
                  <div className={`flex-1 ${message.type === "user" ? "text-right" : ""}`}>
                    <div
                      className={`inline-block p-4 rounded-xl ${
                        message.type === "user"
                          ? "bg-snrt-primary text-white"
                          : message.success === false
                          ? "bg-red-50 border border-red-200 text-red-800"
                          : "bg-gray-50 border border-gray-200 text-corporate-dark-gray"
                      }`}
                    >
                      {message.type === "assistant" && message.success ? (
                        <div className="prose prose-sm max-w-none">
                          <ReactMarkdown components={markdownComponents}>
                            {message.content}
                          </ReactMarkdown>
                        </div>
                      ) : (
                        <p className="whitespace-pre-wrap">{message.content}</p>
                      )}

                      {/* Metadata */}
                      {message.type === "assistant" && message.success && (
                        <div className="mt-3 pt-3 border-t border-gray-300 text-xs text-gray-600 space-y-1">
                          {message.sourcesCount > 0 && (
                            <div className="flex items-center space-x-1">
                              <FileText className="h-3 w-3" />
                              <span>{message.sourcesCount} source(s) utilisée(s)</span>
                            </div>
                          )}
                          {message.processingTime && (
                            <div className="flex items-center space-x-1">
                              <Clock className="h-3 w-3" />
                              <span>Traité en {formatProcessingTime(message.processingTime)}</span>
                            </div>
                          )}
                          {message.chunksUsed && message.chunksUsed.length > 0 && (
                            <div className="mt-2">
                              <details className="cursor-pointer">
                                <summary className="text-xs text-gray-500 hover:text-gray-700">
                                  Voir les extraits utilisés ({message.chunksUsed.length})
                                </summary>
                                <div className="mt-2 space-y-1 max-h-32 overflow-y-auto">
                                  {message.chunksUsed.map((chunk, idx) => (
                                    <div key={idx} className="text-xs p-2 bg-gray-100 rounded text-gray-700">
                                      {typeof chunk === 'string' ? chunk : chunk.text || 'Extrait indisponible'}
                                    </div>
                                  ))}
                                </div>
                              </details>
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Footer */}
                    <div
                      className={`flex items-center mt-2 space-x-2 text-xs text-corporate-gray ${
                        message.type === "user" ? "justify-end" : "justify-start"
                      }`}
                    >
                      <span>{formatTime(message.timestamp)}</span>
                      <button
                        onClick={() => copyMessage(message.content)}
                        className="hover:text-snrt-primary transition-colors"
                      >
                        <Copy className="h-3 w-3" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}

          {/* Loading Indicator */}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex space-x-3 max-w-4xl">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-snrt-light text-snrt-primary flex items-center justify-center">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
                  <LoadingSpinner size="small" text="L'assistant réfléchit..." />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 p-4">
          <form onSubmit={handleSubmit} className="flex space-x-4">
            <div className="flex-1">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Posez votre question..."
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-snrt-primary focus:border-transparent resize-none"
                rows={1}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault()
                    handleSubmit(e)
                  }
                }}
                disabled={isLoading}
              />
              <div className="text-right text-xs text-corporate-gray mt-1">
                {inputValue.length}/500 caractères
              </div>
            </div>

            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading}
              className="btn-primary flex items-center space-x-2 px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="h-4 w-4" />
              <span>Envoyer</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
)

}

export default ChatPage