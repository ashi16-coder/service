import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8000" });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Normalize all API errors into a single readable message
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      (err.response?.status === 0 ? "Cannot connect to server. Is the backend running?" : null) ||
      err.message ||
      "Something went wrong. Please try again.";
    err.userMessage = message;
    return Promise.reject(err);
  }
);

export default api;
