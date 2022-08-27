
# 五、Docker

## 1、简介

Docker是一个开源的应用容器引擎

将软件编译成一个镜像；然后在镜像里各种软件做好配置，将镜像发布出去，其他的使用这就可以直接使用这个镜像。运行中的这个镜像叫做容器，容器启动速度快，类似ghost操作系统，安装好了什么都有了；

## 2、Docker的核心概念

docker主机（HOST）:安装了Docker程序的机器（Docker直接安装在操作系统上的）

docker客户端（Client）:操作docker主机

docker仓库（Registry）：用来保存打包好的软件镜像

docker镜像（Image）:软件打好包的镜像，放到docker的仓库中

docker容器（Container）:镜像启动后的实例（5个容器启动5次镜像）

docker的步骤：

​	1、安装Docker

​	2、去Docker仓库找到这个软件对应的镜像；

​	3、使用Docker运行的这个镜像，镜像就会生成一个容器

​	4、对容器的启动停止，就是对软件的启动和停止

## 3、安装Docker

### 1、安装Linux

[安装vxbox并且安装ubuntu](http://note.youdao.com/noteshare?id=06ccb673d253fea78fe35430465758e1)

### 2、在linux上安装docker

```shell
1、查看centos版本
# uname -r
3.10.0-693.el7.x86_64
要求：大于3.10
如果小于的话升级*（选做）
# yum update
2、安装docker
# yum install docker
3、启动docker
# systemctl start docker
# docker -v
4、开机启动docker
# systemctl enable docker
5、停止docker
# systemctl stop docker
```

## 4、docker的常用操作

### 1、镜像操作

1、搜索

```shell
docker search mysql
```

默认去docker hub网站查找![44.docker1](E:\工作文档\SpringBoot\images\44.docker1.jpg)

2、拉取

```shell
默认最新版本
# docekr pull mysql
安装指定版本
# docker pull mysql:5.5
```

3、查看

```shell
docker images
```

4、删除

```
docker rmi imageid
```

### 2、容器操作

软件的镜像（qq.exe） -- 运行镜像 -- 产生一个容器（正在运行的软件）

```shell
1、搜索镜像
# docker search tomcat
2、拉取镜像
# docker pull tomcat
3、根据镜像启动容器
[root@lion ~]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
docker.io/tomcat    latest              d3d38d61e402        35 hours ago        549 MB
[root@lion ~]# docker run --name mytomcat -d tomcat:latest
2f0348702f5f2a2777082198795d8059d83e5ee38f430d2d44199939cc63e249
4、查看那个进程正在进行
[root@lion ~]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
2f0348702f5f        tomcat:latest       "catalina.sh run"   41 seconds ago      Up 39 seconds       8080/tcp            mytomcat
5、停止运行中容器
[root@lion ~]# docker stop 2f0348702f5f
2f0348702f5f
6、查看所有容器
[root@lion ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                       PORTS               NAMES
2f0348702f5f        tomcat:latest       "catalina.sh run"   52 minutes ago      Exited (143) 2 minutes ago                       mytomcat
7、启动容器
[root@lion ~]# docker start 2f0348702f5f
8、删除docker容器
[root@lion ~]# docker rm 2f0348702f5f
2f0348702f5f
9、端口映射
[root@lion ~]# docker run --name mytomcat -d -p 8888:8080 tomcat
692c408c220128014df32ecb6324fb388427d1ecd0ec56325580135c58f63b29
虚拟机:8888
容器的:8080
-d:后台运行
-p:主机端口映射到容器端口
浏览器：192.168.179.129:8888
10、docker的日志
[root@lion ~]# docker logs 692c408c2201
11、多个启动
[root@lion ~]# docker run -d -p 9000:8080 --name mytomcat2 tomcat
浏览器：192.168.179.129:9000
```

更多命令参考docker镜像文档

### 3、安装Mysql

```shell
docker pull mysql
docker run --name mysql001 -e MYSQL_ROOT_PASSWORD -d -p 3307:3306 mysql
```
