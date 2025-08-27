const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-snrt-primary mb-4">SNRT</h3>
            <p className="text-corporate-gray text-sm">Société Nationale de Radiodiffusion et de Télévision du Maroc</p>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-snrt-primary mb-4">Système de Gestion</h3>
            <ul className="space-y-2 text-sm text-corporate-gray">
              <li>Gestion des documents internes</li>
              <li>Assistant IA intelligent</li>
              <li>Base de connaissances centralisée</li>
            </ul>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-snrt-primary mb-4">Support</h3>
            <ul className="space-y-2 text-sm text-corporate-gray">
              <li>Guide d'utilisation</li>
              <li>Support technique</li>
              <li>Formation utilisateurs</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-200 mt-8 pt-8 text-center">
          <p className="text-sm text-corporate-gray">
            © 2024 SNRT. Tous droits réservés. Système interne de gestion des connaissances avec IA vocale.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
