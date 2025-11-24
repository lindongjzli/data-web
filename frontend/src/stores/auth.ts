import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import apiClient from '@/services/api';
import router from '@/router';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '');
  const user = ref(null); // You can enhance this to store user details

  const isAuthenticated = computed(() => !!token.value);

  function setToken(newToken: string) {
    token.value = newToken;
    localStorage.setItem('token', newToken);
  }

  function clearAuth() {
    token.value = '';
    user.value = null;
    localStorage.removeItem('token');
  }

  async function login(loginData: URLSearchParams) {
    try {
      const response = await apiClient.post('/auth/login', loginData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      const { access_token } = response.data;
      setToken(access_token);
      // Navigate to the dataset page after successful login
      await router.push('/dataset');
    } catch (error) {
      console.error('Login failed:', error);
      // You should probably show an error message to the user
      throw error;
    }
  }

  async function register(registerData: any) {
    try {
      await apiClient.post('/auth/register', registerData);
      // Navigate to the login page after successful registration
      await router.push('/login');
    } catch (error) {
      console.error('Registration failed:', error);
      throw error;
    }
  }

  function logout() {
    clearAuth();
    router.push('/login');
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
  };
});
