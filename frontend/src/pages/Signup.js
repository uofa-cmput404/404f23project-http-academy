
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom'; 
import { useAuth } from '../context/AuthContext';
import '../css/SignUp.css'
const SignUp = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { registerUser } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!email || !password) {
            setError('Please fill in all fields.');
            return;
        }
        try {
            await registerUser(email, username, password, () => navigate('/home'));
        } catch (error) {
            console.error('Registration failed', error);
            setError('Registration failed. Please try again.');
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
                    <label>Username</label>
                    <input 
                        type="text" 
                        placeholder="Enter username" 
                        value={username} 
                        onChange={e => setUsername(e.target.value)} 
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
                {error && <p className="error-message">{error}</p>}
                <p>Have an account? <Link to="/login">Login</Link></p>
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default SignUp;
