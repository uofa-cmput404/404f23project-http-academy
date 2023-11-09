import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; 
import { useAuth } from '../context/AuthContext';
import '../css/Logsin.css';
import logoImage from '../assets/images/logo.png';

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

    const redirect = () =>{
        navigate('/signup')
    }

    return (
        <div className="outer-container">
        <div className="logos">
            <img src={logoImage} alt="SDIST Logo" className="logo-image" />
            <h2>SDIST</h2>
        </div>
        <div className='header-content'>
            <h1>Welcome Back</h1>
            <h3>We’ve missed you! Ready to sell more of your data!</h3>
        </div>
        <div className='outer-login-signup-container'>
            <div className='login-form'>
                <h2>Login</h2>
                <div classname="form-container">
                    <form onSubmit={handleSubmit}>
                        <div>
                           
                            <input 
                                type="email" 
                                placeholder="Email" 
                                value={email} 
                                onChange={e => setEmail(e.target.value)} 
                                class="single-line-input" 
                            />
                        </div>
                        <div>
                            
                            <input 
                                type="password" 
                                placeholder="Password" 
                                value={password} 
                                onChange={e => setPassword(e.target.value)} 
                                class="single-line-input" 
                            />
                        </div>
                        <button type="submit" className = "button-design">Log In</button>
                        {error && <p classname="error-message">{error}</p>}
                        
                        
                        
                        
                    </form>
                </div>
            </div>
            <div className='signup-redirect'>
                <div>
                    <h1>Welcome</h1>
                    <h3>Don’t have an account?</h3>
                    <h4>Join us by signing up and you can sell us ur data !!</h4>
                </div>
                <button className = "button-design" onClick= {redirect}>Sign up</button>
            </div>
        </div>

       
         </div>
    );
};

export default Login;
