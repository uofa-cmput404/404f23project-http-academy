import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import MakePost from './pages/MakePost';
import Navbar from './components/Navbar';
import Detail from './pages/Detail'
import EditPost from './components/EditPost';

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
					<Route path="/post/:id" element={<Detail />} />
				</Routes>
			</div>
		</Router>
	);
}

export default App;
