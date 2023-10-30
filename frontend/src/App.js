import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import MakePost from './pages/MakePost';
import Navbar from './components/Navbar';
import Detail from './pages/Detail'
import EditPost from './components/EditPost';
import Login from '../src/pages/LoginForm'
import { AuthProvider } from './context/AuthContext';

const App = () => {
	return (
		<AuthProvider>
		<Router>
			<div>
				<Navbar />
				<br />
				<Routes>
					<Route path="/" element={<h1>Main Page</h1>} />
					<Route path="/home" element={<Home />} />
					<Route path="/login" element={<Login />} />
					<Route path="/post/create" element={<MakePost />} />
					<Route path="/post/edit/:id" element={<EditPost />} />
					<Route path="/post/:id" element={<Detail />} />
				</Routes>
			</div>
		</Router>
		</AuthProvider>
	);
}

export default App;
