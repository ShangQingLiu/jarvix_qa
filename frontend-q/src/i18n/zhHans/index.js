export default {
  pages: {
    IndexPage: {
      Index: {
        ProjectList: {
          title: "所有项目",
          noFound: "未找到项目",
          viewAll: "查看所有项目",
          viewLess: "显示更少",
        },
        CreateProject: {
          form: {
            projectName: "项目名称",
            description: "在此处输入项目描述...",
            btn: "创建项目",
          },
        },
        EditProject: {
          form: {
            projectName: "项目名称",
            description: "在此处输入项目描述...",
            btn: "更新项目",
          },
        },
      },
      Detail: {
        inviteBtn: "邀请人员",
        updateBtn: "更新项目",
        indexBtn: "项目训练",
        deleteBtn: "删除项目",
        reIndexBtn: "重新训练",
      },
      Invite: {
        email: "电子邮件",
        inviteBtn: "发送邀请",
        title: "邀请人员",
        addField: "+ 添加另一个字段",
      },
    },
    UserAuthenticationAndManagement: {
      DonePage: {
        Done: {
          title: "全部完成",
          subtitle: "您的密码已重置。",
          loginBtn: "登录",
        },
      },
      EditUserPage: {
        breadcrumbs: {
          label: "用户身份验证和用户管理",
          label2: "编辑用户",
        },
        EditUser: {
          title: "编辑用户",
          form: {
            username: "用户名",
            email: "电子邮件",
            password: "密码",
            btn: "编辑用户",
          },
        },
      },
      ForgotPasswordPage: {
        breadcrumbs: {
          label: "用户身份验证和用户管理",
          label2: "忘记密码",
        },
        ForgotPassword: {
          title: "忘记密码",
          form: {
            email: "电子邮件",
            btn: "返回登录",
            btn2: "发送代码",
          },
        },
      },
      IndexPage: {
        UsersList: {
          title: "所有用户",
          noFound: "未找到用户",
          viewAll: "查看所有用户",
          viewLess: "显示更少",
        },
      },
      LoginPage: {
        breadcrumbs: {
          label: "用户身份验证和用户管理",
          label2: "登录",
        },
        Login: {
          title: "登录",
          form: {
            username: "用户名",
            password: "密码",
            btn: "登录",
            dontAccountText: "还没有账号？",
            signupBtn: "注册",
            forgotPasswordBtn: "忘记密码",
            dontRememberText: "如果不记得密码",
          },
        },
      },
      NewPasswordPage: {
        breadcrumbs: {
          label: "用户身份验证和用户管理",
          label2: "设置新密码",
        },
        NewPassword: {
          title: "新密码",
          form: {
            password: "密码",
            confirmPassword: "确认密码",
            btn: "设置新密码",
          },
        },
      },
      OtpPage: {
        breadcrumbs: {
          label: "用户身份验证和用户管理",
          label2: "密码重置",
        },
        Otp: {
          title: "Otp代码",
          subtitle: "我们已将代码发送到",
          form: {
            btn: "继续",
            didntreceive: "没有收到代码",
            resendBtn: "点击重新发送",
          },
        },
      },
      RegisterPage: {
        breadcrumbs: {
          label: "用户认证和用户管理",
          label2: "注册",
        },
        Register: {
          title: "注册",
          form: {
            username: "用户名",
            email: "电子邮件",
            password: "密码",
            btn: "注册",
            alreadyBtn: "已经有一个账号?",
            loginBtn: "登录",
          },
        },
      },
      ViewUserPage: {
        title: "用户项目",
        noFound: "未找到用户项目",
      },
    },
    FileManagementPage: {
      title: "请选择一个项目",
      projectName: "选择项目",
      uploadFilesTitle: "已上传的文件",
      selectProjectTitle: "选择项目",
      noFound: "没有项目文件，请立即索引并上传文件",
      indexBtn: "重新训练",
      uploadNewFileTitle: "上传新文件",
      uploadBtn: "上传",
      theseFiles: '上传这些文件：',
      dragFiles: '拖拽或点击上传文件',
    },
    IndexPreparation: {
      chatBtn: "聊天室",
      validationForum: "验证论坛",
      chooseProject: "选择专案",
      chooseSession: "选择会话",
      showExistingSession: "显示现有会话",
      generateNewSession: "生成新会话",
      Question: {
        questions: {
          title: "新增问题",
          queryText: "在这里输入您的问题...",
          questionType: "问题类型",
          questionBtn: "新增问题",
          question: "问题",
        },
        answers: {
          title: "所有可能的答案",
          answer: "答案",
        },
      },
      ValidationForum: {
        hint1: "1. 每行指定一个问题和一个预期答案",
        hint2: "2. 问题和预期答案需要用逗号分隔",
        hint3: "3. 每行需要以句号结尾",
        previewBtn: "预览问题文件",
        submitBtn: "提交",
        uploadQuestionBtn: "上传问题文件",
        summaryScore: "总分:",
        labels: {
          question: "问题",
          expect_answer: "预期答案",
          query_answer: "查询答案",
          is_correct: "正确(True/False)",
        },
      },
    },
  },
  MainLayout: {
    loginBtn: "登录",
    logoutBtn: "退出登录",
    links: {
      UserAuthenticationAndManagement: "用户认证和管理",
      Index: "项目管理",
      FileManagement: "文件管理",
      Services: "服务",
    },
    languages: {
      english: "英文",
      chineeseSimplified: "简体中文",
      chineeseTraditional: "繁体中文",
    },
    roles: {
      user: "用户",
      admin: "管理员",
    },
  },
  AuthLayout: {
    welcomeText: "歡迎來到我們的網站，這將對您有所幫助。",
  },
  Extra:{
    projectName: '项目名称:',
    logout: '注销',
    existingSession: '现有会话',
    createProject: '创建项目',
    uploadFile: '上传文件',
    service: ' 服务',
    chatPlaceholder: '在此处输入您的问题...',
    fileTitle: '超过了限制',
    fileCaption: '最大文件限制为20MB',
  }
};
