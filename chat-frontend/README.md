# SNRT Knowledge Management System with Voice Interface

Système professionnel de gestion des connaissances internes pour SNRT (Société Nationale de Radiodiffusion et de Télévision du Maroc) avec assistant IA intelligent et interface vocale avancée.

## 🎯 Vue d'ensemble

Cette application React moderne offre une plateforme centralisée pour la gestion des documents internes et l'assistance par intelligence artificielle avec des capacités vocales complètes. Elle permet aux équipes SNRT de naviguer efficacement dans les procédures internes et d'obtenir des réponses instantanées grâce à un chatbot IA alimenté par FastAPI, avec support complet pour les interactions vocales.

## ✨ Fonctionnalités principales

### 🏠 Page d'accueil professionnelle
- Interface d'accueil avec branding SNRT corporate
- Cartes d'action pour navigation intuitive
- Présentation des fonctionnalités système
- Guide de démarrage rapide
- Mise en avant des capacités vocales

### 📄 Gestion documentaire avancée
- Upload de documents PDF par glisser-déposer
- Barre de progression en temps réel
- Validation automatique des fichiers
- Notifications de succès/erreur professionnelles
- Interface intuitive et responsive

### 🤖 Assistant IA avec interface vocale
- Interface de chat moderne et responsive
- **Enregistrement vocal en temps réel** avec visualisation audio
- **Upload de fichiers audio** (.wav, .mp3)
- **Transcription automatique** des messages vocaux
- Historique des conversations avec indicateurs vocaux
- Citations des sources consultées
- Paramétrage du nombre de documents analysés
- Gestion complète des états de chargement

### 🎙️ Capacités vocales avancées
- **Enregistrement vocal** avec contrôles play/pause/stop
- **Visualisation des ondes audio** pendant l'enregistrement
- **Support des fichiers audio** WAV et MP3
- **Transcription en temps réel** des questions vocales
- **Indicateurs visuels** pour les messages vocaux
- **Interface intuitive** pour l'interaction vocale

## 🛠️ Technologies utilisées

- **React 18** avec JSX
- **Vite** - Build tool moderne et rapide
- **React Router v6** - Navigation côté client
- **Tailwind CSS** - Framework CSS utilitaire avec design system
- **Axios** - Client HTTP pour les appels API
- **Framer Motion** - Animations fluides
- **React Hot Toast** - Notifications élégantes
- **Lucide React** - Icônes modernes
- **Web Audio API** - Enregistrement vocal natif

## 🏗️ Architecture technique

\`\`\`
src/
├── components/              # Composants réutilisables
│   ├── Layout.jsx          # Layout principal
│   ├── Header.jsx          # En-tête avec navigation
│   ├── Footer.jsx          # Pied de page corporate
│   ├── ErrorBoundary.jsx   # Gestion d'erreurs
│   ├── LoadingSpinner.jsx  # Indicateurs de chargement
│   ├── ActionCard.jsx      # Cartes d'action
│   ├── VoiceRecorder.jsx   # 🎙️ Enregistreur vocal avancé
│   └── AudioUpload.jsx     # 🎵 Upload de fichiers audio
├── pages/                  # Pages principales
│   ├── HomePage.jsx        # Page d'accueil avec présentation vocale
│   ├── UploadPage.jsx      # Upload de documents
│   └── ChatPage.jsx        # 🗣️ Interface de chat avec voix
├── services/               # Services API
│   └── api.js             # Configuration et appels API (+ audio)
├── App.jsx                # Composant racine
├── routes.jsx             # Configuration des routes
└── main.jsx              # Point d'entrée
\`\`\`

## 🚀 Installation et démarrage

### Prérequis
- Node.js 16+ 
- npm ou yarn
- Backend FastAPI configuré avec endpoints vocaux
- Microphone pour l'enregistrement vocal

### Installation
\`\`\`bash
# Cloner le projet
git clone <repository-url>
cd snrt-knowledge-system

# Installer les dépendances
npm install

# Lancer en développement
npm run dev
\`\`\`

L'application sera accessible sur `http://localhost:3000`

