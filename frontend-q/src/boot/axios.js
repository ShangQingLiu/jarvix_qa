import { boot } from "quasar/wrappers";
import axios from "axios";
import { ofetch } from 'ofetch';
import { useAuthStore } from "src/stores/auth";
// import { isUserLoggedIn } from "src/router/utils";

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const baseURL = import.meta.env.VITE_API_BASE_URL || window.env.API_BASE_URL;

if (baseURL == null) {
  throw new Error("VITE_API_BASE_URL is not defined");
}

const api = axios.create({ baseURL });
function isTokenExpired(userData) {
  if (userData) {
    const expiryTime = new Date(Date.now());
    const expiresAt = new Date(userData.exp * 1000);

    return expiresAt < expiryTime;
  }
  return true;
}



// ℹ️ Add request interceptor to send the authorization header on each subsequent request after login
api.interceptors.request.use(async (config) => {
  const store = useAuthStore();
  // const isLoggedIn = await isUserLoggedIn();
  // console.log("Is Loggged In", isLoggedIn);
  // Retrieve token from localStorage
  const user = JSON.parse(localStorage.getItem("jarvixUser"));
  // If token is found
  if (user) {
    config.headers = config.headers || {};
    if (
      config.url !== "auth/login" ||
      config.url !== "user-management/forgot_password"
    ) {
      config.headers.Authorization = user ? `${user.access_token}` : "";
    }
    if (isTokenExpired(user) && !store.refreshToken) {
      console.log("Refreshing Token");
      store.refreshToken = true
      await store.refreshToken();

    }
  }
  return config;
});

const apiFetch = ofetch.create({
  baseURL,
  async onRequest(context) {
    const store = useAuthStore();
    const user = JSON.parse(localStorage.getItem("jarvixUser"));
    // If token is found
    if (user) {
      context.options.headers = context.options.headers ?? {};
      if (
        context.request !== "auth/login" ||
        context.request !== "user-management/forgot_password"
      ) {
        context.options.headers.Authorization = user ? `${user.access_token}` : "";
      }
      if (isTokenExpired(user) && !store.refreshToken) {
        console.log("Refreshing Token");
        store.refreshToken = true
        await store.refreshToken();
      }
    }
  },
});

export default boot(({ app, store }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  app.config.globalProperties.$pinia = store;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api, apiFetch };
