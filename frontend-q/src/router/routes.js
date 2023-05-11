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
          },
          {
            path: "/:id",
            component: () => import("pages/IndexPage/Detail.vue"),
          },
          {
            path: "/edit/:id",
            component: () =>
              import("components/IndexPage/Index/EditProject.vue"),
          },
          {
            path: "/invite/:id",
            component: () => import("pages/IndexPage/Invite.vue"),
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
          },
          {
            path: "login",
            component: () =>
              import("pages/UserAuthenticationAndManagement/LoginPage.vue"),
          },
          {
            path: "register",
            component: () =>
              import("pages/UserAuthenticationAndManagement/RegisterPage.vue"),
          },
          {
            path: "forgot-password",
            component: () =>
              import(
                "pages/UserAuthenticationAndManagement/ForgotPasswordPage.vue"
              ),
          },
          {
            path: "otp-code",
            component: () =>
              import("pages/UserAuthenticationAndManagement/OtpPage.vue"),
          },
          {
            path: "new-password",
            component: () =>
              import(
                "pages/UserAuthenticationAndManagement/NewPasswordPage.vue"
              ),
          },
          {
            path: "done",
            component: () =>
              import("pages/UserAuthenticationAndManagement/DonePage.vue"),
          },
          {
            path: "edit/:id",
            component: () =>
              import("pages/UserAuthenticationAndManagement/EditUserPage.vue"),
          },
          {
            path: "view/:id",
            component: () =>
              import("pages/UserAuthenticationAndManagement/ViewUserPage.vue"),
          },
        ],
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