### Build production
\`\`\`bash
npm run build
npm run preview
\`\`\`

## ⚙️ Configuration

### Backend FastAPI
Configurez l'URL du backend dans `src/services/api.js`:
\`\`\`javascript
const API_BASE_URL = 'http://localhost:8000' // Votre URL backend
\`\`\`

### Endpoints requis
- `POST /uploadPDF` - Upload et vectorisation des PDF
- `POST /query` - Requêtes texte vers l'assistant IA
- `POST /ask-audio` - **Requêtes vocales** (nouveau)
  - Accepte les fichiers audio (.wav, .mp3)
  - Transcrit l'audio en texte
  - Traite comme une requête normale
  - Retourne la transcription + réponse IA

## 🎨 Design système corporate

### Palette de couleurs SNRT
- **Primaire**: #1e40af (Bleu SNRT)
- **Secondaire**: #3b82f6 (Bleu clair)
- **Accent**: #dc2626 (Rouge SNRT)
- **Corporate**: Gris professionnels

### Composants UI avancés
- Boutons avec états hover/focus/disabled
- Cartes avec ombres corporate
- Formulaires avec validation temps réel
- Notifications toast élégantes
- **Visualisations audio** animées
- **Contrôles vocaux** intuitifs
- Design responsive et accessible

## 📱 Pages et fonctionnalités détaillées

### Page d'accueil (`/`)
- Présentation du système avec focus vocal
- Navigation vers les fonctionnalités principales
- **Section dédiée aux capacités vocales**
- Guide de démarrage avec étapes vocales
- Aperçu des innovations IA

### Upload de documents (`/upload`)
- Zone de glisser-déposer intuitive
- Validation des fichiers PDF (max 50MB)
- Barre de progression d'upload
- Messages de statut professionnels
- Instructions et bonnes pratiques

### Assistant IA vocal (`/chat`)
- Interface de chat professionnelle
- **🎙️ Enregistrement vocal en temps réel**
- **🎵 Upload de fichiers audio**
- **📝 Transcription automatique**
- Historique avec indicateurs vocaux
- Citations des sources consultées
- Paramètres configurables (top_k)
- Gestion complète des erreurs

## 🎙️ Fonctionnalités vocales détaillées

### Enregistrement vocal
- **Interface intuitive** avec boutons record/pause/stop
- **Visualisation audio** avec ondes animées
- **Timer d'enregistrement** en temps réel
- **Prévisualisation** avant envoi
- **Contrôles de lecture** pour vérification

### Upload audio
- **Support des formats** WAV et MP3
- **Validation automatique** des fichiers
- **Limite de taille** configurable (10MB)
- **Feedback visuel** pendant le traitement

### Traitement IA
- **Transcription automatique** des messages vocaux
- **Traitement identique** aux requêtes texte
- **Réponses contextuelles** basées sur les documents
- **Citations des sources** pour les réponses audio

## 🔧 Développement

### Scripts disponibles
\`\`\`bash
npm run dev      # Développement avec hot reload
npm run build    # Build production optimisé
npm run preview  # Aperçu du build
npm run lint     # Vérification du code
\`\`\`

### Bonnes pratiques
- Composants fonctionnels avec hooks React
- Gestion d'état avec useState/useEffect
- Error boundaries pour la robustesse
- Code splitting automatique
- **Gestion des permissions microphone**
- **Optimisation des fichiers audio**

## 🛡️ Sécurité et performance

### Sécurité
- Validation côté client et serveur
- Gestion des permissions microphone
- **Validation des fichiers audio**
- **Timeouts configurables** pour le traitement audio
- Protection contre les uploads malveillants

### Performance
- Optimisation des bundles JavaScript
- Lazy loading des composants
- **Compression audio** automatique
- **Streaming des réponses** IA
- Cache intelligent des requêtes

## 📞 Support et maintenance

### Dépannage vocal
- Vérifier les permissions microphone du navigateur
- Contrôler la qualité audio d'enregistrement
- Tester les formats de fichiers supportés
- Consulter les logs de transcription

### Monitoring
- Logs d'erreurs dans la console
- **Métriques de qualité audio**
- **Temps de traitement vocal**
- Notifications utilisateur claires

## 🔄 Évolutions futures

### Fonctionnalités prévues
- **Synthèse vocale** des réponses IA
- **Reconnaissance vocale multilingue**
- **Commandes vocales** pour la navigation
- **Historique audio** persistant
- **Amélioration continue** de la transcription
- **Support des accents** marocains

### Intégrations
- Authentification utilisateur
- Gestion des rôles et permissions
- Export des conversations (audio inclus)
- Thème sombre avec mode vocal
- Support multilingue (arabe/français)

---

**SNRT - Société Nationale de Radiodiffusion et de Télévision**  
*Système de Gestion des Connaissances Internes avec IA Vocale*

## 🎯 Innovation technologique

Ce système représente une avancée majeure dans l'interaction homme-machine pour les environnements professionnels, combinant l'intelligence artificielle textuelle traditionnelle avec des capacités vocales de pointe pour une expérience utilisateur naturelle et efficace.
