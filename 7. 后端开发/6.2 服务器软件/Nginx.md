# 一、Nginx简介与基本概念

## 1.1 什么是Nginx

Nginx (engine x) 是一款轻量级的 Web 服务器 、反向代理服务器及电子邮件（IMAP/POP3）代理服务器。

![架构图](https://pic1.zhimg.com/80/v2-e1826bab1d07df8e97d61aa809b94a10_720w.jpg)

上图基本上说明了当下流行的技术架构，其中Nginx有点入口网关的味道

## 1.2 正向代理、反向代理与透明代理

> 正向代理

**正向代理的概念**

正向代理（forward）意思是一个位于客户端和原始服务器 (origin server) 之间的服务器，为了从原始服务器取得内容，客户端向代理发送一个请求并指定目标 (原始服务器)，然后代理向原始服务器转交请求并将获得的内容返回给客户端。

正向代理是为我们服务的，即为客户端服务的，客户端可以根据正向代理访问到它本身无法访问到的服务器资源。

正向代理对我们是透明的，对服务端是非透明的，即服务端并不知道自己收到的是来自代理的访问还是来自真实客户端的访问。

![正向代理示意图](https://pic4.zhimg.com/80/v2-c8ac111c267ae0745f984e326ef0c47f_720w.jpg)

由于防火墙的原因，我们并不能直接访问谷歌，那么我们可以借助VPN来实现，这就是一个简单的正向代理的例子。这里你能够发现，正向代理“代理”的是客户端，而且客户端是知道目标的，而目标是不知道客户端是通过VPN访问的。

**正向代理的作用**

  - 访问原来无法访问的资源，如google
  - 可以做缓存，加速访问资源
  - 客户端访问授权，上网进行认证
  - 可以记录用户访问记录（上网行为管理），对外隐藏用户信息

> 反向代理

**反向代理的概念**

反向代理（Reverse Proxy）方式是指以代理服务器来接受 internet 上的连接请求，然后将请求转发给内部网络上的服务器，并将从服务器上得到的结果返回给 internet 上请求连接的客户端，此时代理服务器对外就表现为一个反向代理服务器。

反向代理是为服务端服务的，反向代理可以帮助服务器接收来自客户端的请求，帮助服务器做请求转发，负载均衡等。

反向代理对服务端是透明的，对我们是非透明的，即我们并不知道自己访问的是代理服务器，而服务器知道反向代理在为他服务。

![反向代理示意图](https://pic2.zhimg.com/80/v2-4787a512240b238ebf928cd0651e1d99_720w.jpg)

当我们在外网访问百度的时候，其实会进行一个转发，代理到内网去，这就是所谓的反向代理，即反向代理“代理”的是服务器端，而且这一个过程对于客户端而言是透明的。

**反向代理的作用**

- 保证内网安全，可以使用反向代理提供WAF功能，组织web攻击
  
  ![反向代理保证内网安全](https://images2015.cnblogs.com/blog/305504/201611/305504-20161112124341280-1435223816.png)

- 负载均衡，通过反向代理服务器来优化网站的负载
  
   ![负载均衡](https://images2015.cnblogs.com/blog/305504/201611/305504-20161112124423530-566240666.png)

> 正向代理与方向代理的区别

实际上proxy在两种代理中做的事都是**代为收发请求和响应**，不过从结构上来看正好左右互换了下，所以把后出现的那种代理方式叫成了反向代理。

- 正向代理中，proxy和client同属一个LAN，对server透明；

- 反向代理中，proxy和server同属一个LAN，对client透明。

![正向代理与反向代理的区别](https://pic2.zhimg.com/80/480c1c45d2565e2f92fd930d25b73a18_720w.jpg?source=1940ef5c)

> 透明代理

透明代理的意思是客户端根本不需要知道有代理服务器的存在，它改编你的request fields（报文），并会传送真实IP。注意，加密的透明代理则是属于匿名代理，意思是不用设置使用代理了。
透明代理实践的例子就是时下很多公司使用的行为管理软件。如下图所示：
![透明代理](https://img2018.cnblogs.com/blog/1320725/201904/1320725-20190404092818195-1584585914.png)

用户A和用户B并不知道行为管理设备充当透明代理行为，当用户A或用户B向服务器A或服务器B提交请求的时候，透明代理设备根据自身策略拦截并修改用户A或B的报文，并作为实际的请求方，向服务器A或B发送请求，当接收信息回传，透明代理再根据自身的设置把允许的报文发回至用户A或B，如上图，如果透明代理设置不允许访问服务器B，那么用户A或者用户B就不会得到服务器B的数据

# 二、Nginx入门

[英文文档](nginx.org/en/docs/)

[中文文档](www.nginx.cn/doc/)

## 2.1 Nginx安装方法

详细安装方法请参考 [Nginx运维](https://github.com/dunwu/nginx-tutorial/blob/master/docs/nginx-ops.md)

**MacOS系统**
```shell
# 安装 Nginx：

brew install nginx

# 卸载 Nginx：

brew uninstall nginx

# 验证Nginx是否安装成功
nginx -V
```

## 2.2 Nginx常用命令

> **Nginx常用命令**
```shell
start nginx        # 启动Nginx
nginx -s stop      # 快速关闭Nginx，可能不保存相关信息，并迅速终止web服务。
nginx -s quit      # 平稳关闭Nginx，保存相关信息，有安排的结束web服务。
nginx -s reload    # 因改变了Nginx相关配置，需要重新加载配置而重载。
nginx -s reopen    # 重新打开日志文件。
nginx -c filename  # 为 Nginx 指定一个配置文件，来代替缺省的。
nginx -t           # 不运行，仅仅测试配置文件。nginx 将检查配置文件的语法的正确性，并尝试打开配置文件中所引用到的文件。
nginx -v           # 显示 nginx 的版本。
nginx -V           # 显示 nginx 的版本，编译器版本和配置参数。
```

> **常用的几个文件路径**

注意此处仅供参考实际使用时需要根据实际情况进行判断

```shell
/usr/local/etc/nginx/nginx.conf     # nginx配置文件路径
/usr/local/var/www                  # nginx服务器默认的根目录
/usr/local/Cellar/nginx/1.17.9      # nginx的安装路径
/usr/local/var/log/nginx/error.log  # nginx默认的日志路径
```

> **编写启动脚本**

**Windows系统**
Windows系统下，如果不想每次都敲命令，可在Nginx安装目录下新添加一个启动批处理文件startup.bat,双击运行即可，内容如下：
```bat
@echo off
rem 如果启动前已经启动nginx并记录下pid文件，会kill指定进程
nginx.exe -s stop

rem 测试配置文件语法正确性
nginx.exe -t -c conf/nginx.conf

rem 显示版本信息
nginx.exe -v

rem 按照指定配置去启动nginx
nginx.exe -c conf/nginx.conf
```

**Linux系统**

Linux系统中Nginx启动脚本请参考 [Nginx启动脚本](https://www.cnblogs.com/xiangsikai/p/8393648.html)

**MacOS**

## 2.3 Nginx默认配置文件简介
```conf
# 首尾配置暂时忽略
server {  
        # 当nginx接到请求后，会匹配其配置中的service模块
        # 匹配方法就是将请求携带的host和port去跟配置中的server_name和listen相匹配
        listen       8080;        
        server_name  localhost; # 定义当前虚拟主机（站点）匹配请求的主机名

        location / {
            root   html; # Nginx默认值
            # 设定Nginx服务器返回的文档名
            index  index.html index.htm; # 先找根目录下的index.html，如果没有再找index.htm
        }
}
```
server{ } 其实是包含在 http{ } 内部的。每一个 server{ } 是一个虚拟主机（站点）。

上述代码块意思是：当一个请求叫做localhost:8080请求nginx服务器时，该请求就会被匹配进该代码块的 server{ } 中执行。

当然 nginx 的配置非常多，用的时候可以根据文档进行配置。

## 2.4 Nginx的工作模式

> **Nginx的master-worker模式(默认)**

**master-worker模式**下nginx启动成功后，会有一个master进程和至少一个的worker进程，**worker进程数量建议等于cpu总核心数。**

![Nginx的master-worker模式](https://pic4.zhimg.com/80/v2-b24eb2b29b48f59883232a58392ddae3_720w.jpg)

启动Nginx后，其实就是在80端口启动了Socket监听服务

**master进程**负责处理系统信号，加载配置，管理worker进程（启动，杀死，监控，发送消息/信号等

**worker进程**负责处理具体的业务逻辑，也就是说，对外部来说，真正提供服务的是worker进程

**优点**

- 稳定性高，只要还有worker进程存活，就能够提供服务，并且一个worker进程挂掉master进程会立即启动一个新的worker进程，保证worker进程数量不变，降低服务中断的概率。

- 配合linux的cpu亲和性配置，可以充分利用多核cpu的优势，提升性能

- 处理信号/配置重新加载/升级时可以做到尽可能少或者不中断服务


**nginx.conf中配置**
```conf
worker_processes  4;
```

**终端查看配置结果**

```shell
[root@cn_remote_nginx_232_121 sbin]# cd /usr/local/nginx/sbin/
[root@cn_remote_nginx_232_121 sbin]# pwd
/usr/local/nginx/sbin
[root@cn_remote_nginx_232_121 sbin]# ./nginx
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
nginx: [emerg] still could not bind()
[root@cn_remote_nginx_232_121 sbin]# ps aux | grep nginx 
root      11744  0.0  0.0  77676  3012 ?        Ss   Jul22   0:00 nginx: master process ../sbin/nginx
hpbi      52358  0.0  0.1  86008 10752 ?        S    11:08   0:00 nginx: worker process
hpbi      52359  0.0  0.1  86008 10976 ?        S    11:08   0:00 nginx: worker process
hpbi      52360  0.0  0.1  86008 10980 ?        S    11:08   0:00 nginx: worker process
hpbi      52361  0.0  0.1  86360 11516 ?        S    11:08   0:00 nginx: worker process
root      57278  0.0  0.0 112812   980 pts/0    S+   12:01   0:00 grep --color=auto nginx

[root@cn_remote_nginx_232_121 sbin]# netstat -tnlup | grep nginx
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      11744/nginx: master 
```

> **Nginx的单进程模式**

**Nginx单进程模式**

单进程模式下，nginx启动后只有一个进程，nginx的所有工作都由这个进程负责。因此，该模式一般只在开发阶段和调试时使用，生产环境下不会使用。

**优点**

单进程模式由于只有一个进程，因此可以很方便地利用gdb等工具进行调试。

**缺点**
单进程模式不支持nginx的平滑升级功能，任何的信号处理都可能造成服务中断，并且由于是单进程，进程挂掉后，在没有外部监控的情况下，无法重启服务。



## 2.5 思考

> **Nginx如何做到热部署**

所谓热部署，就是配置文件nginx.conf修改后，不需要stop Nginx，不需要中断请求，就能让配置文件生效！

通过上文我们已经知道worker进程负责处理具体的请求，那么如果想达到热部署的效果，则可通过如下两种方案：

方案一：修改配置文件```nginx.conf```之后**主进程master负责推送给woker进程更新配置信息**，woker进程收到信息后，更新进程内部的线程信息。（有点volatile的味道）

方案二: 修改配置文件`nginx.conf`后，重新生成新的worker进程，当然会以新的配置进行处理请求，而且新的请求必须都交给新的worker进程，至于老的worker进程，等把那些以前的请求处理完毕后，kill掉即可。

Nginx通过采用方案二来实现热部署的。

> **Nginx如何做到高并发下的高效处理**

上文已经提及Nginx的worker进程个数与CPU绑定、worker进程内部包含一个线程高效回环处理请求，这的确有助于效率，但这是不够的。

Nginx采用了Linux的epoll模型，epoll模型基于事件驱动机制，它可以监控多个事件是否准备完毕，如果OK，那么放入epoll队列中，这个过程是异步的。worker只需要从epoll队列循环处理即可。

> **Nginx挂了怎么办**

**Keepalived + Nginx实现高可用**

Keepalived是一个高可用解决方案，主要是用来防止服务器单点发生故障，可以通过和Nginx配合来实现Web服务的高可用。（其实，Keepalived不仅仅可以和Nginx配合，还可以和很多其他服务配合）

Keepalived+Nginx实现高可用的思路：
- 请求不要直接打到Nginx上，应该先通过Keepalived（这就是所谓虚拟IP，VIP）
- Keepalived应该能监控Nginx的生命状态（提供一个用户自定义的脚本，定期检查Nginx进程状态，进行权重变化,，从而实现Nginx故障切换）

![Keepalived + Nginx](https://pic4.zhimg.com/80/v2-ec3208d1ea659d126fe2a008ec5ae927_720w.jpg)

# 三、Nginx实战

Nginx主要有4大应用：
- 动静分离
- 反向代理
- 负载均衡
- 正向代理
  
## 3.1 动静分离

### 01 动静分离简介与原理

![动静分离](https://img2020.cnblogs.com/blog/680719/202007/680719-20200718123700927-1360012634.png)

> 动静分离简介
动静分离：即动态文件与静态文件的分离。其主要目的是为了提高网站响应速度，减轻程序服务器(Tomcat,Jboss等)的负载，**对于静态资源**，如图片、js、css等文件，可以在反向代理服务器中进行缓存，这样浏览器在请求一个静态资源时，代理服务器就可以直接处理，而不用将请求转发给后端服务器。**对于用户请求的动态文件**，如servlet、jsp，则转发给Tomcat，Jboss服务器处理，这就是动静分离。


动静分离可通过location对请求url进行匹配，将网站静态资源（HTML，JavaScript，CSS，img等文件）与后台应用分开部署，提高用户访问静态代码的速度，降低对后台应用访问。**通常将静态资源放到nginx中，动态资源转发到tomcat服务器中。**

### 02 动静分离实现- 根据文件后缀
[教程原链接](https://cloud.tencent.com/developer/article/1665215)

#### 2-1 环境准备

动静分离实验基于Nginx + Tomcat实现，其中

nginx01：进行前端代理，同时本地处理css静态文件
nginx02：处理图片、html、JS等静态文件
nginx03：tomcat处理jsp、servlet等动态请求。

| 主机 | IP | 角色 | 备注 |
| :-----| ----: | :----: |:----: |
| nginx01 | 172.24.10.21 | Nginx Proxy主机 | 接收请求，并代理至后端css存储点 |
| nginx02 | 172.24.10.22 | Nginx 静态服务器 | 处理静态请求                  |
| nginx03 | 172.24.10.23 | Nginx 动态服务器 | 处理动态请求                  |


#### 2-2 创建静态站点
- 在nginx02服务器，创建静态资源目录并上传图片静态资源
    ```shell
    [root@nginx02 ~]# mkdir /usr/share/nginx/staticrs/
    [root@nginx02 ~]# echo '<h1>Static_Web</h1>' > /usr/share/nginx/staticrs/index.html
    [root@nginx02 ~]# ll /usr/share/nginx/staticrs/		#上传示例图片静态资源
    total 16K
    -rw-r--r-- 1 root root  20 Jun 20 14:32 index.html
    -rw-r--r-- 1 root root 11K Jun 20 14:35 nginx.jpg
    [root@nginx02 ~]# mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
    ```
- 修改nginx02中的staticrs.conf文件
    ```shell
    [root@nginx02 ~]# vi /etc/nginx/conf.d/staticrs.conf
    server {
        listen  80;
        server_name  staticrs.linuxds.com;
        access_log  /var/log/nginx/staticrs.access.log  main;
        error_log   /var/log/nginx/staticrs.error.log  warn;
        location / {
            root   /usr/share/nginx/staticrs;
            index  index.html;
        }
    }
    ```
- 检查配置文件并重载配置文件
    ```shell
    [root@nginx02 ~]# nginx -t -c /etc/nginx/nginx.conf	#检查配置文件
    [root@nginx02 ~]# nginx -s reload			#重载配置文件
    ```

- 手动访问后端静态站点及资源：
  http://staticrs.linuxds.com/
  
  http://staticrs.linuxds.com/nginx.jpg

#### 2-3 创建动态站点

- 在nginx03服务器上安装Tomcat
  ```shell
  [root@nginx03 ~]# yum install -y tomcat
  [root@nginx03 ~]# mkdir -p /usr/share/tomcat/webapps/ROOT
  ```

- 构建动态测试页面
  ```shell
    [root@nginx03 ~]# vi /usr/share/tomcat/webapps/ROOT/javatest.jsp	#构建动态测试页面
    <%@ page language="java" import="java.util.*" pageEncoding="utf-8"%>
    <HTML>
    <HEAD>
        <TITLE>JSP Test Page</TITLE>
    </HEAD>

    <BODY>
        <%
        Random rand = new Random();
        out.println("<h1>随机数:<h1>");
        out.println(rand.nextInt(99)+100);
        %>
    </BODY>
    </HTML>
  ```

- 启动Tomcat
  ```shell
    [root@nginx03 ~]# systemctl start tomcat.service	#启动tomcat
  ```

- 手动访问后端动态站点及资源：http://dynamic.linuxds.com:8080/javatest.jsp
  
#### 2-4 在nginx01(nginx Proxy)配置动静分离

```shell
[root@nginx01 ~]# mkdir -p /usr/share/nginx/dss
[root@nginx01 ~]# ll /usr/share/nginx/dss/
total 4.0K
-rw-r--r-- 1 root root 1.9K Jun 20 18:10 test.css	#模拟css
```

- 修改配置文件
```conf
[root@nginx01 ~]# vi /etc/nginx/conf.d/dss.conf		# 配置Dynamic-Static Separation

upstream static_server {
    server 172.24.10.22;
}
upstream tomcat_server {
    server 172.24.10.23:8080;
}

server {
    listen       80;
    server_name  dss.linuxds.com;
    access_log  /var/log/nginx/dss.access.log  main;
    error_log   /var/log/nginx/dss.error.log  warn;
    proxy_set_header    X-Real-IP       $remote_addr;
    proxy_set_header    Host            $host;
    proxy_set_header    X-Forwarded-For         $proxy_add_x_forwarded_for;
    proxy_set_header    X-Forwarded-Proto       $scheme;
#    location / {
#        root html;
#        index index.html;
#    }
    location / {
        proxy_pass http://static_server;
    }
    location ~  .*\.(css)$  {
        root   /usr/share/nginx/dss;
    }
    location ~ .*\.(htm|html|gif|jpg|jpeg|png|gif|bmp|swf|ioc|rar|zip|txt|flv|mid|doc|ppt|pdf|xls|mp3|wma) {
        proxy_pass http://static_server;
        expires 5d;
    }
    location ~ .*\.jsp$ {
        proxy_pass http://tomcat_server;
        expires 1h;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }
}
```

- 检查配置文件并重载配置文件
```shell
[root@nginx01 ~]# nginx -t -c /etc/nginx/nginx.conf	#检查配置文件
[root@nginx01 ~]# nginx -s reload			#重载配置文件
```

#### 2-5 访问测试

浏览器分别访问：

http://dss.linuxds.com/

http://dss.linuxds.com/javatest.jsp

http://staticrs.linuxds.com/nginx.jpg

http://dss.linuxds.com/test.css


### 03 动静分离实现- 根据文件路径

#### 3-1 环境准备(同2-1)

#### 3-2 创建静态站点
- 在nginx02服务器，创建静态资源目录并上传图片静态资源（同2-2）

- 修改nginx02中的staticrs.conf文件
  ```shell
    [root@nginx02 ~]# vi /etc/nginx/conf.d/staticrs.conf
    server {
        listen  80;
        server_name  staticrs.linuxds.com;
        access_log  /var/log/nginx/staticrs.access.log  main;
        error_log   /var/log/nginx/staticrs.error.log  warn;
        location /static {
            # 此处与通过文件后缀配置动静分离不同
            alias   /usr/share/nginx/staticrs;
            index  index.html;
        }
    }
  ```

- 检查配置文件并重载配置文件

#### 3-3 创建动态站点
- 在nginx03服务器上安装Tomcat


- 构建动态测试页面

- 启动Tomcat

- 手动访问后端动态站点及资源：http://dynamic.linuxds.com:8080/javatest.jsp

#### 3-4 根据文件路径实现动静分离

```conf
[root@nginx01 ~]# vi /etc/nginx/conf.d/dss.conf		#配置Dynamic-Static Separation
upstream static_server {
    server 172.24.10.22;
}
upstream tomcat_server {
    server 172.24.10.23:8080;
}

server {
    listen       80;
    server_name  dss.linuxds.com;
    access_log  /var/log/nginx/dss.access.log  main;
    error_log   /var/log/nginx/dss.error.log  warn;
    proxy_set_header    X-Real-IP       $remote_addr;
    proxy_set_header    Host            $host;
    proxy_set_header    X-Forwarded-For         $proxy_add_x_forwarded_for;
    proxy_set_header    X-Forwarded-Proto       $scheme;
#    location / {
#        root html;
#        index index.html;
#    }
    location / {
        proxy_pass http://static_server;
    }
    location ~  .*\.(css)$  {
        root   /usr/share/nginx/dss;
    }
    # 此处与通过文件后缀配置动静分离不同
    location /static/ {
        proxy_pass http://static_server;
        expires 5d;
    }
    # 此处与通过文件后缀配置动静分离不同
    location /dynamic/ {
        proxy_pass http://tomcat_server;
        expires 1h;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }
}
```

#### 3-5 访问测试


## 3.2 反向代理

### 01 Http反向代理

此处仅完成一个http反向代理

> **http反向代理中nginx.conf文件如下**

```shell
#运行用户
#user somebody;

#启动进程,通常设置成和cpu的数量相等
worker_processes  1;

#全局错误日志
error_log  D:/Tools/nginx-1.10.1/logs/error.log;
error_log  D:/Tools/nginx-1.10.1/logs/notice.log  notice;
error_log  D:/Tools/nginx-1.10.1/logs/info.log  info;

#PID文件，记录当前启动的nginx的进程ID
pid        D:/Tools/nginx-1.10.1/logs/nginx.pid;

#工作模式及连接数上限
events {
    worker_connections 1024;    #单个后台worker process进程的最大并发链接数
}

#设定http服务器，利用它的反向代理功能提供负载均衡支持
http {
    #设定mime类型(邮件支持类型),类型由mime.types文件定义
    include       D:/Tools/nginx-1.10.1/conf/mime.types;
    default_type  application/octet-stream;

    #设定日志
	log_format  main  '[$remote_addr] - [$remote_user] [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    access_log    D:/Tools/nginx-1.10.1/logs/access.log main;
    rewrite_log     on;
    #sendfile 指令指定 nginx 是否调用 sendfile 函数（zero copy 方式）来输出文件，对于普通应用，
    #必须设为 on,如果用来进行下载等应用磁盘IO重负载应用，可设置为 off，以平衡磁盘与网络I/O处理速度，降低系统的uptime.
    sendfile        on;
    #tcp_nopush     on;
    #连接超时时间
    keepalive_timeout  120;
    tcp_nodelay        on;

	#gzip压缩开关
	#gzip  on;

    #设定实际的服务器列表
    upstream zp_server1{
        server 127.0.0.1:8089;
    }

    #HTTP服务器
    server {
        #监听80端口，80端口是知名端口号，用于HTTP协议
        listen       80;

        #定义使用www.xx.com访问
        server_name  www.helloworld.com;

		#首页
		index index.html

		#指向webapp的目录
		root D:\01_Workspace\Project\github\zp\SpringNotes\spring-security\spring-shiro\src\main\webapp;

		#编码格式
		charset utf-8;

		#代理配置参数
        proxy_connect_timeout 180;
        proxy_send_timeout 180;
        proxy_read_timeout 180;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarder-For $remote_addr;

        #反向代理的路径（和upstream绑定），location 后面设置映射的路径
        location / {
            proxy_pass http://zp_server1;
        }

        #静态文件，nginx自己处理
        location ~ ^/(images|javascript|js|css|flash|media|static)/ {
            root D:\01_Workspace\Project\github\zp\SpringNotes\spring-security\spring-shiro\src\main\webapp\views;
            #过期30天，静态文件不怎么更新，过期可以设大一点，如果频繁更新，则可以设置得小一点。
            expires 30d;
        }

        #设定查看Nginx状态的地址
        location /NginxStatus {
            stub_status           on;
            access_log            on;
            auth_basic            "NginxStatus";
            auth_basic_user_file  conf/htpasswd;
        }

        #禁止访问 .htxxx 文件
        location ~ /\.ht {
            deny all;
        }

		#错误处理页面（可选择性配置）
		#error_page   404              /404.html;
		#error_page   500 502 503 504  /50x.html;
        #location = /50x.html {
        #    root   html;
        #}
    }
}
```

> **执行如下操作**

- 启动 webapp，注意启动绑定的端口要和 nginx 中的 upstream 设置的端口保持一致。
- 更改 host：在 C:\Windows\System32\drivers\etc 目录下的 host 文件中添加一条 DNS 记```127.0.0.1 www.helloworld.com```
- 启动前文中 startup.bat 的命令
- 浏览器访问www.helloworld.com



### 02 Https反向代理

> **基础知识**
- HTTPS是一种使用SSL通信标准的安全HTTP协议
- HTTPS 的固定端口号是 443，不同于 HTTP 的 80 端口
- SSL 标准需要引入安全证书，所以在 nginx.conf 中你需要指定证书和它对应的 key

> **nginx配置**
其他和 http 反向代理基本一样，只是在 Server 部分配置有些不同。
```shell
  server {
      #监听443端口。443为知名端口号，主要用于HTTPS协议
      listen       443 ssl;

      #定义使用www.xx.com访问
      server_name  www.helloworld.com;

      #ssl证书文件位置(常见证书文件格式为：crt/pem)
      ssl_certificate      cert.pem;
      #ssl证书key位置
      ssl_certificate_key  cert.key;

      #ssl配置参数（选择性配置）
      ssl_session_cache    shared:SSL:1m;
      ssl_session_timeout  5m;
      #数字签名，此处使用MD5
      ssl_ciphers  HIGH:!aNULL:!MD5;
      ssl_prefer_server_ciphers  on;

      location / {
          root   /root;
          index  index.html index.htm;
      }
  }

```

### 03 网站有多个webapp的配置

当一个网站功能越来越丰富时，往往需要将一些功能相对独立的模块剥离出来，独立维护。这样的话，通常，会有多个 webapp。

> 场景举例

假设 www.helloworld.com 站点有好几个 webapp，finance（金融）、product（产品）、admin（用户中心）。访问这些应用的方式通过上下文(context)来进行区分:

- www.helloworld.com/finance/

- www.helloworld.com/product/

- www.helloworld.com/admin/

http 的默认端口号是 80，如果在一台服务器上同时启动这 3 个 webapp 应用，都用 80 端口，肯定是不成的。所以，**这三个应用需要分别绑定不同的端口号**。

但是用户在请求www.helloworld.com 站点时，需要访问不同 webapp，应使用统一的端口号，因此需要使用反向代理来做处理。

> 网站有多个webapp的nginx配置
```shell
http {
	#此处省略一些基本配置

	upstream product_server{
		server www.helloworld.com:8081;
	}

	upstream admin_server{
		server www.helloworld.com:8082;
	}

	upstream finance_server{
		server www.helloworld.com:8083;
	}

	server {
		#此处省略一些基本配置
		#默认指向product的server
		location / {
			proxy_pass http://product_server;
		}

		location /product/{
			proxy_pass http://product_server;
		}

		location /admin/ {
			proxy_pass http://admin_server;
		}

		location /finance/ {
			proxy_pass http://finance_server;
		}
	}
}
```



## 3.3 负载均衡

网站在实际运营过程中，大部分都是以集群的方式运行，这时需要使用负载均衡来分流。nginx 也可以实现简单的负载均衡功能。

![Nginx负载均衡](https://raw.githubusercontent.com/dunwu/images/dev/cs/web/nginx/nginx-load-balance.png)


### 01 场景

应用部署到三台Linux环境服务器上，IP分别为：192.168.1.11:80、192.168.1.12:80、192.168.1.13:80

公网IP：192.168.1.11 在公网 IP 所在的服务器上部署 nginx，对所有请求做负载均衡处理

网站域名：www.helloworld.com

### 02 nginx配置

> nginx.conf 配置(加权轮询策略)

```shell
http {
     #设定mime类型,类型由mime.type文件定义
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    #设定日志格式
    access_log    /var/log/nginx/access.log;

    #设定负载均衡的服务器列表
    upstream load_balance_server {
        #weigth参数表示权值，权值越高被分配到的几率越大
        server 192.168.1.11:80   weight=5;
        server 192.168.1.12:80   weight=1;
        server 192.168.1.13:80   weight=6;
    }

   #HTTP服务器
   server {
        #侦听80端口
        listen       80;

        #定义使用www.xx.com访问
        server_name  www.helloworld.com;

        #对所有请求进行负载均衡请求
        location / {
            root        /root;                 #定义服务器的默认网站根目录位置
            index       index.html index.htm;  #定义首页索引文件的名称
            proxy_pass  http://load_balance_server ;#请求转向load_balance_server 定义的服务器列表

            #以下是一些反向代理的配置(可选择性配置)
            #proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            #后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
            proxy_set_header X-Forwarded-For $remote_addr;
            proxy_connect_timeout 90;          #nginx跟后端服务器连接超时时间(代理连接超时)
            proxy_send_timeout 90;             #后端服务器数据回传时间(代理发送超时)
            proxy_read_timeout 90;             #连接成功后，后端服务器响应时间(代理接收超时)
            proxy_buffer_size 4k;              #设置代理服务器（nginx）保存用户头信息的缓冲区大小
            proxy_buffers 4 32k;               #proxy_buffers缓冲区，网页平均在32k以下的话，这样设置
            proxy_busy_buffers_size 64k;       #高负荷下缓冲大小（proxy_buffers*2）
            proxy_temp_file_write_size 64k;    #设定缓存文件夹大小，大于这个值，将从upstream服务器传

            client_max_body_size 10m;          #允许客户端请求的最大单文件字节数
            client_body_buffer_size 128k;      #缓冲区代理缓冲用户端请求的最大字节数
        }
    }
}
```


### 03 负载均衡策略

负载均衡策略在各种分布式系统中基本上原理一致，Nginx 提供了多种负载均衡策略

> 轮询

```shell
upstream bck_testing_01 {
  # 默认所有服务器权重为 1
  server 192.168.250.220:8080
  server 192.168.250.221:8080
  server 192.168.250.222:8080
}
```

> 加权轮询

```shell
upstream bck_testing_01 {
  server 192.168.250.220:8080   weight=3
  server 192.168.250.221:8080              # default weight=1
  server 192.168.250.222:8080              # default weight=1
}
```

> 最小连接

```shell
upstream bck_testing_01 {
  least_conn;

  # with default weight for all (weight=1)
  server 192.168.250.220:8080
  server 192.168.250.221:8080
  server 192.168.250.222:8080
}
```

> 加权最小连接

```shell
upstream bck_testing_01 {
  least_conn;

  server 192.168.250.220:8080   weight=3
  server 192.168.250.221:8080              # default weight=1
  server 192.168.250.222:8080              # default weight=1
}
```

> IP Hash
```shell
upstream bck_testing_01 {
  ip_hash;

  # with default weight for all (weight=1)
  server 192.168.250.220:8080
  server 192.168.250.221:8080
  server 192.168.250.222:8080
}
```

> 普通hash

```shell
upstream bck_testing_01 {

  hash $request_uri;

  # with default weight for all (weight=1)
  server 192.168.250.220:8080
  server 192.168.250.221:8080
  server 192.168.250.222:8080
}
```

## 3.4 正向代理

> nginx正向代理配置如下
```shell
server{
        resolver 8.8.8.8;
        resolver_timeout 30s; 
        listen 82;
        location / {
                proxy_pass http://$http_host$request_uri;
                proxy_set_header Host $http_host;
                proxy_buffers 256 4k;
                proxy_max_temp_file_size 0;
                proxy_connect_timeout 30;
                proxy_cache_valid 200 302 10m;
                proxy_cache_valid 301 1h;
                proxy_cache_valid any 1m;
        }
}
```

注意事項：
- 1、不能有hostname。 
- 2、必须有resolver, 即dns，即上面的8.8.8.8，超时时间（30秒）可选。 
- 3、配置正向代理参数，均是由 Nginx 变量组成。
    proxy_pass $scheme://$host$request_uri;  
    proxy_set_header Host $http_host;  
- 4、配置缓存大小，关闭磁盘缓存读写减少I/O，以及代理连接超时时间。
    proxy_buffers 256 4k;  
    proxy_max_temp_file_size 0;  
    proxy_connect_timeout 30;  
- 5、配置代理服务器 Http 状态缓存时间。
    proxy_cache_valid 200 302 10m;  
    proxy_cache_valid 301 1h;  
    proxy_cache_valid any 1m; 

- 配置好后，重启nginx，以浏览器为例，要使用这个代理服务器，则只需将浏览器代理设置为http://+服务器ip地址+:+82（82是刚刚设置的端口号）即可使用了。

## 3.5 透明代理

> nginx透明代理配置示例

```shell
# cat /etc/nginx/sites-enabled/proxy
       server {
                resolver        8.8.8.8;
                access_log      off;
                listen  [::]:8080;
                location / {
                        proxy_pass      $scheme://$host$request_uri;
                        proxy_set_header Host $http_host;
                        proxy_buffers   256 4k;
                        proxy_max_temp_file_size        0k;
                        }
                }
 
iptables -t nat -A PREROUTING -s 10.8.0.0/24 -p tcp --dport 80 -j DNAT --to 192.168.0.253:8080
RAW Paste Data
# cat /etc/nginx/sites-enabled/proxy
       server {
                resolver        8.8.8.8;
                access_log      off;
                listen  [::]:8080;
                location / {
                        proxy_pass      $scheme://$host$request_uri;
                        proxy_set_header Host $http_host;
                        proxy_buffers   256 4k;
                        proxy_max_temp_file_size        0k;
                        }
                }

iptables -t nat -A PREROUTING -s 10.8.0.0/24 -p tcp --dport 80 -j DNAT --to 192.168.0.253:8080

```





## 3.6 搭建文件服务器

> nginx中配置要点
- 将 autoindex 开启可以显示目录，默认不开启。
- 将 autoindex_exact_size 开启可以显示文件的大小。
- 将 autoindex_localtime 开启可以显示文件的修改时间。
- root 用来设置开放为文件服务的根路径。
- charset 设置为 charset utf-8,gbk;，可以避免中文乱码问题（windows 服务器下设置后，依然乱码，本人暂时没有找到解决方法）。

> 简化配置

```shell
autoindex on;# 显示目录
autoindex_exact_size on;# 显示文件大小
autoindex_localtime on;# 显示文件时间

server {
    charset      utf-8,gbk; # windows 服务器下设置后，依然乱码，暂时无解
    listen       9050 default_server;
    listen       [::]:9050 default_server;
    server_name  _;
    root         /share/fs;
}
```

## 3.7 解决跨域问题

web 领域开发中，经常采用前后端分离模式。这种模式下，前端和后端分别是独立的 web 应用程序，例如：后端是 Java 程序，前端是 React 或 Vue 应用。

> 解决跨域问题的两种思路

- **CORS**：在后端服务器设置 HTTP 响应头，把你需要允许访问的域名加入 Access-Control-Allow-Origin 中。

- **jsonp**：把后端根据请求，构造 json 数据，并返回，前端用 jsonp 跨域。

> nginx跨域解决方案

nginx 根据第一种思路，也提供了一种解决跨域的解决方案。

例子：www.helloworld.com 网站是由一个前端 app ，一个后端 app 组成的。前端端口号为 9000， 后端端口号为 8080。前端和后端如果使用 http 进行交互时，请求会被拒绝，因为存在跨域问题。

- 首先，在 enable-cors.conf 文件中设置 cors ：

```conf
# allow origin list
set $ACAO '*';

# set single origin
if ($http_origin ~* (www.helloworld.com)$) {
  set $ACAO $http_origin;
}

if ($cors = "trueget") {
	add_header 'Access-Control-Allow-Origin' "$http_origin";
	add_header 'Access-Control-Allow-Credentials' 'true';
	add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
	add_header 'Access-Control-Allow-Headers' 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type';
}

if ($request_method = 'OPTIONS') {
  set $cors "${cors}options";
}

if ($request_method = 'GET') {
  set $cors "${cors}get";
}

if ($request_method = 'POST') {
  set $cors "${cors}post";
}
```

- 其次在服务器nginx配置文件中`include enable-cors.conf`引入跨域配置
```conf
# ----------------------------------------------------
# 此文件为项目 nginx 配置片段
# 可以直接在 nginx config 中 include（推荐）
# 或者 copy 到现有 nginx 中，自行配置
# www.helloworld.com 域名需配合 dns hosts 进行配置
# 其中，api 开启了 cors，需配合本目录下另一份配置文件
# ----------------------------------------------------
upstream front_server{
  server www.helloworld.com:9000;
}
upstream api_server{
  server www.helloworld.com:8080;
}

server {
  listen       80;
  server_name  www.helloworld.com;

  location ~ ^/api/ {
    include enable-cors.conf;
    proxy_pass http://api_server;
    rewrite "^/api/(.*)$" /$1 break;
  }

  location ~ ^/ {
    proxy_pass http://front_server;
  }
}
```

# 四、参考资料
[Nginx中文维基](http://tool.oschina.net/apidocs/apidoc?api=nginx-zh)

[Nginx开发入门到精通](http://tengine.taobao.org/book/index.html)

[Nginx配置生成器](https://nginxconfig.io/)

[英文文档](nginx.org/en/docs/)

[中文文档](www.nginx.cn/doc/)
