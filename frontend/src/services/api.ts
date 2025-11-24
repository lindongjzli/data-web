import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

// Create an Axios instance
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // Your FastAPI backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the token in headers
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;
