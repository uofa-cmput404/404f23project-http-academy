import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import MakePost from './pages/MakePost';
import Navbar from '../src/components/Navbar';
import EditPost from './components/EditPost';
import Login from '../src/pages/Login';
import SignUp from '../src/pages/Signup';
import Profile from '../src/pages/profile';
import { AuthProvider, useAuth } from './context/AuthContext';
import './css/App.css';

const App = () => {

	return (
		<AuthProvider>
			<Router>
				<div className='app-container'>
					<Navbar />
					<br />
					<div className='app-content'>
						<Routes>
							<Route path="/" element={<Navigate replace to="/login" />} />
							<Route path="/home" element={<ProtectedRoute><Home /></ProtectedRoute>} />
							<Route path="/login" element={<GuestRoute><Login /></GuestRoute>} />
							<Route path="/signup" element={<GuestRoute><SignUp /></GuestRoute>} />
							<Route path="/post/create" element={<ProtectedRoute><MakePost /></ProtectedRoute>} />
							<Route path="/post/edit/:id" element={<ProtectedRoute><EditPost /></ProtectedRoute>} />
							<Route path="/post/:id" element={<ProtectedRoute><Detail /></ProtectedRoute>} />
							<Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />

						</Routes>
					</div>
				</div>
			</Router>
		</AuthProvider>
	);
};

//the reason i have this is that it will check if the user is already authenticated 
//or logged in, and if so it will take them away from guest routes like (logins/sign up)
//and to the home page were they can do whatever 
function GuestRoute({ children }) {
	const { isAuthenticated } = useAuth();
	return isAuthenticated ? <Navigate to="/home" /> : children;
}



// this will redirect u to the login screen if you're not yet authenticated.
function ProtectedRoute({ children }) {
	const { isAuthenticated } = useAuth();
	const location = useLocation();

	if (!isAuthenticated) {
		return <Navigate to="/login" state={{ from: location }} replace />;
	}

	return children;
}
export default App;
