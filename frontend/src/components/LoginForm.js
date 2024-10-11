import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginForm = () => {
  // State for storing email and password
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the form from refreshing the page

    const credentials = { username, password };

    try {
      const response = await fetch("http://localhost:8000/api/auth/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      if (response.ok) {
        const data = await response.json();
        sessionStorage.setItem("token", data.token);
        sessionStorage.setItem("username", username)
        navigate('/home');

        
      } else {
        const errorData = await response.json();
        setError(errorData.detail || "Login failed");
      }
    } catch (err) {
      setError("Something went wrong");
    }
  };

  return (
    <div className="login-box">
      <div className="box">
        <h2>Login</h2>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <div>
            <label>Username:</label>
            <input
              type="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
