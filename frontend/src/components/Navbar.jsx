import React from "react";
import "../css/Navbar.css"
import { useNavigate } from "react-router-dom";

export default function Navbar() {

    const navigate = useNavigate();
    const goToPage = (page) => () => {
        navigate(page);
    };

    return (
        <nav>
            <button className="navButton" onClick={goToPage("/")}>Main</button>
            <button className="navButton" onClick={goToPage("/home")}>Home</button>
            <button className="navButton" onClick={goToPage("/login")}>Login</button>
            <button className="navButton" onClick={goToPage("/post/create")}>Create a Post</button>
        </nav>
    );
}