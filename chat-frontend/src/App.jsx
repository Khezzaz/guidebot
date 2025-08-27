import { BrowserRouter } from "react-router-dom"
import { ErrorBoundary } from "./components/ErrorBoundary"
import Layout from "./components/Layout"
import AppRoutes from "./routes"

function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Layout>
          <AppRoutes />
        </Layout>
      </BrowserRouter>
    </ErrorBoundary>
  )
}

export default App
