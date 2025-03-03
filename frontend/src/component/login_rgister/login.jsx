import { useState } from "react";
import "./style.scss";
import axios from "axios";

function Login({ switchToRegister, close }) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const handleFormChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/account/login/",
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log("API Response:", res.data); // Debugging

      // Extract tokens correctly
      const accessToken = res.data?.token?.access;
      const refreshToken = res.data?.token?.refresh;

      if (accessToken && refreshToken) {
        localStorage.setItem("access_token", accessToken);
        localStorage.setItem("refresh_token", refreshToken);
        console.log("Tokens stored successfully!");
      } else {
        console.error("Tokens missing in response:", res.data);
      }

      close();
    } catch (error) {
      console.error("Login Error:", error.response?.data || error.message);
    
      if (error.response?.data?.message) {
        // Extract only error messages, ignoring field names
        const errorMessages = Object.values(error.response.data.message)
          .flat() // Flatten nested arrays (if any)
          .join("\n"); // Join messages into a single string
    
        setError(errorMessages);
      } else {
        setError("Something went wrong. Please try again.");
      }
    
      setTimeout(() => setError(""), 5000);
    }
    
  };

  return (
    <div className="login" onClick={close}>
      <div className="login-container" onClick={(e) => e.stopPropagation()}>
        <div className="login-page-header">Login</div>

        {/* Form Element */}
        <form onSubmit={handleLogin} className="login-form">
          <label>Email</label>
          <input
            type="email"
            name="email"
            onChange={handleFormChange}
            value={formData.email}
            placeholder="Email"
            required
          />

          <label>Password</label>
          <input
            type="password"
            name="password"
            onChange={handleFormChange}
            value={formData.password}
            placeholder="Password"
            required
          />

          <button type="submit" className="login-page-btn">
            Login
          </button>
        </form>
        <div className="login-froget-password">Forget Password?</div>
        <div className="login-page-footer">
          Don&apos;t have an account?{" "}
          <span className="login-page-createlink" onClick={switchToRegister}>
            Create
          </span>{" "}
          one.
        </div>
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
}

export default Login;
