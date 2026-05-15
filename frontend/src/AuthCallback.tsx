import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const AuthCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    
    const access_token = params.get("access_token");
    
    console.log(window.location.search);
    console.log(access_token)

    if (!access_token) return;

    localStorage.setItem("access_token", access_token);

    navigate("/dashboard");
  }, []);

  return <p>Logging you in...</p>;
};

export default AuthCallback;
