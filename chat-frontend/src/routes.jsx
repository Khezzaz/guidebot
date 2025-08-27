import { Routes, Route, Navigate } from "react-router-dom"
import HomePage from "./pages/HomePage"
import UploadPage from "./pages/UploadPage"
import ChatPage from "./pages/ChatPage"

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/chat" element={<ChatPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default AppRoutes
