import axios from 'axios';


const baseURL = 'http://localhost:8000/';

// TODO: this is broken; CORS is not configured correctly, but using the default axios instance works
const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        accept: 'application/json',
    },
});

export default axiosInstance;