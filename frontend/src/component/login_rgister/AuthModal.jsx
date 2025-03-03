import { useState } from "react";
import Login from "./Login";
import Register from "./Register";

const AuthModal = ({ close }) => {
  const [currentPage, setCurrentPage] = useState("login"); // Default to login

  return (
    <div className="auth-modal" onClick={close}>
      <div className="auth-modal-content" onClick={(e) => e.stopPropagation()}>
        {currentPage === "login" ? (
          <Login switchToRegister={() => setCurrentPage("register")} close={close} />
        ) : (
          <Register switchToLogin={() => setCurrentPage("login")} close={close} />
        )}
      </div>
    </div>
  );
};

export default AuthModal;
