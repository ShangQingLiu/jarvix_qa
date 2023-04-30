const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "", component: () => import("pages/IndexPage.vue") },
      {
        path: "/user-authentication-and-management",
        component: () => import("pages/UserAuthenticationAndManagement.vue"),
      },
      {
        path: "/file-management",
        component: () => import("pages/FileManagement.vue"),
      },
      {
        path: "/index-preparation",
        component: () => import("pages/IndexPreparation.vue"),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
