import { useState, useEffect } from "react";
import { FaHome, FaAngleDown } from "react-icons/fa";
import { MdSportsCricket } from "react-icons/md";
import { RiMovie2Fill } from "react-icons/ri";
import { SiEventbrite } from "react-icons/si";
import { NavLink } from "react-router-dom";
import Select from "react-select";
import "./style.scss";
import cities from "../../cities/cities-name-list.json";
import AuthModal from "../login_rgister/AuthModal";
import { IoSearch } from "react-icons/io5";

const cityOptions = cities.map((city) => ({ label: city, value: city }));

const navbar = [
  { name: "Home", link: "/", icon: <FaHome size={22}/> },
  { name: "Movies", link: "/movies", icon: <RiMovie2Fill size={22}/> },
  { name: "Events", link: "/events", icon: <SiEventbrite size={22}/> },
  { name: "Sports", link: "/sports", icon: <MdSportsCricket size={22}/> },
];

const Navbar = () => {
  const [selectedState, setSelectedState] = useState("");
  const [popUp, setPopup] = useState(false);
  const [isLogin, setIsLogin] = useState(false);
  const [showAuthModal, setShowAuthModal] = useState(false);

  useEffect(() => {
    // Load stored state and tokens on mount
    const savedState = localStorage.getItem("userState");
    if (savedState) {
      setSelectedState(savedState);
    } else {
      setPopup(true);
    }

    const token = localStorage.getItem("access_token");
    setIsLogin(!!token); // Convert token existence to boolean
  }, []);

  const handleStateSelection = (selectedOption) => {
    const newState = selectedOption.value;
    setSelectedState(newState);
    localStorage.setItem("userState", newState);
    setPopup(false);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setIsLogin(false); // Update state
  };

  const handleLoginSuccess = () => {
    setIsLogin(true); // Ensure state updates on successful login
    setShowAuthModal(false)
  };

  return (
    <div className="nav">
      <div className="nav-first-line">
        <div className="logo">
          <NavLink className="nav-logo-name" to="/">
            <img className="nav-logo-img" src="logo.png" alt="Logo" />
            Tickettree
          </NavLink>
        </div>
        <div className="nav-search">
          <div className="nav-serach-box">
              <input type="text" placeholder="Search" />
              <IoSearch className="search-icon" />
          </div>
          <div
            className="nav-location"
            onClick={() => {
              setPopup(true);
            }}
          >
            {selectedState || "Select Location"}
            <FaAngleDown />
          </div>
        {/* login/logout button */}
        {isLogin ? (
          <div className="nav-bar-login" onClick={handleLogout}>
            Logout
          </div>
        ) : (
          <div className="nav-bar-login" onClick={() => setShowAuthModal(true)}>
            Login
          </div>
        )}
        </div>
      </div>
      <div className="navbar">
        {navbar.map((item, index) => (
          <NavLink
            key={index}
            to={item.link}
            className={({ isActive }) =>
              `${isActive ? "navLink active" : "navLink"}`
            }
          >
            {item.icon} {item.name}
          </NavLink>
        ))}
      </div>
      {/* select popup */}
      {popUp && (
        <div className="popup-overlay" onClick={() => setPopup(false)}>
          <div className="popup-content" onClick={(e) => e.stopPropagation()}>
            <h3>Select Your City</h3>
            <Select
              className="nav-popup-search"
              options={cityOptions}
              onChange={handleStateSelection}
              placeholder="Search "
            />
          </div>
        </div>
      )}
      {/* Show AuthModal if clicked */}
      {showAuthModal && <AuthModal close={() => setShowAuthModal(false)} onSuccess={handleLoginSuccess} />}
    </div>
  );
};

export default Navbar;
