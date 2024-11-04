import axios from "axios";
import { ACCESS_TOKEN } from "./constants";
import { jwtDecode } from "jwt-decode";
import { refreshToken } from "./components/OktaAuthServices";

const apiUrl = "/choreo-apis/mulecentral/backend/v1";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl
});

api.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    
    const decoded = jwtDecode(token);
    const tokenExpiration = decoded.exp;
    const now = Date.now() / 1000;

    if (tokenExpiration < now) {
      console.log('Trying to fetch a new token...');
      const auth = await refreshToken();
      localStorage.setItem(ACCESS_TOKEN, auth);
      config.headers.Authorization = `Bearer ${auth}`;
    } else {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;