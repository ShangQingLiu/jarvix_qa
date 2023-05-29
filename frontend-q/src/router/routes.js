const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        component: () => import("pages/IndexPage.vue"),
        children: [
          {
            path: "",
            component: () => import("pages/IndexPage/Index.vue"),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
          },
          {
            path: "/:id",
            component: () => import("pages/IndexPage/Detail.vue"),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
          },
          {
            path: "/edit/:id",
            component: () =>
              import("components/IndexPage/Index/EditProject.vue"),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
          },
          {
            path: "/invite/:id",
            component: () => import("pages/IndexPage/Invite.vue"),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
          },
        ],
      },
      {
        path: "user-authentication-and-management",
        component: () => import("pages/UserAuthenticationAndManagement.vue"),
        children: [
          {
            path: "",
            component: () =>
              import("pages/UserAuthenticationAndManagement/IndexPage.vue"),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
            name: "UsersManagementPage",
          },

          {
            path: "otp-code",
            component: () =>
              import("pages/UserAuthenticationAndManagement/OtpPage.vue"),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
          },
          {
            path: "new-password",
            component: () =>
              import(
                "pages/UserAuthenticationAndManagement/NewPasswordPage.vue"
              ),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
          },
          {
            path: "done",
            component: () =>
              import("pages/UserAuthenticationAndManagement/DonePage.vue"),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
          },
          {
            path: "edit/:id",
            component: () =>
              import("pages/UserAuthenticationAndManagement/EditUserPage.vue"),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
          },
          {
            path: "view/:id",
            component: () =>
              import("pages/UserAuthenticationAndManagement/ViewUserPage.vue"),
            // only authenticated users can create posts
            meta: { requiresAuth: true },
          },
        ],
      },
      {
        path: "/file-management",
        component: () => import("pages/FileManagement.vue"),
        // only authenticated users can create posts
        meta: { requiresAuth: true },
        name: "fileManagement",
      },
      {
        path: "/index-preparation",
        component: () => import("pages/IndexPreparation.vue"),
        // only authenticated users can create posts
        meta: { requiresAuth: true },
        name: "services",
      },
    ],
  },
  {
    path: "/auth",
    component: () => import("layouts/AuthLayout.vue"),
    children: [
      {
        path: "login",
        component: () =>
          import("pages/UserAuthenticationAndManagement/LoginPage.vue"),
        // only authenticated users can create posts
        meta: { requiresAuth: false },
        name: "login",
      },
      {
        path: "register",
        component: () =>
          import("pages/UserAuthenticationAndManagement/RegisterPage.vue"),
        // only authenticated users can create posts
        meta: { requiresAuth: false },
      },
      {
        path: "forgot-password",
        component: () =>
          import(
            "pages/UserAuthenticationAndManagement/ForgotPasswordPage.vue"
          ),
        // only authenticated users can create posts
        meta: { requiresAuth: false },
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
