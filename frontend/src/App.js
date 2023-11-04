import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import MakePost from './pages/MakePost';
import Navbar from './components/Navbar';
import Detail from './pages/Detail'
import EditPost from './components/EditPost';
import Login from '../src/pages/LoginForm'
import Profile from '../src/pages/profile'
import { AuthProvider } from './context/AuthContext';
import '../src/css/App.css'

const App = () => {
	return (
		<AuthProvider>
		<Router>
			<div className='app-container'>
				<Navbar />
				<br />
				<div className='app-content'>
				<Routes>
					<Route path="/" element={<h1>Main Page</h1>} />
					<Route path="/home" element={<Home />} />
					<Route path="/login" element={<Login />} />
					<Route path="/post/create" element={<MakePost />} />
					<Route path="/post/edit/:id" element={<EditPost />} />
					<Route path="/post/:id" element={<Detail />} />
					<Route path="/profile" element={<Profile />} />
				</Routes>
				</div>
				
			</div>
		</Router>
		</AuthProvider>
	);
}

export default App;
