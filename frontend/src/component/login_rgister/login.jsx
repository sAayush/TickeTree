import { NavLink } from "react-router-dom";
import { useState } from "react";
import "./style.scss";
import axios from "axios";

function Login({ close }) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleFormChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // const handleLogin = () => {
  //   console.log("Logging in with:", formData);
  //   try{
  //     const res = axios.post()
  //   }
  // };

  return (
    <div className="login" onClick={close}>
      <div className="login-container" onClick={(e) => e.stopPropagation()}>
        <div className="login-page-header">Login</div>
        <div className="login-form">
          <label>Email</label>
          <input
            type="email"
            name="email"
            onChange={handleFormChange}
            value={formData.email}
            placeholder="Email"
          />
          <label>Password</label>
          <input
            type="password"
            name="password"
            onChange={handleFormChange}
            value={formData.password}
            placeholder="Password"
          />
        </div>
        <button className="login-page-btn" onClick={handleLogin}>
          Login
        </button>
        <div className="login-page-footer">
          Don&apos;t have an account? <NavLink to="/register">Register</NavLink> one
        </div>
      </div>
    </div>
  );
}

export default Login;
