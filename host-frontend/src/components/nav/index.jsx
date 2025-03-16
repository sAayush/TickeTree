import { NavLink } from "react-router-dom";
import logo from "/logo.png";
import { IoLogOut } from "react-icons/io5";
import './style.scss'

export default function Navbar({ onLogout }) {
    return (
        <div className="nav-component">
            <NavLink to="/" className="logo">
                <img src={logo} alt="TicketTree Logo" />
                <span>Tickettree</span>
            </NavLink>
            <div className="logout-button" onClick={onLogout}>
                <IoLogOut className="nav-icon" />
                <span>Logout</span>
            </div>
        </div>
    );
}
