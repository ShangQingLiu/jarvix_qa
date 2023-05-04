import { route } from "quasar/wrappers";
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import routes from "./routes";
import { isUserLoggedIn } from "./utils";
import { useProjectStore } from "src/stores/project";

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === "history"
    ? createWebHistory
    : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });
  Router.beforeEach(async (to, from, next) => {
    const isLoggedIn = await isUserLoggedIn();
    console.log(isLoggedIn);
    const store = useProjectStore();
    // If not loggedIn and also not going to login page redirect user to login page
    if (to.meta.requiresAuth && !isLoggedIn) next({ name: "login" });
    if (to.name === "services" && !store.selectedProject)
      next({ name: "fileManagement" });
    // If loggedIn and also going to login page redirect user to home page
    // else if (!to.meta.requiresAuth && isLoggedIn)
    //   next({ name: "UsersManagementPage" });
    else next();
  });

  return Router;
});
