
import React, { useState } from 'react';
import { useNavigate} from 'react-router-dom'; 
import { useAuth } from '../context/AuthContext';
import '../css/SignUp.css'
import logoImage from '../assets/images/logo.png';

const SignUp = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [github, setGithub] = useState('')
    const [profileImage, setProfileImage] = useState('')
    const { registerUser } = useAuth();
    
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!email || !password) {
            setError('Please fill in all fields.');
            return;
        }
        try {
            await registerUser(email, username, password, github, profileImage, () => navigate('/home'));
        } catch (error) {
            console.error('Registration failed', error);
            setError('Registration failed. Please try again.');
        }
    };

    const redirect = () =>{
        navigate('/login')
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
                <h2>Sign up</h2>
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
                            type="text" 
                            placeholder="Enter username" 
                            value={username} 
                            class="single-line-input" 
                            onChange={e => setUsername(e.target.value)} 
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
                        <div>
                        <input 
                            type="text" 
                            placeholder="GitHub URL" 
                            value={github} 
                            onChange={e => setGithub(e.target.value)}
                            className="single-line-input" 
                        />
                    
                        </div>
                        <div>
                        <input 
                            type="text" 
                            placeholder="Profile Image URL" 
                            value={profileImage} 
                            onChange={e => setProfileImage(e.target.value)}
                            className="single-line-input" 
                        />
                        </div>
                        <button type="submit" className = "button-design">Sign up</button>
                        {error && <p className="error-message">{error}</p>}
                        
                        
                        
                        
                    </form>
                </div>
            </div>
            <div className='Login-redirect'>
                <div>
                    <h1>Welcome</h1>
                    <h3>Have an account?</h3>
                    <h4>Join us by logging in and you can sell us ur data !!</h4>
                </div>
                <button className = "button-design" onClick= {redirect}>Log in</button>
            </div>
        </div>

       
         </div>
    );
};

export default SignUp;
