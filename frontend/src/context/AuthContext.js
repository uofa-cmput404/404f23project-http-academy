
import React, { createContext, useState, useContext, useEffect } from 'react';
import axiosInstance from '../axiosInstance';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);


    useEffect(() => {
        const user = localStorage.getItem('user');
        setIsAuthenticated(!!user); // we use localstorage so that the user session persists 
    }, []);

    const loginUser = async (email, password, callback) => {
        try {
            const res = await axiosInstance.post("/authors/login", { email, password });
            localStorage.setItem('user', JSON.stringify(res.data));
            const author = JSON.parse(localStorage.getItem('user'));
            console.log('authcontextuser', author)
            setIsAuthenticated(true);
            if (callback) callback(); 
        } catch (error) {
            console.error('Login failed', error);
            throw error;
        }
    };

    const registerUser = async (email, 
        username, 
        password, 
        github, 
        profileImage, callback) => {
            console.log('data sent', email, 
            username, 
            password, 
            github, 
            profileImage )
        try {
            await axiosInstance.post("/authors/register", {email, 
                username, 
                password, 
                github, 
                profileImage });
            // Log in the user after registration
            await loginUser(email, password);
            if (callback) callback(); 
        } catch (error) {
            console.error('Registration failed', error);
            throw error; 
        }
    };
    

    const logout = () => {
        axiosInstance.post("/authors/logout", { withCredentials: true })
            .then(function (res) {
                localStorage.removeItem('user');
                setIsAuthenticated(false);
            })
            .catch(function (error) {
                console.error('Logout failed', error);
            });
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, loginUser, registerUser, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};