import reactLogo from "./assets/react.svg";
import viteLogo from "./assets/vite.svg";
import heroImg from "./assets/hero.png";
import "./App.css";

function App() {
  const handleGoogleSignIn = () => {
    window.location.href = "http://127.0.0.1:5000/api/v1/auth/google";
  }

  return (
    <>
      <section id="center">
        <div className="hero">
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1>Get started</h1>
          <p>
            Join us in our journey to build a secure and user-friendly
            authentication system using Google Sign-In.
          </p>
        </div>
        <button
          type="button"
          className="counter"
          onClick={() => handleGoogleSignIn()}
        >
          Sign In with Google
        </button>
      </section>

      <div className="ticks"></div>

      <div className="ticks"></div>
    </>
  );
}

export default App;
