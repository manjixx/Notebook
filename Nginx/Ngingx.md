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
