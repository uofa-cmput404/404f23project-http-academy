import axios from 'axios';


const baseURL = 'http://localhost:8000/';

// TODO: this is broken; CORS is not configured correctly, but using the default axios instance works
const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:8000',
        'Access-Control-Allow-Origin': 'http://localhost:3000/', // Remove this in prod as it's a security risk
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS', // this too
        accept: 'application/json',
    },
});

axiosInstance.interceptors.response.use(

    // if response is received, return it directly
    (response) => {
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        // Prevent infinite loops by preventing refresh token requests from being retried
        if (
            error.response.status === 401 &&
            originalRequest.url === baseURL + 'token/refresh/'
        ) {
            // navigate to login page
            window.location.href = '/login';
            return Promise.reject(error);
        }
    }
);

export default axiosInstance;