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
        indexBtn: "Project Training",
        deleteBtn: "Delete Project",
        reIndexBtn: "Re-Training",
        ProjectUsers: {
          title: "Project Users",
          noFound: "No Users Found in Project",
          viewAll: "View All Users of Project",
          viewLess: " Show Less",
        },
      },
      Invite: {
        email: "Email",
        inviteBtn: "Send Invite",
        title: "Invite People",
        addField: "+ add another field",
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
            btn: "Back",
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
            dontAccountText: "New to Bauma?/No account yet?",
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
      noFound: "No Project Files. Please Upload Files Now and do the Training",
      indexBtn: "Re-Training",
      uploadNewFileTitle: "Upload New File",
      uploadBtn: "Upload",
      theseFiles: 'Upload these files:',
      dragFiles: 'Drag or Click to upload files',

    },
    IndexPreparation: {
      chatBtn: "Chat Room",
      validationForum: "Validation Forum",
      chooseProject: "Choose Project",
      chooseSession: "Choose Session",
      showExistingSession: " Show Existing Sessions",
      generateNewSession: "Generate New Session",
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
      ValidationForum: {
        hint1: "1. Each line specify one question and one expected answer",
        hint2: "2. The question and expected answer need to seperate by comma ",
        hint3: "3. Each line need to end by .",
        previewBtn: " Preview Question Document ",
        submitBtn: "Submit",
        uploadQuestionBtn: "Upload Questions Document",
        summaryScore: "Summary Score:",
        labels: {
          question: "Question",
          expect_answer: "Expected Answer",
          query_answer: "Query Answer",
          is_correct: "Correct(True/False)",
        },
      },
    },

  },
  MainLayout: {
    loginBtn: "Login",
    logoutBtn: "Logout",
    links: {
      UserAuthenticationAndManagement:
        "Users",
      Index: "Project Management",
      FileManagement: "File Management",
      Services: "Services",
    },
    languages: {
      english: "English",
      chineeseSimplified: "Chineese ( Simplified )",
      chineeseTraditional: "Chineese ( Traditional )",
    },
    roles: {
      user: "User",
      admin: "Admin",
    },
  },
  AuthLayout: {
    welcomeText: "Personalized Knowledge, Tailored Conversation, Secured Privacy",
  },
  Extra:{
    projectName: 'Project Name:',
    logout:'Logout',
    existingSession: 'Existing Sessions',
    createProject: 'Create Project',
    uploadFile: 'Upload Files',
    service: 'Service',
    chatPlaceholder: 'Type your question here...',
    fileTitle:"is exceeding the limit",
    fileCaption:"Maximum File limit is 20 MB",

  }
};
