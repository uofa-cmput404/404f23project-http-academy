import React, { useState, useEffect } from 'react';
import axiosInstance from '../axiosInstance';
import '../css/login.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useAuth } from '../context/AuthContext';

const LoginForm = () => {
    const [currentUser, setCurrentUser] = useState();
    const [registrationToggle, setRegistrationToggle] = useState(false);
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { isAuthenticated, setIsAuthenticated } = useAuth();
  

    useEffect(() => {
    
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            setCurrentUser(true);
            setIsAuthenticated(true);
        } else {
            setCurrentUser(false);
            setIsAuthenticated(false);
        }
    }, []);

    useEffect(() => {
        axiosInstance.get("/authors/user")
      .then(function(res) {
        setCurrentUser(true);
        setIsAuthenticated(true);
      })
      .catch(function(error) {
        setCurrentUser(false);
        setIsAuthenticated(false);
      });
    }, []);


  
    function update_form_btn() {
      if (registrationToggle) {
        document.getElementById("form_btn").innerHTML = "Register";
        setRegistrationToggle(false);
      } else {
        document.getElementById("form_btn").innerHTML = "Log in";
        setRegistrationToggle(true);
      }
    }
  
    function submitRegistration(e) {
      e.preventDefault();
      axiosInstance.post(
        "/authors/register",
        {
          email: email,
          username: username,
          password: password
        }
      ).then(function(res) {
        axiosInstance.post(
          "/authors/login",
          {
            email: email,
            password: password
          }
        ).then(function(res) {
            localStorage.setItem('user', JSON.stringify(res.data));
          setCurrentUser(true);
        });
      });
    }
  
    function submitLogin(e) {
      e.preventDefault();
      axiosInstance.post(
        "/authors/login",
        {
          email: email,
          password: password
        }
      ).then(function(res) {
        localStorage.setItem('user', JSON.stringify(res.data));
        setCurrentUser(true);
        console.log('User ID:', res.data.user_id);
      });
    }
  
    function submitLogout(e) {
      e.preventDefault();
      axiosInstance.post(
        "/authors/logout",
        {withCredentials: true}
      ).then(function(res) {
        localStorage.removeItem('user');
        setCurrentUser(false);
      });
    }
  
    if (currentUser) {
        return (
          <div className="formContainer">
            <form onSubmit={e => submitLogout(e)}>
              <Button type="submit" variant="light">Log out</Button>
            </form>
            <h2>You're logged in!</h2>
          </div>
        );
      }
      return (
        <div className="formContainer">
          <Button id="form_btn" onClick={update_form_btn} variant="light">{registrationToggle ? "Log in" : "Register"}</Button>
          {
        registrationToggle ? (
          <div className="center">
            <Form onSubmit={e => submitRegistration(e)}>
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
                <Form.Text className="text-muted">
                  We'll never share your email with anyone else.
                </Form.Text>
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicUsername">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
              </Form.Group>
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form>
          </div>        
        ) : (
          <div className="center">
            <Form onSubmit={e => submitLogin(e)}>
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
                <Form.Text className="text-muted">
                  We'll never share your email with anyone else.
                </Form.Text>
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
              </Form.Group>
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form>
          </div>
        )
      }
      </div>
    );
}

export default LoginForm;
