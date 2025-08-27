import { ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"

const ActionCard = ({ title, description, icon: Icon, to, color = "blue" }) => {
  const colorClasses = {
    blue: "border-snrt-primary hover:border-snrt-dark",
    red: "border-snrt-accent hover:border-red-700",
    green: "border-green-500 hover:border-green-600",
  }

  return (
    <Link to={to} className="block">
      <div className={`card card-hover border-2 ${colorClasses[color]} transition-all duration-200 group`}>
        <div className="flex items-start space-x-4">
          <div
            className={`p-3 rounded-lg ${
              color === "blue"
                ? "bg-snrt-light text-snrt-primary"
                : color === "red"
                  ? "bg-red-50 text-snrt-accent"
                  : "bg-green-50 text-green-600"
            }`}
          >
            <Icon className="h-6 w-6" />
          </div>
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-corporate-dark-gray mb-2 group-hover:text-snrt-primary transition-colors">
              {title}
            </h3>
            <p className="text-corporate-gray mb-4">{description}</p>
            <div className="flex items-center text-snrt-primary font-medium group-hover:text-snrt-dark transition-colors">
              <span>Commencer</span>
              <ArrowRight className="h-4 w-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>
      </div>
    </Link>
  )
}

export default ActionCard
