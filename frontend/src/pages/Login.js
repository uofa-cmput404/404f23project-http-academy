import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import { useAuth } from '../context/AuthContext';
import '../css/Logsin.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { loginUser } = useAuth();
   

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!email || !password) {
            setError('Please fill in all fields.');
            return;
        }
        
        try {
            await loginUser(email, password, () => navigate('/home'));
            // Redirect the user to the homepage with posts 
        } catch (error) {
            console.error('Failed to log in', error);
            setError('Failed to log in. Please check your email and password.');
        }
    };

    return (
        <div className="formContainer">
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Email address</label>
                    <input 
                        type="email" 
                        placeholder="Enter email" 
                        value={email} 
                        onChange={e => setEmail(e.target.value)} 
                    />
                </div>
                <div>
                    <label>Password</label>
                    <input 
                        type="password" 
                        placeholder="Password" 
                        value={password} 
                        onChange={e => setPassword(e.target.value)} 
                    />
                </div>
                <button type="submit">Log In</button>
                {error && <p className="error-message">{error}</p>}
                <p>Don't have an account? <Link to="/signup">Sign up</Link></p>
            </form>
        </div>
    );
};

export default Login;
