import React, { useState } from 'react';

function SignupAndLogin() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSignup = () => {
        // TODO: Implement signup logic
        if (email === '') {
            alert('Please enter an email address');
            return;
        }
        if (password === '') {
            alert('Please enter a password');
            return;
        }
        fetch('http://localhost:5000/api/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('Success:', data);
                alert('Signup successful');
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Signup failed');
            });
    };

    const handleLogin = () => {
        // TODO: Implement login logic
        if (email === '') {
            alert('Please enter an email address');
            return;
        }
        if (password === '') {
            alert('Please enter a password');
            return;
        }
        fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('Success:', data);
                alert('Login successful');
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Login failed');
            });
    };

    return (
        <div>
            <h1>Signup and Login</h1>
            <form>
                <label>
                    Email:
                    <input type="email" value={email} onChange={handleEmailChange} />
                </label>
                <br />
                <label>
                    Password:
                    <input type="password" value={password} onChange={handlePasswordChange} />
                </label>
                <br />
                <button type="button" onClick={handleSignup}>Signup</button>
                <button type="button" onClick={handleLogin}>Login</button>
            </form>
        </div>
    );
}

export default SignupAndLogin;
