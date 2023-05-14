export default {
  pages: {
    IndexPage: {
      Index: {
        ProjectList: {
          title: "All Projects",
          noFound: "No Projects Found",
          viewAll: "View All Projects",
          viewLess: " Show Less",
        },
        CreateProject: {
          form: {
            projectName: "Project Name",
            description: "Type project description here...",
            btn: "Create Project",
          },
        },
        EditProject: {
          form: {
            projectName: "Project Name",
            description: "Type project description here...",
            btn: "Update Project",
          },
        },
      },
      Detail: {
        inviteBtn: "Invite people",
        updateBtn: "Update Project",
        indexBtn: "Index Project",
        deleteBtn: "Delete Project",
        reIndexBtn: "Re-Index",
      },
      Invite: {
        email: "Email",
        inviteBtn: "Invite",
        title: 'Invite People'
      },
    },
    UserAuthenticationAndManagement: {
      DonePage: {
        Done: {
          title: "All done",
          subtitle: "Your password has been reset.",
          loginBtn: "Login",
        },
      },
      EditUserPage: {
        breadcrumbs: {
          label: "User Authentication and User Management",
          label2: "Edit User",
        },
        EditUser: {
          title: "Edit User",
          form: {
            username: "User name",
            email: "Email",
            password: "Password",
            btn: "Edit User",
          },
        },
      },
      ForgotPasswordPage: {
        breadcrumbs: {
          label: "User Authentication and User Management",
          label2: "Forget Password",
        },
        ForgotPassword: {
          title: "Forgot Password",
          form: {
            email: "Email",
            btn: "Go back to login",
            btn2: "Send code",
          },
        },
      },
      IndexPage: {
        UsersList: {
          title: "All Users",
          noFound: "No Users Found",
          viewAll: "View All Users",
          viewLess: "Show Less",
        },
      },
      LoginPage: {
        breadcrumbs: {
          label: "User Authentication and User Management",
          label2: "Login",
        },
        Login: {
          title: "Login",
          form: {
            username: "User name",
            password: "Password",
            btn: "Login",
            dontAccountText: "Don’t have a account?",
            signupBtn: "Sign Up",
            forgotPasswordBtn: "Forget Password",
            dontRememberText: "If don’t remember password",
          },
        },
      },
      NewPasswordPage: {
        breadcrumbs: {
          label: "User Authentication and User Management",
          label2: "Set new pasword",
        },
        NewPassword: {
          title: "New Password",
          form: {
            password: "Password",
            confirmPassword: "Confirm Password",
            btn: "Set New Password",
          },
        },
      },
      OtpPage: {
        breadcrumbs: {
          label: "User Authentication and User Management",
          label2: "Password Reset",
        },
        Otp: {
          title: "Otp Code",
          subtitle: "We have sent the code to",
          form: {
            btn: "Continue",
            didntreceive: "Didn’t receive the code",
            resendBtn: "click to resend",
          },
        },
      },
      RegisterPage: {
        breadcrumbs: {
          label: "User Authentication and User Management",
          label2: "Sign Up",
        },
        Register: {
          title: "Register",
          form: {
            username: "User name",
            email: "Email",
            password: "Password",
            btn: "Sign Up",
            alreadyBtn: "Already have an account?",
            loginBtn: "Login",
          },
        },
      },
      ViewUserPage: {
        title: "User Projects",
        noFound: "No User Projects Found",
      },
    },
    FileManagementPage: {
      title: "Please select a project",
      projectName: "Choose Project",
      uploadFilesTitle: "Uploaded Files",
      selectProjectTitle: "Select Project",
      noFound: "No Project Files. Please Index and Upload Files Now",
      indexBtn: "Re-Index",
      uploadNewFileTitle: "Upload New File",
      uploadBtn: "Upload",
    },
    IndexPreparation: {
      chatBtn: "Chat Room",
      validationForum: "Validation Forum",
      chooseProject: "Choose Project",
      chooseSession: "Choose Session",
      showExistingSession: " Show Existing Sessions",
      Question: {
        questions: {
          title: "Add New Question",
          queryText: "Type your question here...",
          questionType: "Question Type",
          questionBtn: "Add Question",
          question: "Question",
        },
        answers: {
          title: "All Possible Answers",
          answer: "Answer",
        },
      },
    },
  },
  MainLayout: {
    loginBtn: "Login",
    logoutBtn: "Logout",
    links:{
      UserAuthenticationAndManagement: 'User Authentication and User Management',
      Index: 'Project Management',
      FileManagement: 'File Management',
      Services: 'Services'
    }
  },
};
