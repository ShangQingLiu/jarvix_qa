import { boot } from "quasar/wrappers";
import axios from "axios";
import { useAuthStore } from "src/stores/auth";
// import { isUserLoggedIn } from "src/router/utils";

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: "https://api.bauma.sis.ai/api/" });
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

export { api };
