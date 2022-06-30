# 1. 前后端分离对比

# 2. 准备工作

- 1. 安装nodejs
[NodeJS官网](https://nodejs.org/en/download/)

- 2. 安装Vue
  ```bash
  npm install -g vue
  ```
[Vue主页](https://cn.vuejs.org/v2/guide/index.html)

- 3. 安装vue-cli
[vue-cli介绍](https://cli.vuejs.org/zh/guide/)

  ```bash
  npm install -g @vue/cli
  ```

 # 3. Vue-cli搭建项目

  - 1. 创建项目
  ```bash
  vue create vue-demo
  ```
  - Error 1
    ```bash
    ‘vue‘ 不是内部或外部命令，也不是可运行的程序 或批处理文件
    ```
    [解决方案](https://blog.csdn.net/m0_62404884/article/details/120905036)

  - Error 2
    ```bash
    You are using Node v10.12.0, but this version of @vue/cli requires Node ^12.0.0 || >= 14.0.0.
    Please upgrade your Node version.
    ```
     解决方案:升级版本

  - 2. 用空格选择所需模块
  ```bash
  <!--手动选择相关配置-->
  ? Please pick a preset: Manually select features
  <!--选择项目所需模块-->
  ? Check the features needed for your project: Babel, Router, Vuex, CSS Pre-processors, Linter
    <!--选择Vue.js版本-->
  ? Choose a version of Vue.js that you want to start the project with 2.x
  ? Use history mode for router? (Requires proper server setup for index fallback in production) Yes
  <!--选择CSS预处理器-->
  ? Pick a CSS pre-processor (PostCSS, Autoprefixer and CSS Modules are supported by default): Sass/SCSS (with
  dart-sass)
  <!--Eslint配置-->
  ? Pick a linter / formatter config: Prettier
  <!--保存时检测-->
  ? Pick additional lint features: Lint on save
  <!--配置文件-单独配置文件-->
  ? Where do you prefer placing config for Babel, ESLint, etc.? In dedicated config files
  ? Save this as a preset for future projects? Yes
  ? Save preset as: vue-demo
  🎉  Preset vue-demo saved in C:\Users\w50010425\.vuerc
  ```
  - 3.运行项目
  ```bash
  cd vue-demo
  npm run serve
  ```
  
# 4. 工程目录说明
```bash
|-- node_modules         // 项目依赖模块
|-- public               // 静态资源，不会被webpack编译，绝对路径
|
|-- dist                 // 项目打包文件
|
|-- src                  // 源码目录
|   |-- assets          // 项目公共资源
|   |-- components      // 组件库
|   |-- views           // 项目页面模块
|   |-- router          // 路由文件
|   |-- store           // vuex的状态管理
|   |-- style           // 各种样式文件
|   |-- App.vue         // 页面入口文件
|   |-- main.js         // 程序入口文件，加载各种公共组件
|
|-- .babelrc            // ES6语法编译配置
|-- .editorconfig      // 代码编写规格
|-- .gitignore         // 忽略的文件
|-- favicon.ico        // 页面左上角小图标
|-- index.html          // 入口html文件
|-- package.json        // 项目及工具的依赖配置文件
|-- README.md           // 说明
```

# 5. Vue+Element 使用

## 5.1 安装Element

```bash
  npm i element-ui -S
```

## 5.2 在main.js中引入
```bash
  import ElementUI from 'element-ui';
  import 'element-ui/lib/theme-chalk/index.css';
  Vue.use(ElementUI);
```

# 6. 前后端交互

## 6.1 axios
    axios 是一个基于 Promise 的 HTTP 库，可以用在浏览器和 node.js 中。axios是通过Promise实现对Ajax技术的一种封装，就像jquery对Ajax的封装一样，简单来说就是Ajax技术实现了局部数据的刷新，axios实现了对Ajax的封装

### 6.1.1 Axios特性
  - 1. 可以在浏览器中发送 XMLHttpRequests
  - 2. 可以在 node.js 发送 http 请求
  - 3. 支持 Promise API
  - 4. 拦截请求和响应
  - 5. 转换请求数据和响应数据
  - 6. 能够取消请求
  - 7. 自动转换 JSON 数据
  - 8. 客户端支持保护安全免受 XSRF 攻击
## 6.2 基本使用
# 7. Error
- 解决eslint与prettier同时使用时校验冲突问题
  ```bash
  19:15  error  Replace `⏎······:data="tableData"·⏎······style="width:·100%">⏎` with `:data="tableData"·style="width:·100%">`                          prettier/prettier
  ```
  参考如下链接：[vscode 中 prettier 和 ESLint 冲突解决](https://blog.csdn.net/u011705725/article/details/117036377?spm=1001.2101.3001.6650.4&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-4-117036377-blog-124181920.pc_relevant_multi_platform_whitelistv1&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-4-117036377-blog-124181920.pc_relevant_multi_platform_whitelistv1)
