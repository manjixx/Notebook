# Docker

## 一、Docker 概述

## 1.1 PaaS背景
  
2013-2014年Cloud Foundry 项目已经基本度过了最艰难的概念普及和用户教育阶段，吸引了包括百度、京东、华为、IBM 等一大批国内外技术厂商，开启了以开源 PaaS 为核心构建平台层服务能力的变革。

Cloud Foundry 这样的 PaaS 项目，最核心的组件就是一套应用的打包和分发机制。

Cloud Foundry 为每种主流编程语言都定义了一种打包格式，而`“cf push”`的作用，基本上等同于用户把应用的可执行文件和启动脚本打进一个压缩包内，上传到云上 Cloud Foundry 的存储中。接着，Cloud Foundry 会通过调度器选择一个可以运行这个应用的虚拟机，然后通知这个机器上的 Agent 把应用压缩包下载下来启动。这时候关键来了，由于需要在一个虚拟机上启动很多个来自不同用户的应用，

Cloud Foundry 会调用操作系统的 Cgroups 和 Namespace 机制为每一个应用单独创建一个称作“沙盒”的隔离环境，然后在“沙盒”中启动这些应用进程。这样，就实现了把多个用户的应用互不干涉地在虚拟机里批量地、自动地运行起来的目的。这，正是 PaaS 项目最核心的能力。 而这些 Cloud Foundry 用来运行应用的隔离环境，或者说“沙盒”，就是所谓的“容器”。

Docker 镜像解决的，恰恰就是打包这个根本性的问题。 所谓 Docker 镜像，其实就是一个压缩包。但是这个压缩包里的内容，比 PaaS 的应用可执行文件 + 启停脚本的组合就要丰富多了。
  
实际上，大多数 Docker 镜像是直接由一个完整操作系统的所有文件和目录构成的，所以这个压缩包里的内容跟你本地开发和测试环境用的操作系统是完全一样的。这就有意思了：假设你的应用在本地运行时，能看见的环境是 CentOS 7.2 操作系统的所有文件和目录，那么只要用 CentOS 7.2 的 ISO 做一个压缩包，再把你的应用可执行文件也压缩进去，那么无论在哪里解压这个压缩包，都可以得到与你本地测试时一样的环境。当然，你的应用也在里面！这就是 Docker 镜像最厉害的地方：只要有这个压缩包在手，你就可以使用某种技术创建一个“沙盒”，在“沙盒”中解压这个压缩包，然后就可以运行你的程序了。

   更重要的是，这个压缩包包含了完整的操作系统文件和目录，也就是包含了这个应用运行所需要的所有依赖，所以你可以先用这个压缩包在本地进行开发和测试，完成之后，再把这个压缩包上传到云端运行。在这个过程中，你完全不需要进行任何配置或者修改，因为这个压缩包赋予了你一种极其宝贵的能力：本地环境和云端环境的高度一致！

这，正是 Docker 镜像的精髓。

## 1.2 Docker为什么会火？

   解决了应用打包这个根本性的问题，同开发者与生俱来的的亲密关系，再加上 PaaS 概念已经深入人心的完美契机，成为 Docker 这个技术上看似平淡无奇的项目一举走红的重要原因。

   2013~2014 年，以 Cloud Foundry 为代表的 PaaS 项目，逐渐完成了教育用户和开拓市场的艰巨任务，也正是在这个将概念逐渐落地的过程中，应用“打包”困难这个问题，成了整个后端技术圈子的一块心病。Docker 项目的出现，则为这个根本性的问题提供了一个近乎完美的解决方案。这正是 Docker 项目刚刚开源不久，就能够带领一家原本默默无闻的 PaaS 创业公司脱颖而出，然后迅速占领了所有云计算领域头条的技术原因。而在成为了基础设施领域近十年难得一见的技术明星之后，dotCloud 公司则在 2013 年底大胆改名为 Docker 公司。

## 二、Docker 安装

## 三、 Docker 常用命令

## 四、Docker 镜像讲解

## 五、容器数据卷

