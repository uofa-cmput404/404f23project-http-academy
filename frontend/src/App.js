import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import MakePost from './pages/MakePost';

const App = () => {
	return (
		<Router>
			<div> 
				<nav>
					<ul>
						<li><a href="/">Main Page</a></li>
						<li><a href="/home">Home</a></li>
					</ul>
				</nav>
				<Routes>
					<Route path="/" element={<h1>Main Page</h1>} />
					<Route path="/home" element={<Home />} />
					<Route path="/post/create" element={<MakePost />} />
				</Routes>
			</div>
		</Router>
	);
}

export default App;
