

import React, { useState } from "react";
import { NavLink, useNavigate, useLocation } from "react-router-dom";
import "../css/Navbar.css";
import logoImage from '../assets/images/logo.png';
import Modal from "./Modal";
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
    const [openModal, setOpenModal] = useState(false);
    const { currentUser, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    
        const handleLogout = async () => {
            try {
                await logout();
                navigate("/login");
            } catch (error) {
                console.error("Failed to log out", error);
            }
        };
    
        if (location.pathname === '/login' || location.pathname === '/signup'){
            return null
        }

        return (
            <div className="navbar">
                <div className="logo">
                    <img src={logoImage} alt="SDIST Logo" className="logo-image" />
                    SDIST
                </div>
                <div className="nav-items">
                    <NavLink className={({ isActive }) => isActive ? "navButton active" : "navButton"} to="/">Main</NavLink>
                    <NavLink
                        to="/home"
                        className={({ isActive }) => isActive ? "navButton active" : "navButton"}
                    >
                        Home
                    </NavLink>
               
                
                    <button className="navButton" onClick={() => setOpenModal(true)}>Create a Post</button>
                    <NavLink className={({ isActive }) => isActive ? "navButton active" : "navButton"} to="/profile">Profile</NavLink>
                </div>
                
                <div className="logout-section">
                    <button className="navButton" onClick={handleLogout}>Logout</button>
                </div>
    
                {openModal && <Modal isOpen={openModal} mode="make" onClose={() => setOpenModal(false)} />}
            </div>
        );
    }


