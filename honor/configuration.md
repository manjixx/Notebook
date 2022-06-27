# 软件安装

> ## Beyond Compare 
- Beyond Compare是一套由Scooter Software推出的软件，主要用途比较多。Beyond Compare可以比较的内容有以下这三种：
  - 本地两个目录的内容

  - 本地的目录和FTP地址的内容
    
  - 文本档案的内容（包括 UTF-8、html、Delphi源程序等文本档案）
  
  - 同时，还可以进行文件夹合并、文件合并、文件夹同步等。文件比较重，可以进行hex比较、table比较、注册列表对比、图片对比、版本对比、MP3对比等

> ## Notepad++


> ## git

- [安装教程](https://blog.csdn.net/wdh1994115/article/details/104916177)

- git常用流程
![git常用流程](https://img-blog.csdnimg.cn/20200528121000778.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hhaWxvbmdjc2Ru,size_16,color_FFFFFF,t_70)

- 查看版本 ```git --version```

> ## TortoiseGit

- TortoiseGit其实是一款开源的git的版本控制系统，也叫海龟git。TortoiseGit提供了人性化的图形化界面，不用像Git一样输入许多语句，像git init、git add、git commit这些语句就通通不用记了。轻松使用鼠标，就可以完成代码的提交和上传。对于使用本地Git的新手来说，TortoiseGit更加简便，更加容易上手。

- [TortoiseGit的介绍和使用](https://blog.csdn.net/hailongcsdn/article/details/106399635)

> ## MobaXterm
- 终端

### MobaXterm主要功能
- 1. 远程会话管理器：单个应用程序中的SSH，SFTP，telnet，VNC，Mosh，RDP连接
![远程会话管理](https://img2018.cnblogs.com/blog/774327/201901/774327-20190111221725208-1355107434.png)
- 2. Windows上的许多Unix/Linux命令：基本Cygwin命令（bash，grep，awk，sed，rsync，...
- 3. 丰富的组件和插件，可以自由选择。详情查看MobaXterm Plugins
- 4. 远程桌面：使用RDP，VNC或XDMCP在计算机上显示完整的远程桌面
- 5. 嵌入式Xserver：在Windows计算机上显示远程应用程序

# IDEA 环境配置

> ## 安装 IDEA OpenJDK、maven、nodejs
- 安装Mave,[Maven路径配置](https://www.runoob.com/maven/maven-setup.html)
```bash
<!--Maven验证-->
mvn -v
Apache Maven 3.6.3 (cecedd343002696d0abb50b32b541b8a6ba2883f)
Maven home: D:\software\apache-maven-3.6.3\bin\..
Java version: 11.0.13, vendor: Oracle Corporation, runtime: C:\Program Files\Java\openjdk-11.0.13_8
Default locale: zh_CN, platform encoding: GBK
OS name: "windows 10", version: "10.0", arch: "amd64", family: "windows"
```
- 安装nodejs
  - [Node.js安装配置](https://www.runoob.com/nodejs/nodejs-install-setup.html)

  - 设置npm镜像
  ```bash
  npm config set registry http://cmc.cloudartifact.dragon.tools.hihonor.com/artifactory/api/npm/npm-virtual
  ```
  
  - 设置Node-Sass的镜像地址
  ```bash
  npm config set SASS_BINARY_SITE http://cmc.cloudartifact.dragon.tools.hihonor.com/artifactory/mirrors/node-sass
  ```
  
  - 设置全局模块安装路径（node_global）与缓存路径（node_cache）
  ```bash
  npm config set prefix "D:\software\nodejs\node_global" 
  npm config set cache "D:\software\nodejs\node_cache"
  ```

> ## IDEA工程配置

- 加载OTA工程

- 设置JDK版本

- maven设置
```bash
<!--配置文件路径-->
C:\Users\w50010425\.m2\settings.xml
<!--仓库路径-->
D:\apache-maven-3.6.3\repository
```


> ## vue编译环境配置
- 按照 安装nodejs中步骤完成nodejs安装与配置

- 安装vue脚手架

```bash
npm install -g @vue/cli
```

> ## 代码编译运行与调试

### 前台编译与调试
- 进入工程目录```OTAPlatform\baseline-portal-fronend```

### 后台程序编译运行

#### Error
- 问题1：
  - 问题描述
  > maven无法下载依赖，报错信息如下
    ```bash
    [ERROR] org.apache.maven.model.resolution.UnresolvableModelException: Failure to transfer org.springframework.boot:spring-boot-starter-parent:pom:2.6.4 from https://mirrors.huaweicloud.com/repository/maven/ was cached in the local repository, resolution will not be reattempted until the update interval of huaweicloud has elapsed or updates are forced. Original error: Could not transfer artifact org.springframework.boot:spring-boot-starter-parent:pom:2.6.4 from/to huaweicloud (https://mirrors.huaweicloud.com/repository/maven/): Transfer failed for https://mirrors.huaweicloud.com/repository/maven/org/springframework/boot/spring-boot-starter-parent/2.6.4/spring-boot-starter-parent-2.6.4.pom
    ```
  - 解决方案
   > 查看setting.XML文件中的镜像源设置,将ota-5.0.0.pom文件放入\apache-maven-3.6.3\repo\com\hihonor\ota\ota\5.0.0

