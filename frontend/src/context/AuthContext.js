// AuthContext.js

import React, { createContext, useState, useContext } from 'react';
import axiosInstance from '../axiosInstance';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);


    const logout = () => {
        axiosInstance.post("/authors/logout", { withCredentials: true })
            .then(function(res) {
                localStorage.removeItem('user');
                setIsAuthenticated(false);
            })
            .catch(function(error) {
                console.error('Logout failed', error);
            });
    };
    return (
        <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};
