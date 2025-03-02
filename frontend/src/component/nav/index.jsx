import { useState, useEffect } from "react";
import { FaHome, FaAngleDown } from "react-icons/fa";
import { MdSportsCricket } from "react-icons/md";
import { RiMovie2Fill } from "react-icons/ri";
import { SiEventbrite } from "react-icons/si";
import { NavLink } from "react-router-dom";
import Select from "react-select";
import Login from "../login_rgister/login"
import "./style.scss";
import cities from "../../cities/cities-name-list.json";

const cityOptions = cities.map((city) => ({ label: city, value: city }));

const navbar = [
  { name: "Home", link: "/", icon: <FaHome /> },
  { name: "Movies", link: "/movies", icon: <RiMovie2Fill /> },
  { name: "Events", link: "/events", icon: <SiEventbrite /> },
  { name: "Sports", link: "/sports", icon: <MdSportsCricket /> },
];

const Navbar = () => {
  const [selectedState, setSelectedState] = useState("");
  const [popUp, setpopup] = useState(false);
  const [isLogin, setIsLogin] = useState(false);
  const [loginPage, setLoginPage] = useState(false)
  useEffect(() => {
    const savedState = localStorage.getItem("userState");
    if (savedState) {
      setSelectedState(savedState);
    } else {
      setpopup(true);
    }

    const token = localStorage.getItem("token")
    if(token){
      setIsLogin(true);
    }

  }, []);
  const handleStateSelection = (selectedOption) => {
    const newState = selectedOption.value;
    setSelectedState(newState); // Update state
    localStorage.setItem("userState", newState);
    setpopup(false);
  };

  return (
    <div className="nav">
      <div className="nav-bar-mobile">
        <div className="logo">
          <NavLink className="nav-logo-name" to="/">
            <img className="nav-logo-img" src="logo.png" alt="Logo" />
            Tickettree
          </NavLink>
        </div>
        <div className="nav-search">
          <input type="text" placeholder="Search" />
          <div
            className="nav-location"
            onClick={() => {
              setpopup(true);
            }} // Clear state to trigger popup
          >
            {selectedState || "Select Location"}
            <FaAngleDown />
          </div>
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
      {/* login button */}
      {isLogin ? (
        <div className="nav-bar-login" to="/logout">
          Logout
        </div>
      ) : (
        <div className="nav-bar-login" onClick={()=>setLoginPage(true)}>
          Login
        </div>
      )}
      {/* select popup */}
      {popUp && (
        <div className="popup-overlay" onClick={() => setpopup(false)}>
          <div className="popup-content" onClick={(e) => e.stopPropagation()}>
            <h3>Select Your City</h3>
            <Select
              className="nav-popup-search"
              options={cityOptions} // Corrected data format
              value={selectedState} // Updated value binding
              onChange={handleStateSelection}
              placeholder="Search "
            />
          </div>
        </div>
      )}
      {/* login page */}
      {loginPage && <Login close = {()=> setLoginPage(false)}/> }
    </div>
  );
};

export default Navbar;
