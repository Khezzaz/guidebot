import { useLocation } from "react-router-dom"
import Header from "./Header"
import Footer from "./Footer"

const Layout = ({ children }) => {
  const location = useLocation()

  // On cache le footer si on est sur la route /chat (ajuste selon ta route exacte)
  const hideFooter = location.pathname === "/chat"

  return (
    <div className="min-h-screen bg-corporate-light-gray flex flex-col">
      <Header />
      <main className="flex-1 pt-20">{children}</main>
      {!hideFooter && <Footer />}
    </div>
  )
}

export default Layout