### 5.1 容器隔离原理

    对于进程来说，它的**静态表现**就是程序，平常都安安静静地待在磁盘上；而一旦运行起来，它就变成了计算机里的数据和状态的总和，这就是它的**动态表现**；

**容器技术的核心功能**，就是通过约束和修改进程的动态表现，从而为其创造出一个“边界”。

**容器，其实是一种特殊的进程+文件系统。**

#### 5.1.1 一种特殊的进程

  `Linux Cgroups( Linux Control Group)` 技术是用来制造约束的主要手段，就是**限制一个进程组能够使用的资源上限**，包括 CPU、内存、磁盘、网络带宽等等(简单粗暴地理解呢，它就是一个子系统目录加上一组资源限制文件的组合);

   `Namespace（PID\Mount\Network）`技术则是用来**修改进程视图的主要方法**，实现对程序运行环境的隔离；**`rootfs` 做文件系统（即 Docker 容器镜像）**。

> **举例**：PID 的 namespace 进行进程隔离为例：

  在 Linux 系统中创建线程的系统调用是 `clone()`。当调用 `clone()` 系统调用创建一个新进程时，就可以在参数中指定`CLONE_NEWPID`参数。比如：

```c
    int pid = clone(main_function, stack_size, SIGCHLD, NULL);
    int pid = clone(main_function, stack_size, CLONE_NEWPID | SIGCHLD, NULL);
```

  **进程隔离**：*新创建的容器，类似新创建一个进程*，在这个进程将会“看到”一个全新的进程空间，它的PID 是 1。

```sh
    $ docker run -it busybox /bin/sh
    # ps
    PID  USER   TIME COMMAND
    1 root   0:00 /bin/sh
    10 root   0:00 ps
```
  
除了这里用到的 `PID Namespace`，Linux 操作系统还提供了 `Mount、UTS、IPC、Network` 和 `User`这些 `Namespace`，用来对各种不同的进程上下文进行“障眼法”操作。

  `Linux Cgroups` 的设计还是比较易用的，简单粗暴地理解呢，它就是一个子系统目录加上一组资源限制文件的组合。而对于 `Docker` 等 `Linux` 容器项目来说，它们只需要在每个子系统下面，为每个容器创建一个控制组（即创建一个新目录），然后在启动容器进程之后，把这个进程的 `PID` 填写到对应控制组的 `tasks` 文件中就可以了。

#### 5.1.2 文件系统

   用来为**容器进程提供隔离后执行环境的文件系统**，就是所谓的“容器镜像”。它还有一个更为专业的名字，叫作：**rootfs（根文件系统）**。`rootfs` 只是一个操作系统所包含的文件、配置和目录，并不包括操作系统内核(内核由谁提供?)。

   **容器一致性的体现**：由于 `rootfs` 里打包的不只是应用，而是**整个操作系统的文件和目录**，也就意味着，应用以及它运行所需要的所有依赖，都被封装在了一起。

  **联合文件系统技术(`Union File System`,`UnionFS`)**，实现镜像分层的功能，其核心功能是*将多个不同位置的目录联合挂载（union mount）到同一个目录下*。

## 六、Docker File

### 6.1 基本结构

### 6.2 指令

### 6.3 创建镜像

****

## 七、 Docker 网络

安装 Docker 以后会默认创建三种网络，可以通过 `docker network ls` 查看。

```sh
[root@localhost ~]# docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
688d1970f72e        bridge              bridge              local
885da101da7d        host                host                local
f4f1b3cf1b7f        none                null                local
```

**Docker 网络模式：**

Docker网络模式 | 配置 | 说明
---------|----------|---------
 host模式 | –net=host | 容器和宿主机共享Network namespace，容器将不会虚拟出自己的网卡，配置自己的 IP 等，而是使用宿主机的 IP 和端口。
 container模式 | –net=container:NAME_or_ID | 新创建的容器不会创建自己的网卡和配置自己的 IP，而是和一个指定的容器共享 IP、端口范围等。 kubernetes中的pod就是多个容器共享一个Network namespace。
 none模式 | –net=none | 容器有独立的Network namespace，但并没有对其进行任何网络设置，如分配veth pair 和网桥连接，配置IP等。
 bridge模式 | –net=bridge  | 为每一个容器分配、设置 IP 等，并将容器连接到一个 docker0 虚拟网桥，默认为该模式。

