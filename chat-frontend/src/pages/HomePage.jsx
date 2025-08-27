import { Upload, MessageCircle, FileText, Brain, Shield, Zap, Mic, Volume2 } from "lucide-react"
import ActionCard from "../components/ActionCard"

const HomePage = () => {
  const features = [
    {
      icon: FileText,
      title: "Gestion Documentaire",
      description: "Centralisez et organisez tous vos documents internes",
    },
    {
      icon: Brain,
      title: "Intelligence Artificielle",
      description: "Assistant IA pour répondre à vos questions instantanément",
    },
    {
      icon: Zap,
      title: "Recherche Rapide",
      description: "Trouvez l'information dont vous avez besoin en quelques secondes",
    },
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-bold text-corporate-dark-gray mb-6">
          Guide
          <span className="text-snrt-primary">Bot</span>
        </h1>
        <p className="text-xl text-corporate-gray max-w-3xl mx-auto mb-8">
          Plateforme intelligente pour la gestion des procédures internes et l'assistance par intelligence artificielle
          . Optimisez votre productivité avec notre système de gestion des connaissances
          centralisé.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="btn-primary text-lg px-8 py-3">Découvrir le système</button>
          <button className="btn-secondary text-lg px-8 py-3">Guide d'utilisation</button>
        </div>
      </div>

      {/* Action Cards */}
      <div className="grid md:grid-cols-2 gap-8 mb-16">
        <ActionCard
          title="Uploader un Document"
          description="Ajoutez de nouveaux documents PDF à la base de connaissances pour enrichir l'assistant IA avec vos procédures internes."
          icon={Upload}
          to="/upload"
          color="blue"
        />
        <ActionCard
          title="Assistant IA"
          description="Posez vos questions à l'assistant intelligent par texte et obtenez des réponses précises basées sur vos documents internes."
          icon={MessageCircle}
          to="/chat"
          color="red"
        />
      </div>

      {/* Features Section */}
      <div className="mb-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-corporate-dark-gray mb-4">Fonctionnalités Principales</h2>
          <p className="text-lg text-corporate-gray max-w-2xl mx-auto">
            Notre système offre des outils avancés pour optimiser la gestion de vos connaissances internes et améliorer
            l'efficacité de vos équipes avec des capacités vocales innovantes.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <div key={index} className="card text-center">
                <div className="bg-snrt-light p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                  <Icon className="h-8 w-8 text-snrt-primary" />
                </div>
                <h3 className="text-lg font-semibold text-corporate-dark-gray mb-2">{feature.title}</h3>
                <p className="text-corporate-gray text-sm">{feature.description}</p>
              </div>
            )
          })}
        </div>
      </div>

      {/* Quick Start Guide */}
      <div className="card bg-gradient-to-r from-snrt-light to-blue-50">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-corporate-dark-gray mb-4">Guide de Démarrage Rapide</h2>
          <p className="text-corporate-gray mb-8">Commencez à utiliser le système en quelques étapes simples</p>

          <div className="grid md:grid-cols-4 gap-6 text-left">
            <div className="flex items-start space-x-3">
              <div className="bg-snrt-primary text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">
                1
              </div>
              <div>
                <h3 className="font-semibold text-corporate-dark-gray mb-1">Uploadez vos documents</h3>
                <p className="text-sm text-corporate-gray">
                  Ajoutez vos procédures et documents PDF à la base de connaissances
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="bg-snrt-primary text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">
                2
              </div>
              <div>
                <h3 className="font-semibold text-corporate-dark-gray mb-1">Posez vos questions</h3>
                <p className="text-sm text-corporate-gray">
                  Utilisez l'assistant IA par texte ou par voix pour obtenir des réponses
                </p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="bg-snrt-primary text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">
                3
              </div>
              <div>
                <h3 className="font-semibold text-corporate-dark-gray mb-1">Consultez les sources</h3>
                <p className="text-sm text-corporate-gray">Vérifiez les références et sources des réponses fournies</p>
              </div>
            </div>

            
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage
