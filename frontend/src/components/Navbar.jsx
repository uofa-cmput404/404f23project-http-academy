// import React from "react";
// import "../css/Navbar.css"
// import { useNavigate } from "react-router-dom";

// export default function Navbar() {

//     const navigate = useNavigate();
//     const goToPage = (page) => () => {
//         navigate(page);
//     };

//     return (
//         <div className="navbar">
//             <div className="logo">SDIST</div>
//             <div className="nav-items">
//             <button className="navButton" onClick={goToPage("/")}>Main</button>
//             <button className="navButton" onClick={goToPage("/home")}>Home</button>
//             <button className="navButton" onClick={goToPage("/login")}>Login</button>
//             <button className="navButton" onClick={goToPage("/post/create")}>Create a Post</button>
//             <button className="navButton" onClick={goToPage("/profile")}>Profile</button>
//             </div>
            
//         </div>
//     );
// }

import React, { useState } from "react";
import "../css/Navbar.css";
import { NavLink } from "react-router-dom"; 
import logoImage from '../assets/images/logo.png'; 
import Modal from "../components/Modal";
import {useAuth} from '../context/AuthContext'

export default function Navbar() {
    const [openModal, setOpenModal] = useState(false);
    const [modalMode, setModalMode] = useState("make");

    const {logout} = useAuth();

    return (
        <div className="navbar">
            <div className="logo">
                <img src={logoImage} alt="SDIST Logo" className="logo-image" />
                SDIST
            </div>
            <div className="nav-items">
                <NavLink activeClassName="active" className="navButton" to="/">Main</NavLink>
                <NavLink
                    to="/home"
                    className="navButton"
                    activeClassName="active"
                    isActive={(match, location) => {
                        return location.pathname.startsWith("/home") || location.pathname === "/";
                    }}
                >
                    Home
                </NavLink>
                <NavLink activeClassName="active" className="navButton" to="/login">Login</NavLink>
                {/* Replace NavLink with button for modal */}
                <button className="navButton" onClick={() => setOpenModal(true)}>Create a Post</button>
                <NavLink activeClassName="active" className="navButton" to="/profile">Profile</NavLink>
            </div>
            {/* <div className="logout-section">
                <NavLink activeClassName="active" className="navButton" to="/logout">Logout</NavLink>
            </div> */}

            <div className="logout-section">
                <button className="navButton" onClick={logout}>Logout</button>
            </div>

            {openModal && <Modal isOpen={openModal} mode = "make" onClose={() => setOpenModal(false)} />}
        </div>
    );
}
