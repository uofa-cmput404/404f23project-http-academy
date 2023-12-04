import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const baseURL = 'https://cmput404-httpacademy5-2f1f7827d5c1.herokuapp.com/';

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