import Logo from "../components/Logo";
import { useNavigate } from "react-router-dom";

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="home">
      <div className="home-content">

        <Logo />

        <p className="company">
          Built by XCINO Technologies Pvt Ltd
        </p>

        <p className="tagline">
          Intelligent document analysis powered by Artificial Intelligence
        </p>

        <button
          className="start-button"
          onClick={() => navigate("/upload")}
        >
          Start Analysis 🚀
        </button>

      </div>
    </div>
  );
}

export default HomePage;