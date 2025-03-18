import logo from "/logo.png";
import "./style.scss";
export default function AuthModel({ children }) {
  return (
    <div className="model-container">
      <div className="model-main-container"style={{
            width:
              window.location.pathname === "/login" ? "50rem" : "40rem",
            height:
              window.location.pathname === "/login" ? "30rem" : "auto",
          }}>
        <div className="model-container-img">
          <img src={logo} />
        </div>
        <div
          className="model-content"
          
        >
          {children}
        </div>
      </div>
    </div>
  );
}
