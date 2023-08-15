export default {
  pages: {
    IndexPage: {
      Index: {
        ProjectList: {
          title: "所有專案",
          noFound: "沒有專案",
          viewAll: "查看所有專案",
          viewLess: "顯示較少",
        },
        CreateProject: {
          form: {
            projectName: "專案名稱",
            description: "在此輸入專案描述...",
            btn: "創建專案",
          },
        },
        EditProject: {
          form: {
            projectName: "專案名稱",
            description: "在此輸入專案描述...",
            btn: "更新專案",
          },
        },
      },
      Detail: {
        inviteBtn: "邀請成員",
        updateBtn: "更新專案",
        indexBtn: "專案訓練",
        deleteBtn: "刪除專案",
        reIndexBtn: "重新訓練",
      },
      Invite: {
        email: "電子郵件",
        inviteBtn: "發送邀請",
        title: "邀請人",
        addField: "+ 添加另一個領域",
      },
    },
    UserAuthenticationAndManagement: {
      DonePage: {
        Done: {
          title: "完成",
          subtitle: "你的密码已重置。",
          loginBtn: "登錄",
        },
      },
      EditUserPage: {
        breadcrumbs: {
          label: "用戶驗證和用戶管理",
          label2: "編輯用戶",
        },
        EditUser: {
          title: "編輯用戶",
          form: {
            username: "用戶名",
            email: "電郵地址",
            password: "密碼",
            btn: "編輯用戶",
          },
        },
      },
      ForgotPasswordPage: {
        breadcrumbs: {
          label: "用戶驗證和用戶管理",
          label2: "忘記密碼",
        },
        ForgotPassword: {
          title: "忘記密碼",
          form: {
            email: "電郵地址",
            btn: "返回登錄",
            btn2: "發送驗證碼",
          },
        },
      },
      IndexPage: {
        UsersList: {
          title: "所有用戶",
          noFound: "未找到用戶",
          viewAll: "查看所有用戶",
          viewLess: "顯示較少",
        },
      },
      LoginPage: {
        breadcrumbs: {
          label: "用戶驗證和用戶管理",
          label2: "登錄",
        },
        Login: {
          title: "登錄",
          form: {
            username: "用戶名",
            password: "密碼",
            btn: "登錄",
            dontAccountText: "還沒有帳戶？",
            signupBtn: "註冊",
            forgotPasswordBtn: "忘記密碼",
            dontRememberText: "如果忘記密碼",
          },
        },
      },
      NewPasswordPage: {
        breadcrumbs: {
          label: "用戶驗證和用戶管理",
          label2: "設置新密碼",
        },
        NewPassword: {
          title: "新密碼",
          form: {
            password: "密碼",
            confirmPassword: "確認密碼",
            btn: "設置新密碼",
          },
        },
      },
      OtpPage: {
        breadcrumbs: {
          label: "用戶驗證和用戶管理",
          label2: "重置密碼",
        },
        Otp: {
          title: "驗證碼",
          subtitle: "我們已將驗證碼發送至",
          form: {
            btn: "繼續",
            didntreceive: "未收到驗證碼",
            resendBtn: "點擊重新發送",
          },
        },
      },
      RegisterPage: {
        breadcrumbs: {
          label: "用戶認證和用戶管理",
          label2: "註冊",
        },
        Register: {
          title: "註冊",
          form: {
            username: "用戶名稱",
            email: "電子郵件",
            password: "密碼",
            btn: "註冊",
            alreadyBtn: "已經有帳戶？",
            loginBtn: "登入",
          },
        },
      },
      ViewUserPage: {
        title: "用戶專案",
        noFound: "找不到用戶專案",
      },
    },
    FileManagementPage: {
      title: "請選擇專案",
      projectName: "選擇專案",
      uploadFilesTitle: "上傳的檔案",
      selectProjectTitle: "選擇專案",
      noFound: "沒有專案檔案。請現在索引並上傳檔案",
      indexBtn: "重新訓練",
      uploadNewFileTitle: "上傳新檔案",
      uploadBtn: "上傳",
      theseFiles: '上傳這些檔案：',
dragFiles: '拖曳或點擊以上傳檔案'
    },
    IndexPreparation: {
      chatBtn: "聊天室",
      validationForum: "驗證論壇",
      chooseProject: "選擇專案",
      chooseSession: "選擇會話",
      showExistingSession: "顯示現有會話",
      generateNewSession: "生成新會話",
      Question: {
        questions: {
          title: "新增問題",
          queryText: "在此輸入您的問題...",
          questionType: "問題類型",
          questionBtn: "新增問題",
          question: "問題",
        },
        answers: {
          title: "所有可能的答案",
          answer: "答案",
        },
      },
      ValidationForum: {
        hint1: "1. 每行指定一個問題和一個預期答案",
        hint2: "2. 問題和預期答案需要用逗號分隔",
        hint3: "3. 每行需要以句號結尾",
        previewBtn: "預覽問題文件",
        submitBtn: "提交",
        uploadQuestionBtn: "上傳問題文件",
        summaryScore: "總分:",
        labels: {
          question: "問題",
          expect_answer: "預期答案",
          query_answer: "查詢答案",
          is_correct: "正確（是/否）",
        },
      },
    },
  },
  MainLayout: {
    loginBtn: "登入",
    logoutBtn: "登出",
    links:{
      UserAuthenticationAndManagement: '使用者驗證與管理',
      Index: '專案管理',
      FileManagement: '檔案管理',
      Services: '服務'
    },
    languages: {
      english: "英文",
      chineeseSimplified: "中文（简体）",
      chineeseTraditional: "中文（繁體）",
    },
    roles: {
      user: '使用者',
      admin: '管理員'
    }
  },
  AuthLayout: {
    welcomeText: "欢迎访问我们的网站，将为您提供帮助。",
    },
};