### 7.1 容器网络理论

容器网络实质上是由 Dokcer 为应用程序所创造的虚拟环境的一部分，它能让应用从宿主机操作系统的网络环境中独立出来，形成容器自有的网络设备、IP 协议栈、端口套接字、IP 路由表、防火墙等等与网络相关的模块。

Docker 为实现容器网络，主要采用的架构由三部分组成：**CNM、Libnetwork 和驱动**。

CNM 就是一个设计文档，指导你怎么去实现容器网络，而 Libnetwork 和驱动则是其具体实现，从而确保容器网络的通信。

#### 7.1.1 CNM

Docker 网络架构采用的**设计规范是 CNM**（`Container Network Model`）：CNM 中规定了 Docker 网络的基础组成要素：**Sandbox、Endpoint、Network**。如图所示：

![](https://ask.qcloudimg.com/http-save/yehe-7158674/4abelkv4oi.jpeg)

- `Sandbox`，提供了容器的虚拟网络栈，也即端口套接字、IP 路由表、防火墙、DNS 配置等内容。主要**用于隔离容器网络与宿主机网络**，形成了完全独立的容器网络环境。
- `Network`，Docker 内部的虚拟子网，网络内的参与者相互可见并能够进行通讯。Docker 的虚拟网路和宿主机网络是存在隔离关系的，其目的主要是形成容器间的安全通讯环境。
- `Endpoint`，就是虚拟网络的接口，就像普通网络接口一样，**Endpoint 的主要职责是负责创建连接**。在 CNM 中，终端负责将沙盒连接到网络。Endpoint 与常见的网络适配器类似，也就意味着 Endpoint 只能接入某一个网络。因此，如果容器需要接入到多个网络，就需要多个 Endpoint。

注💡：如上图所示（我们将图中的三个容器从左到右依次标记为 1、2、3），那么容器 2 有两个 endpoint 并且分别接入 NetworkdA 和 NetworkB。那么容器 1 和容器 2 是可以实现通信的，因为都接入了 NetworkA。但是容器 3 和容器 1，以及容器 2 的两个 Endpoint 之间是不能通信的，除非有三层路由器的支持。

#### 7.1.2 Libnetwork

**`Libnetwork` 是 CNM 的标准实现**。

Libnetwork 是[开源库](https://github.com/moby/libnetwork/tree/master)，采用 Go 语言编写（跨平台的），也是 Docker 所使用的库，Docker 网络架构的核心代码都在这个库中。Libnetwork 实现了 CNM 中定义的全部三个组件，此外它还实现了本地服务发现、基于 Ingress 的容器负载均衡，以及网络控制层和管理层功能。

#### 7.1.3 驱动

如果说 **`Libnetwork` 实现了控制层和管理层功能**，那么**驱动就负责实现数据层**。比如网络的连通性和隔离性是由驱动来处理的。驱动通过实现特定网络类型的方式扩展了 Docker 网络栈，例如桥接网络和覆盖网络。

`Docker` 内置了若干驱动，通常被称作原生驱动或者本地驱动。比如 `Bridge Driver、Host Driver、Overlay Driver、MacLan Driver、None Driver` 等等。第三方也可以编写 Docker 网络驱动，这些驱动被叫做远程驱动，例如 `Calico、Contiv、Kuryr` 以及 `Weave` 等。**每个驱动负责创建其上所有网络资源的创建和管理。**

其中 `Bridge` 和 `Overlay` 在开发过程中使用频率较高。

- `Bridge`：Docker 容器的默认网络驱动，通过网桥来实现网络通讯。
- `Overlay`，借助 Docker 集群模块 Docker Swarm 搭建的**跨 Docker Daemon 网络**。通过它**可以搭建跨物理网络主机的虚拟网络**，进而让不同物理机中运行的容器感知不到多个物理机的存在。

![](https://ask.qcloudimg.com/http-save/yehe-7158674/wm6xlgs8qx.png)

在 Docker 安装时，会自动安装一块 Docker 网卡称为 `docker0`(容器网桥)，用于 Docker 各容器及宿主机的网络通信。

Container-IP：Docker 启动一个容器时会根据 Docker 网桥的网段分配给容器一个 IP 地址，称为 Container-IP

Docker网桥（Docker0）是每个容器的默认网关。因为在同一宿主机内的容器都接入同一个网桥，这样容器之间就能够通过容器的 Container-IP 直接通信。

```sh
docker0   Link encap:Ethernet  HWaddr 02:42:be:6b:61:dc
          inet addr:172.17.0.1  Bcast:172.17.255.255  Mask:255.255.0.0
          inet6 addr: fe80::42:beff:fe6b:61dc/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:332 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:0 (0.0 B)  TX bytes:30787 (30.7 KB)
```

### 7.2 Docker 网络模式

#### 7.2.1 host 模式

  容器不会获得一个独立的Network Namespace，而是和宿主机共用一个Network Namespace。容器将不会虚拟出自己的网卡，配置自己的IP等，而是使用宿主机的IP和端口。但是，容器的其他方面，如文件系统、进程列表等还是和宿主机隔离的。

  使用host模式的容器可以直接使用宿主机的IP地址与外界通信，容器内部的服务端口也可以使用宿主机的端口，不需要进行NAT，host最大的优势就是网络性能比较好，但是docker host上已经使用的端口就不能再用了，网络的隔离性不好。

#### 7.2.2 container模式

  这个模式指定新创建的容器和已经存在的一个容器共享一个 Network Namespace，而不是和宿主机共享。新创建的容器不会创建自己的网卡，配置自己的 IP，而是和一个指定的容器共享 IP、端口范围等。同样，两个容器除了网络方面，其他的如文件系统、进程列表等还是隔离的。两个容器的进程可以通过 lo 网卡设备通信。

#### 7.2.3 none 模式

  使用none模式，Docker容器拥有自己的Network Namespace，但是，并不为Docker容器进行任何网络配置。也就是说，这个Docker容器没有网卡、IP、路由等信息。需要我们自己为Docker容器添加网卡、配置IP等。

  这种网络模式下容器只有lo回环网络，没有其他网卡。none模式可以在容器创建时通过–network=none来指定。这种类型的网络没有办法联网，封闭的网络能很好的保证容器的安全性。

#### 7.2.4 bridge模式

  当Docker进程启动时，会在主机上创建一个名为docker0的虚拟网桥，此主机上启动的Docker容器会连接到这个虚拟网桥上。虚拟网桥的工作方式和物理交换机类似，这样主机上的所有容器就通过交换机连在了一个二层网络中。

  从docker0子网中分配一个IP给容器使用，并设置docker0的IP地址为容器的默认网关。在主机上创建一对虚拟网卡veth pair设备，Docker将veth pair设备的一端放在新创建的容器中，并命名为eth0（容器的网卡），另一端放在主机中，以vethxxx这样类似的名字命名，并将这个网络设备加入到docker0网桥中。可以通过brctl show命令查看。

  bridge模式是docker的默认网络模式，不写–net参数，就是bridge模式。使用docker run -p时，docker实际是在iptables做了DNAT规则，实现端口转发功能。可以使用iptables -t nat -vnL查看。

### 7.3 使用网络

#### 7.3.1 外部访问容器

#### 7.3.2 容器互联

### 7.4 高级网络配置

****

## 八、

****

## 巨人的肩膀

[Docker-从入门到实践](https://yeasy.gitbook.io/docker_practice)
[docker.doc-en](https://docs.docker.com/reference/dockerfile/)
[docker.doc-cn](http://www.dockerinfo.net/dockerfile%E4%BB%8B%E7%BB%8D)

