import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import MakePost from './pages/MakePost';

import EditPost from './components/EditPost';

import Navbar from './components/Navbar';

const App = () => {
	return (
		<Router>
			<div>
				<Navbar />
				<br />
				<Routes>
					<Route path="/" element={<h1>Main Page</h1>} />
					<Route path="/home" element={<Home />} />
					<Route path="/post/create" element={<MakePost />} />
					<Route path="/post/edit/:id" element={<EditPost />} />
				</Routes>
			</div>
		</Router>
	);
}

export default App;