# 1. 前后端分离对比

# 2. 准备工作

- 安装nodejs  [NodeJS官网](https://nodejs.org/en/download/)

- 安装Vue  [Vue主页](https://cn.vuejs.org/v2/guide/index.html)
  ```bash
  npm install -g vue
  ```  

- 安装vue-cli  [vue-cli介绍](https://cli.vuejs.org/zh/guide/)

  ```bash
  npm install -g @vue/cli
  ```

# 3. Vue-cli搭建项目

- 创建项目
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

- 用空格选择所需模块
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
- 运行项目
  ```bash
    cd vue-demo
    npm run serve
  ```
  
# 4. 工程目录说明
  ```BASH
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

### 6.2.1 安装axios
```bash
npm i axios --save
```

### 6.2.2 在main.js中引入

```js
import axios from "axios"

Vue.prototype.$http = axios;
```

### 6.2.3 基本使用 - .vue文件下method方法中

```js
 methods: {
    getdata() {
      this.$axios.get("/queryCityInfo").then((res) => {
        alert("请求成功,response = " + res.data);
        this.cityInfoList = res.data;
        console.log(this.cityInfoList);
      });
    },
    handleEdit() {},
    handleSizeChange() {},
    handleCurrentChange() {},
  },
};
```

### 6.2.4 在vue.config.js中配置代理，解决跨域问题
```js
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/ota": {
        target: "http://localhost:8088",
        changeOrigin: true,
        pathRewrite: {
          "^/api": "",
        },
      },
    },
  },
});
```
# 7. Error
## 7.1 解决eslint与prettier同时使用时校验冲突问题
  ```bash
  19:15  error  Replace `⏎······:data="tableData"·⏎······style="width:·100%">⏎` with `:data="tableData"·style="width:·100%">`                          prettier/prettier
  ```
  参考如下链接：
  - [vscode 中 prettier 和 ESLint 冲突解决](https://blog.csdn.net/u011705725/article/details/117036377?spm=1001.2101.3001.6650.4&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-4-117036377-blog-124181920.pc_relevant_multi_platform_whitelistv1&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-4-117036377-blog-124181920.pc_relevant_multi_platform_whitelistv1)
  - [eslint+prettier 统一代码风格](https://www.cnblogs.com/shi2310/p/14267460.html)
  
## 7.2 解决CORS跨域问题: No 'Access-Control-Allow-Origin' header is present on the requested resource.
  [后端配置](https://blog.51cto.com/u_12564104/5235494)
  
  [前端配置](https://blog.51cto.com/u_12564104/5235494](https://learner.blog.csdn.net/article/details/88955387)
  
  
## 7.3 VUE路由的hash模式与history模式

### 7.3.1 背景知识

大多数vue项目采用SPA(单页面应用)的模式开发，不同视图的切换，都要通过前端路由去管理和控制。

因此平时我们开发vue的项目，都会install vue-router来实现前端路由，控制视图的切换。

前端路由的作用，就是改变视图的同时不会向后端发出请求。

vue-Router的原理就是利用了浏览器自身的两个特性(hash和history),来实现前端路由的功能。

### 7.3.2 history和hash实现原理

> **history mode实现原理**

介绍history mode前，需要先认识window.history对象

![histroy mode原理](https://segmentfault.com/img/bVbGwdS)

- window.history 提供了两类API:
  - 一类是go(), back(), forward()这种定位到某个浏览历史的记录上；
  - 另外一类是pushState(), replaceState()这种，是操作历史记录的接口（添加和替换历史记录栈）。

- history mode就是使用pushState()和replaceState()来实现前端路由，通过这两个方法改变url，页面不会重新刷新。
使用这两个方法更改url后，会触发popstate事件，监听popstate事件，实现前端路由。

- window.addEventListener('popstate', function(e) { alert('url 更新') }); 当我们访问同域下不同的url时，就能触发popstate事件

> **hash mode实现原理**

- hash mode下的url都有一个特点，就是url里面带'#'号，如：https://www.baidu.com/#/view1。 '#'号后面就是hash值。
![](https://segmentfault.com/img/bVbGvJD)

- 同样的，改变hash值，也不会向服务器发出请求，因此也就不会刷新页面。每次hash值发生改变的时候，会触发hashchange事件。通过监听hashchange事件，实现前端路由：

### 7.3.3 history和hash的差异

- 1.history和hash都是利用浏览器的两种特性实现前端路由，history是利用浏览历史记录栈的API实现，hash是监听location对象hash值变化事件来实现
- 2.history的url没有'#'号，hash反之
- 3.history修改的url可以是同域的任意url，hash是同文档的url
- 4.相同的url，history会触发添加到浏览器历史记录栈中，hash不会触发。


### 7.3.4 history和hash的优点和缺点
- 1.history比hash的url美观（没有'#'号）
- 2.history修改的url可以是同域的任意url，hash则只能是同文档的url
- 3.history模式往往需要后端支持，如果后端nginx没有覆盖路由地址，就会返回404，hash因为是同文档的url，即使后端没有覆盖路由地址，也不会返回404
- 4.hash模式下，如果把url作为参数传后端，那么后端会直接从'#'号截断，只处理'#'号前的url，因此会存在#后的参数内容丢失的问题，不过这个问题hash模式下也有解决的方法。

### 7.3.5 总结
一般场景下，前端路由使用history或hash都可以，个人推荐history mode，history mode更加符合个人使用习惯，只要后端nginx做好配置即可。

