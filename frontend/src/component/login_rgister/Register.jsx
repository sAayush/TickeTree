import axios from "axios";
import { useState } from "react";

function Register({ switchToLogin, close }) {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");

  const handleFormChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault(); // Prevent page reload

    if (formData.confirmPassword !== formData.password) {
      setError("Confirm Password and Password don't match.");
      setTimeout(() => setError(""), 3000);
      return;
    }

    try {
      const { username, email, password } = formData; // Exclude confirmPassword
      const res = await axios.post("http://127.0.0.1:8000/api/account/register/", {
        username,
        email,
        password,
      });

      // Store tokens
      const { access, refresh } = res.data.token;
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);

      close(); // Close modal on success
    } catch (error) {
        console.error("Registration Error:", error.response?.data || error.message);
      
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
        <div className="login-page-header">Register</div>

        <form onSubmit={handleRegister} className="login-form">
          <label>Username</label>
          <input
            type="text"
            name="username"
            onChange={handleFormChange}
            value={formData.username}
            placeholder="Username"
            required
          />

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

          <label>Confirm Password</label>
          <input
            type="password"
            name="confirmPassword"
            onChange={handleFormChange}
            value={formData.confirmPassword}
            placeholder="Confirm Password"
            required
          />

          <button type="submit" className="login-page-btn">
            Register
          </button>
        </form>

        <div className="login-page-footer">
          Already have an account?{" "}
          <span className="login-page-createlink" onClick={switchToLogin}>
            Login
          </span>
        </div>

        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
}

export default Register;
