# Docker

## 一、Docker 简介

### 1.1 什么是Docker

**Docker** 使用 `Google` 公司推出的 [Go 语言](https://golang.google.cn/) 进行开发实现，基于 `Linux` 内核的 [cgroup](https://zh.wikipedia.org/wiki/Cgroups)，[namespace](https://en.wikipedia.org/wiki/Linux_namespaces)，以及 [OverlayFS](https://docs.docker.com/storage/storagedriver/overlayfs-driver/) 类的 [Union FS](https://en.wikipedia.org/wiki/Union_mount) 等技术，**对进程进行封装隔离**，属于 [操作系统层面的虚拟化技术](https://en.wikipedia.org/wiki/Operating-system-level_virtualization)。由于隔离的进程独立于宿主和其它的隔离的进程，因此也称其为容器。

最初实现是基于 [LXC](https://linuxcontainers.org/lxc/introduction/)，从 `0.7` 版本以后开始去除 `LXC`，转而使用自行开发的 [libcontainer](https://github.com/docker/libcontainer)，从 `1.11` 版本开始，则进一步演进为使用 [runC](https://github.com/opencontainers/runc) 和 [containerd](https://github.com/containerd/containerd)。

![Docker 架构](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/media/docker-on-linux.png)

> `runc` 是一个 Linux 命令行工具，用于根据 [OCI容器运行时规范](https://github.com/opencontainers/runtime-spec) 创建和运行容器。

> `containerd` 是一个守护程序，它管理容器生命周期，提供了在一个节点上执行容器和管理镜像的最小功能集。

**Docker** 在容器的基础上，进行了进一步的封装，从文件系统、网络互联到进程隔离等等，极大的简化了容器的创建和维护。使得 `Docker` 技术比虚拟机技术更为轻便、快捷。

 **Docker** 和传统虚拟化方式的不同之处在于：

- 传统虚拟机技术是虚拟出一套硬件后，在其上运行一个完整操作系统，在该系统上再运行所需应用进程；
- 而容器内的应用进程直接运行于宿主的内核，容器内没有自己的内核，而且也没有进行硬件虚拟。因此容器要比传统虚拟机更为轻便。

![传统虚拟化 VS Docker](https://pdai.tech/images/devops/docker/docker-y-0.jpg)

[docker-soft]:https://en.wikipedia.org/wiki/Docker_(software)

### 1.2  为什么要使用Docker

作为一种新兴的虚拟化方式，`Docker` 跟传统的虚拟化方式相比具有众多的优势。

- **更高效的利用系统资源**: 由于容器不需要进行硬件虚拟以及运行完整操作系统等额外开销，`Docker` 对系统资源的利用率更高。无论是应用执行速度、内存损耗或者文件存储速度，都要比传统虚拟机技术更高效。因此，相比虚拟机技术，一个相同配置的主机，往往可以运行更多数量的应用。

- **更快速的启动时间**:传统的虚拟机技术启动应用服务往往需要数分钟，而 `Docker` 容器应用，由于直接运行于宿主内核，无需启动完整的操作系统，因此可以做到秒级、甚至毫秒级的启动时间。大大的节约了开发、测试、部署的时间。
- **一致的运行环境**：开发过程中一个常见的问题是环境一致性问题。由于开发环境、测试环境、生产环境不一致，导致有些 bug 并未在开发过程中被发现。而 `Docker` 的镜像提供了除内核外完整的运行时环境，确保了应用运行环境一致性，从而不会再出现 *「这段代码在我机器上没问题啊」* 这类问题。
- **持续交付和部署**：对开发和运维（[DevOps](https://zh.wikipedia.org/wiki/DevOps)）人员来说，最希望的就是一次创建或配置，可以在任意地方正常运行。
  - 使用 `Docker` 可以通过定制应用镜像来实现持续集成、持续交付、部署。
  - 开发人员可以通过 [Dockerfile](../image/dockerfile/) 来进行镜像构建，并结合 [持续集成(Continuous Integration)](https://en.wikipedia.org/wiki/Continuous_integration) 系统进行集成测试，
  - 运维人员则可以直接在生产环境中快速部署该镜像，甚至结合 [持续部署(Continuous Delivery/Deployment)](https://en.wikipedia.org/wiki/Continuous_delivery) 系统进行自动部署。
  - 使用 [`Dockerfile`](../image/build.md) 使镜像构建透明化，不仅仅开发团队可以理解应用运行环境，也方便运维团队理解应用运行所需条件，帮助更好的生产环境中部署该镜像。

- **更轻松的迁移：**由于 `Docker` 确保了执行环境的一致性，使得应用的迁移更加容易。`Docker` 可以在很多平台上运行，无论是物理机、虚拟机、公有云、私有云，甚至是笔记本，其运行结果是一致的。因此用户可以很轻易的将在一个平台上运行的应用，迁移到另一个平台上，而不用担心运行环境的变化导致应用无法正常运行的情况。
- **更轻松的维护和扩展：**Docker` 使用的分层存储以及镜像的技术，使得应用重复部分的复用更为容易，也使得应用的维护更新更加简单，基于基础镜像进一步扩展镜像也变得非常简单。此外，`Docker` 团队同各个开源项目团队一起维护了一大批高质量的 [官方镜像](https://hub.docker.com/search/?type=image&image_filter=official)，既可以直接在生产环境使用，又可以作为基础进一步定制，大大的降低了应用服务的镜像制作成本。

#### 对比传统虚拟机总结

| 特性       | 容器               | 虚拟机      |
| :--------- | :----------------- | :---------- |
| 启动       | 秒级               | 分钟级      |
| 硬盘使用   | 一般为 `MB`        | 一般为 `GB` |
| 性能       | 接近原生           | 弱于        |
| 系统支持量 | 单机支持上千个容器 | 一般几十个  |

## 二、Docker 三大组件

### 2.1 仓库、镜像、容器的关系

![](https://pdai.tech/images/devops/docker/docker-architecture.svg)

### 2.1 镜像

#### 镜像

操作系统分为 **内核** 和 **用户空间**。对于 `Linux` 而言，内核启动后，会挂载 `root` 文件系统为其提供用户空间支持。而 **Docker 镜像**（`Image`），就相当于是一个 `root` 文件系统。比如官方镜像 `ubuntu:18.04` 就包含了完整的一套 Ubuntu 18.04 最小系统的 `root` 文件系统。

**Docker 镜像** 是一个特殊的文件系统，除了**提供容器运行时所需的程序、库、资源、配置等文件**外，还**包含了一些为运行时准备的一些配置参数**（如匿名卷、环境变量、用户等）。镜像 **不包含** 任何动态数据，其内容在构建之后也不会被改变。

#### 分层存储

因为镜像包含操作系统完整的 `root` 文件系统，其体积往往是庞大的，因此在 Docker 设计时，就充分**利用 [Union FS](https://en.wikipedia.org/wiki/Union_mount) 的技术**，将其设计为分层存储的架构。

因此严格来说，镜像并非是像一个 `ISO` 那样的打包文件，镜像只是一个虚拟的概念，其实际体现并非由一个文件组成，而是由一组文件系统组成，或者说，由多层文件系统联合组成。

**镜像构建时，会一层层构建，前一层是后一层的基础**。每一层构建完就不会再发生改变，后一层上的任何改变只发生在自己这一层。比如，删除前一层文件的操作，实际不是真的删除前一层的文件，而是仅在当前层标记为该文件已删除。在最终容器运行的时候，虽然不会看到这个文件，但是实际上该文件会一直跟随镜像。因此，在构建镜像的时候，需要额外小心，每一层尽量只包含该层需要添加的东西，任何额外的东西应该在该层构建结束前清理掉。

分层存储的特征还使得镜像的复用、定制变的更为容易。甚至可以用之前构建好的镜像作为基础层，然后进一步添加新的层，以定制自己所需的内容，构建新的镜像。

### 2.2 容器

**镜像（`Image`）**和**容器（`Container`）**的关系，就像是面向对象程序设计中的 `类` 和 `实例` 一样，**镜像是静态的定义（类），容器是镜像运行时的实体（实例）**。容器可以被创建、启动、停止、删除、暂停等。

**容器的实质是进程**，但与直接在宿主执行的进程不同，容器进程运行于属于自己的独立的 [命名空间](https://en.wikipedia.org/wiki/Linux_namespaces)。因此容器可以拥有自己的 `root` 文件系统、网络配置、进程空间，用户 ID 空间。容器内的进程是运行在一个隔离的环境里，使用起来，就好像是在一个独立于宿主的系统下操作一样。这种特性使得容器封装的应用比直接在宿主运行更加安全。也因为这种隔离的特性，很多人初学 Docker 时常常会混淆容器和虚拟机。

镜像使用的是分层存储，容器也是如此。每一个容器运行时，**以镜像为基础层，在其上创建一个当前容器的存储层**，我们可以称这个为容器运行时读写而准备的存储层为 **容器存储层**。

![容器组成](https://preview.cloud.189.cn/image/imageAction?param=0F3BFE5B08FC09DFF6428BFE564977C16146D27D447654A4FD8F6926DB51C7F4BDC5C797A36B3ADF42174372415D1830BB4C99397347E44340CB5937CBF3F3332DB62C605337C0701B7180E848FE658BD31C3B3D7374354966BFAED076D987422B25C48F1C903988E80A25AB12A628A5)

**容器存储层的生存周期和容器一样，容器消亡时，容器存储层也随之消亡**。因此，任何保存于容器存储层的信息都会随容器删除而丢失。

按照 Docker 最佳实践的要求，容器不应该向其存储层内写入任何数据，容器存储层要保持无状态化。所有的文件写入操作，都应该使用 **数据卷（Volume）**、或者 绑定宿主目录，在这些位置的读写会跳过容器存储层，直接对宿主（或网络存储）发生读写，其性能和稳定性更高。

数据卷的生存周期独立于容器，容器消亡，数据卷不会消亡。因此，使用数据卷后，容器删除或者重新运行之后，数据却不会丢失。

### 2.3 仓库

镜像构建完成后，可以很容易的在当前宿主机上运行，但是，如果需要在其它服务器上使用这个镜像，我们就需要一个集中的存储、分发镜像的服务，[Docker Registry](https://yeasy.gitbook.io/docker_practice/repository/registry) 就是这样的服务。

一个 **Docker Registry** 中可以包含多个 **仓库**（`Repository`）；每个仓库可以包含多个 **标签**（`Tag`）；每个标签对应一个镜像。

通常，一个仓库会包含同一个软件不同版本的镜像，而标签就常用于对应该软件的各个版本。我们可以通过 `<仓库名>:<标签>` 的格式来指定具体是这个软件哪个版本的镜像。如果不给出标签，将以 `latest` 作为默认标签。

以 [Ubuntu 镜像](https://hub.docker.com/_/ubuntu) 为例，`ubuntu` 是仓库的名字，其内包含有不同的版本标签，如，`16.04`, `18.04`。我们可以通过 `ubuntu:16.04`，或者 `ubuntu:18.04` 来具体指定所需哪个版本的镜像。如果忽略了标签，比如 `ubuntu`，那将视为 `ubuntu:latest`。

**仓库名经常以 *两段式路径* 形式出现**，比如 `jwilder/nginx-proxy`，前者往往意味着 Docker Registry 多用户环境下的用户名，后者则往往是对应的软件名。但这并非绝对，取决于所使用的具体 Docker Registry 的软件或服务。

#### **Docker Registry 公开服务**

Docker Registry 公开服务是开放给用户使用、允许用户管理镜像的 Registry 服务。一般这类公开服务允许用户免费上传、下载公开的镜像，并可能提供收费服务供用户管理私有镜像。

最常使用的 Registry 公开服务是官方的 [Docker Hub](https://hub.docker.com/)，这也是默认的 Registry，并拥有大量的高质量的 [官方镜像](https://hub.docker.com/search?q=&type=image&image_filter=official)。除此以外，还有 Red Hat 的 [Quay.io](https://quay.io/repository/)；Google 的 [Google Container Registry](https://cloud.google.com/container-registry/)，[Kubernetes](https://kubernetes.io/) 的镜像使用的就是这个服务；代码托管平台 [GitHub](https://github.com/) 推出的 [ghcr.io](https://docs.github.com/cn/packages/working-with-a-github-packages-registry/working-with-the-container-registry)。

由于某些原因，在国内访问这些服务可能会比较慢。国内的一些云服务商提供了针对 Docker Hub 的镜像服务（`Registry Mirror`），这些镜像服务被称为 **加速器**。常见的有 [阿里云加速器](https://www.aliyun.com/product/acr?source=5176.11533457&userCode=8lx5zmtu)、[DaoCloud 加速器](https://www.daocloud.io/mirror#accelerator-doc) 等。使用加速器会直接从国内的地址下载 Docker Hub 的镜像，比直接从 Docker Hub 下载速度会提高很多。在 [安装 Docker](https://yeasy.gitbook.io/docker_practice/install/mirror) 一节中有详细的配置方法。

国内也有一些云服务商提供类似于 Docker Hub 的公开服务。比如 [网易云镜像服务](https://c.163.com/hub#/m/library/)、[DaoCloud 镜像市场](https://hub.daocloud.io/)、[阿里云镜像库](https://www.aliyun.com/product/acr?source=5176.11533457&userCode=8lx5zmtu) 等。

#### 私有 Docker Registry

除了使用公开服务外，用户还可以在本地搭建私有 Docker Registry。Docker 官方提供了 [Docker Registry](https://hub.docker.com/_/registry/) 镜像，可以直接使用做为私有 Registry 服务。在 **私有仓库** 一节中，会有进一步的搭建私有 Registry 服务的讲解。

开源的 Docker Registry 镜像只提供了 [Docker Registry API](https://docs.docker.com/registry/spec/api/) 的服务端实现，足以支持 `docker` 命令，不影响使用。但不包含图形界面，以及镜像维护、用户管理、访问控制等高级功能。

除了官方的 Docker Registry 外，还有第三方软件实现了 Docker Registry API，甚至提供了用户界面以及一些高级功能。比如，[Harbor](https://github.com/goharbor/harbor) 和 [Sonatype Nexus](https://yeasy.gitbook.io/docker_practice/repository/nexus3_registry)。

## 三、 Docker 镜像

Docker 运行容器前需要本地存在对应的镜像，如果本地不存在该镜像，Docker 会从镜像仓库下载该镜像。

本章将介绍更多关于镜像的更多操作内容。

### 3.1 镜像列表

使用 `docker images` 来列出本地主机上的镜像

```bash
[root@pdai ~]$ docker image ls
REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
redis                latest              5f515359c7f8        5 days ago          183 MB
nginx                latest              05a60462f8ba        5 days ago          181 MB
mongo                3.2                 fe9198c04d62        5 days ago          342 MB
<none>               <none>              00285df0df87        5 days ago          342 MB
ubuntu               18.04               329ed837d508        3 days ago          63.3MB
ubuntu               bionic              329ed837d508        3 days ago          63.3MB
```

各个选项说明:

- REPOSITORY：表示镜像的仓库源
- TAG：镜像的标签, 同一仓库源可以有多个 TAG，代表这个仓库源的不同个版本
- IMAGE ID：**镜像 ID** 则是镜像的唯一标识，一个镜像可以对应多个 **标签**。在上面的例子中，可以看到 `ubuntu:18.04` 和 `ubuntu:bionic` 拥有相同的 ID，因为它们对应的是同一个镜像。
- CREATED：镜像创建时间
- SIZE：镜像大小

##### 镜像体积

 使用`docker system df` 命令来便捷的查看镜像、容器、数据卷所占用的空间。

```sh
% docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          14        12        2.296GB   1.25GB (54%)
Containers      15        14        693.3MB   693MB (99%)
Local Volumes   45        9         5.625GB   4.731GB (84%)
Build Cache     87        0         848.5MB   848.5MB

```

- `docker image ls` 显示的是镜像下载到本地后，展开的大小，准确说，是展开后的各层所占空间的总和，因为镜像到本地后，查看空间的时候，更关心的是本地磁盘空间占用的大小。
- Docker Hub 中显示的体积是压缩后的体积。镜像下载和上传过程中镜像是保持着压缩状态。因此本地标识的所占用空间和在 Docker Hub 上看到的镜像大小不同。比如，`ubuntu:18.04` 镜像大小，在这里是 `63.3MB`，但是在 [Docker Hub](https://hub.docker.com/layers/ubuntu/library/ubuntu/bionic/images/sha256-32776cc92b5810ce72e77aca1d949de1f348e1d281d3f00ebcc22a3adcdc9f42?context=explore) 显示的却是 `25.47 MB`。
- `docker image ls` 列表中的镜像体积总和并非是所有镜像实际硬盘消耗。由于 Docker 镜像是多层存储结构，并且可以继承、复用，因此不同镜像可能会因为使用相同的基础镜像，从而拥有共同的层。由于 Docker 使用 Union FS，相同的层只需要保存一份即可，因此实际镜像硬盘占用空间很可能要比这个列表镜像大小的总和要小的多。因此可以通过 `docker system df` 命令来便捷的查看镜像、容器、数据卷所占用的空间。

##### 虚悬镜像

在镜像列表中，还可能存在一个特殊的镜像，这个镜像既没有仓库名，也没有标签，均为 `<none>`。这个镜像原本是有镜像名和标签的，原来为 `mongo:3.2`，随着官方镜像维护，发布了新版本后，重新 `docker pull mongo:3.2` 时，`mongo:3.2` 这个镜像名被转移到了新下载的镜像身上，而旧的镜像上的这个名称则被取消，从而成为了 `<none>`。除了 `docker pull` 可能导致这种情况，`docker build` 也同样可以导致这种现象。

由于新旧镜像同名，旧镜像名称被取消，从而出现仓库名、标签均为 `<none>` 的镜像。这类无标签镜像也被称为 **虚悬镜像(dangling image)** ，可以用下面的命令专门显示这类镜像：

```
$ docker image ls -f dangling=true
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
<none>              <none>              00285df0df87        5 days ago          342 MB
```

一般来说，虚悬镜像已经失去了存在的价值，是可以随意删除的，可以用下面的命令删除。

```
$ docker image prune
```

##### 中间层镜像

为了加速镜像构建、重复利用资源，Docker 会利用 **中间层镜像**。所以在使用一段时间后，可能会看到一些依赖的中间层镜像。

默认的 `docker image ls` 列表中只会显示顶层镜像，如果希望显示包括中间层镜像在内的所有镜像的话，需要加 `-a` 参数。

```
$ docker image ls -a
```

与之前的虚悬镜像不同，这些无标签的镜像很多都是中间层镜像，是其它镜像所依赖的镜像。这些无标签镜像不应该删除，否则会导致上层镜像因为依赖丢失而出错。实际上，这些镜像也没必要删除，因为之前说过，相同的层只会存一遍，而这些镜像是别的镜像的依赖，因此并不会因为它们被列出来而多存了一份。当删除那些依赖中间层镜像的镜像后，这些依赖的中间层镜像也会被连带删除。

##### 列出部分镜像

不加任何参数的情况下，`docker image ls` 会列出所有顶层镜像，但是有时候我们只希望列出部分镜像。`docker image ls` 有好几个参数可以帮助做到这个事情。

根据仓库名列出镜像

```sh
$ docker image ls ubuntu
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              18.04               329ed837d508        3 days ago          63.3MB
ubuntu              bionic              329ed837d508        3 days ago          63.3MB
```

列出特定的某个镜像，也就是说指定仓库名和标签

```sh
$ docker image ls ubuntu:18.04
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              18.04               329ed837d508        3 days ago          63.3MB
```

除此以外，`docker image ls` 还支持强大的过滤器参数 `--filter`，或者简写 `-f`。之前我们已经看到了使用过滤器来列出虚悬镜像的用法，它还有更多的用法。比如，我们希望看到在 `mongo:3.2` 之后建立的镜像，可以用下面的命令：

```sh
$ docker image ls -f since=mongo:3.2
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
redis               latest              5f515359c7f8        5 days ago          183 MB
nginx               latest              05a60462f8ba        5 days ago          181 MB
```

想查看某个位置之前的镜像也可以，只需要把 `since` 换成 `before` 即可。

如果镜像构建时，定义了 `LABEL`，还可以通过 `LABEL` 来过滤。

```
$ docker image ls -f label=com.example.version=0.1
...
```

##### 以特定格式显示

默认情况下，`docker image ls` 会输出一个完整的表格，但是我们并非所有时候都会需要这些内容。比如，刚才删除虚悬镜像的时候，我们需要利用 `docker image ls` 把所有的虚悬镜像的 ID 列出来，然后才可以交给 `docker image rm` 命令作为参数来删除指定的这些镜像，这个时候就用到了 `-q` 参数。

```sh
$ docker image ls -q
5f515359c7f8
05a60462f8ba
fe9198c04d62
00285df0df87
329ed837d508
329ed837d508
```

`--filter` 配合 `-q` 产生出指定范围的 ID 列表，然后送给另一个 `docker` 命令作为参数，从而针对这组实体成批的进行某种操作的做法在 Docker 命令行使用过程中非常常见，不仅仅是镜像，将来我们会在各个命令中看到这类搭配以完成很强大的功能。因此每次在文档看到过滤器后，可以多注意一下它们的用法。

另外一些时候，我们可能只是对表格的结构不满意，希望自己组织列；或者不希望有标题，这样方便其它程序解析结果等，这就用到了 [Go 的模板语法](https://gohugo.io/templates/introduction/)。

比如，下面的命令会直接列出镜像结果，并且只包含镜像ID和仓库名：

```
$ docker image ls --format "{{.ID}}: {{.Repository}}"
5f515359c7f8: redis
05a60462f8ba: nginx
fe9198c04d62: mongo
00285df0df87: <none>
329ed837d508: ubuntu
329ed837d508: ubuntu
```

或者打算以表格等距显示，并且有标题行，和默认一样，不过自己定义列：

```
$ docker image ls --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}"
IMAGE ID            REPOSITORY          TAG
5f515359c7f8        redis               latest
05a60462f8ba        nginx               latest
fe9198c04d62        mongo               3.2
00285df0df87        <none>              <none>
329ed837d508        ubuntu              18.04
329ed837d508        ubuntu              bionic
```

### 3.2 查找镜像

- 通过[Docker Hub](https://hub.docker.com/search?q=mysql&type=image) 查找镜像

![img](https://pdai.tech/images/devops/docker/docker-y-1.png)

- **使用 docker search 命令来搜索镜像**

```bash
[root@pdai ~]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
[root@pdai ~]# docker search mysql
NAME                              DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
mysql                             MySQL is a widely used, open-source relation…   9132                [OK]
mariadb                           MariaDB is a community-developed fork of MyS…   3233                [OK]
mysql/mysql-server                Optimized MySQL Server Docker images. Create…   676                                     [OK]
centos/mysql-57-centos7           MySQL 5.7 SQL database server                   68
mysql/mysql-cluster               Experimental MySQL Cluster Docker images. Cr…   62
centurylink/mysql                 Image containing mysql. Optimized to be link…   61                                      [OK]
deitch/mysql-backup               REPLACED! Please use http://hub.docker.com/r…   41                                      [OK]
bitnami/mysql                     Bitnami MySQL Docker Image                      35                                      [OK]
tutum/mysql                       Base docker image to run a MySQL database se…   34
schickling/mysql-backup-s3        Backup MySQL to S3 (supports periodic backup…   29                                      [OK]
prom/mysqld-exporter                                                              26                                      [OK]
linuxserver/mysql                 A Mysql container, brought to you by LinuxSe…   24
centos/mysql-56-centos7           MySQL 5.6 SQL database server                   19
circleci/mysql                    MySQL is a widely used, open-source relation…   18
mysql/mysql-router                MySQL Router provides transparent routing be…   14
arey/mysql-client                 Run a MySQL client from a docker container      13                                      [OK]
databack/mysql-backup             Back up mysql databases to... anywhere!         10
openshift/mysql-55-centos7        DEPRECATED: A Centos7 based MySQL v5.5 image…   6
fradelg/mysql-cron-backup         MySQL/MariaDB database backup using cron tas…   5                                       [OK]
genschsa/mysql-employees          MySQL Employee Sample Database                  4                                       [OK]
devilbox/mysql                    Retagged MySQL, MariaDB and PerconaDB offici…   2
ansibleplaybookbundle/mysql-apb   An APB which deploys RHSCL MySQL                2                                       [OK]
jelastic/mysql                    An image of the MySQL database server mainta…   1
monasca/mysql-init                A minimal decoupled init container for mysql    0
widdpim/mysql-client              Dockerized MySQL Client (5.7) including Curl…   0                                       [OK]
```

- NAME: 镜像仓库源的名称
- DESCRIPTION: 镜像的描述
- OFFICIAL: 是否 docker 官方发布
- STARS: 类似 Github 里面的 star，表示点赞、喜欢的意思。
- AUTOMATED: 自动构建。

### 3.3 拉取镜像

[Docker Hub](https://hub.docker.com/search?q=&type=image) 上有大量的高质量的镜像可以用，这里我们就说一下怎么获取这些镜像。

从 Docker 镜像仓库获取镜像的命令是 `docker pull`。其命令格式为：

```sh
$ docker pull [选项] [Docker Registry 地址[:端口号]/]仓库名[:标签]
# 具体的选项可以通过 `docker pull --help` 命令看到
```

- Docker 镜像仓库地址：地址的格式一般是 `<域名/IP>[:端口号]`。默认地址是  `Docker Hub(docker.io)`。
- 仓库名：如之前所说，这里的仓库名是两段式名称，即 `<用户名>/<软件名>`。对于 Docker Hub，如果不给出用户名，则默认为 `library`，也就是官方镜像。

比如：

```
$ docker pull ubuntu:18.04
18.04: Pulling from library/ubuntu
92dc2a97ff99: Pull complete
be13a9d27eb8: Pull complete
c8299583700a: Pull complete
Digest: sha256:4bc3ae6596938cb0d9e5ac51a1152ec9dcac2a1c50829c74abd9c4361e321b26
Status: Downloaded newer image for ubuntu:18.04
docker.io/library/ubuntu:18.04
```

上面的命令中没有给出 Docker 镜像仓库地址，因此将会从 Docker Hub （`docker.io`）获取镜像。而镜像名称是 `ubuntu:18.04`，因此将会获取官方镜像 `library/ubuntu` 仓库中标签为 `18.04` 的镜像。`docker pull` 命令的输出结果最后一行给出了镜像的完整名称，即： `docker.io/library/ubuntu:18.04`。

从下载过程中可以看到我们之前提及的分层存储的概念，镜像是由多层存储所构成。下载也是一层层的去下载，并非单一文件。下载过程中给出了每一层的 ID 的前 12 位。并且下载结束后，给出该镜像完整的 `sha256` 的摘要，以确保下载一致性。

### 3.4 删除镜像

可以使用 `docker image rm` 命令，删除本地的镜像：

```
$ docker image rm [选项] <镜像1> [<镜像2> ...]
```

注意是否存在 container 实例或者是镜像依赖。

##### 用 ID、镜像名、摘要删除镜像

上述命令中`<镜像>` 可以是 `镜像短 ID`、`镜像长 ID`、`镜像名` 或者 `镜像摘要`。

假如存在如下镜像：

```
$ docker image ls
REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
centos                      latest              0584b3d2cf6d        3 weeks ago         196.5 MB
redis                       alpine              501ad78535f0        3 weeks ago         21.03 MB
docker                      latest              cf693ec9b5c7        3 weeks ago         105.1 MB
nginx                       latest              e43d811ce2f4        5 weeks ago         181.5 MB
```

可以用镜像的完整 ID，也称为 `长 ID`，来删除镜像。使用脚本的时候可能会用长 ID，但是人工输入就太累了，所以更多的时候是用 `短 ID` 来删除镜像

- 使用短 ID 删除镜像。`docker image ls` 默认列出的就已经是短 ID 了，一般取前3个字符以上，只要足够区分于别的镜像就可以了。如果我们要删除 `redis:alpine` 镜像，可以执行：

```sh
$ docker image rm 501
Untagged: redis:alpine
Untagged: redis@sha256:f1ed3708f538b537eb9c2a7dd50dc90a706f7debd7e1196c9264edeea521a86d
Deleted: sha256:501ad78535f015d88872e13fa87a828425117e3d28075d0c117932b05bf189b7
Deleted: sha256:96167737e29ca8e9d74982ef2a0dda76ed7b430da55e321c071f0dbff8c2899b
Deleted: sha256:32770d1dcf835f192cafd6b9263b7b597a1778a403a109e2cc2ee866f74adf23
Deleted: sha256:127227698ad74a5846ff5153475e03439d96d4b1c7f2a449c7a826ef74a2d2fa
Deleted: sha256:1333ecc582459bac54e1437335c0816bc17634e131ea0cc48daa27d32c75eab3
Deleted: sha256:4fc455b921edf9c4aea207c51ab39b10b06540c8b4825ba57b3feed1668fa7c7
```

- 用`镜像名`，也就是 `<仓库名>:<标签>`，来删除镜像。

```sh
$ docker image rm centos
Untagged: centos:latest
Untagged: centos@sha256:b2f9d1c0ff5f87a4743104d099a3d561002ac500db1b9bfa02a783a46e0d366c
Deleted: sha256:0584b3d2cf6d235ee310cf14b54667d889887b838d3f3d3033acd70fc3c48b8a
Deleted: sha256:97ca462ad9eeae25941546209454496e1d66749d53dfa2ee32bf1faabd239d38
```

- 使用 `镜像摘要` 删除镜像。

```sh
$ docker image ls --digests
REPOSITORY                  TAG                 DIGEST                                                                    IMAGE ID            CREATED             SIZE
node                        slim                sha256:b4f0e0bdeb578043c1ea6862f0d40cc4afe32a4a582f3be235a3b164422be228   6e0c4c8e3913        3 weeks ago         214 MB

$ docker image rm node@sha256:b4f0e0bdeb578043c1ea6862f0d40cc4afe32a4a582f3be235a3b164422be228
Untagged: node@sha256:b4f0e0bdeb578043c1ea6862f0d40cc4afe32a4a582f3be235a3b164422be228
```

##### Untagged 和 Deleted

观察上述命令的运行输出信息的话，删除行为分为两类：一类是 `Untagged`，另一类是 `Deleted`。

前面介绍过，镜像的唯一标识是其 ID 和摘要，而一个镜像可以有多个标签。因此当使用上面命令删除镜像的时候，实际上是在**要求删除某个标签的镜像**。所以首先需要做的是将满足我们要求的所有镜像标签都取消，这就是我们看到的 `Untagged` 的信息。因为一个镜像可以对应多个标签，因此当我们删除了所指定的标签后，可能还有别的标签指向了这个镜像，如果是这种情况，那么 `Delete` 行为就不会发生。所以并非所有的 `docker image rm` 都会产生删除镜像的行为，有可能仅仅是取消了某个标签而已。

当该镜像所有的标签都被取消了，该镜像很可能会失去了存在的意义，因此会触发删除行为。

镜像是多层存储结构，因此在删除的时候也是从上层向基础层方向依次进行判断删除。镜像的多层结构让镜像复用变得非常容易，因此很有可能**某个其它镜像正依赖于当前镜像的某一层**。这种情况，依旧不会触发删除该层的行为。直到没有任何层依赖当前层时，才会真实的删除当前层。这就是为什么明明没有别的标签指向这个镜像，但是它还是存在的原因，也是为什么有时候会发现所删除的层数和自己 `docker pull` 看到的层数不一样的原因。

除了镜像依赖以外，还需要注意的是**容器对镜像的依赖**。如果有用这个镜像启动的容器存在（即使容器没有运行），那么同样不可以删除这个镜像。之前讲过，容器是以镜像为基础，再加一层容器存储层，组成这样的多层存储结构去运行的。因此该镜像如果被这个容器所依赖的，那么删除必然会导致故障。如果这些容器是不需要的，应该先将它们删除，然后再来删除镜像。

##### 用 docker image ls 命令来配合

像其它可以承接多个实体的命令一样，可以使用 `docker image ls -q` 来配合使用 `docker image rm`，这样可以成批的删除希望删除的镜像。我们在“镜像列表”章节介绍过很多过滤镜像列表的方式都可以拿过来使用。

需要删除所有仓库名为 `redis` 的镜像：

```sh
$ docker image rm $(docker image ls -q redis)
```

或者删除所有在 `mongo:3.2` 之前的镜像：

```sh
$ docker image rm $(docker image ls -q -f before=mongo:3.2)
```

### 3.4 构建镜像



### 3.5  镜像标签

### 3.6 更新镜像

## 四、容器

### 4.1 容器的生命周期

容器的生命周期是容器可能处于的状态，容器的生命周期分为 7 种。最重要和常见的是除了restarting（重启中）和removing（迁移中）之外的5个状态

- `created`：初建状态
-  restarting：重启状态
- `running`：运行状态
-  removing：迁移状态
- `stopped`：停止状态
- `paused`： 暂停状态
- `deleted`：删除状态

![](https://img-blog.csdnimg.cn/20210323145827177.png)

### 4.2 容器启动

启动容器有两种方式，一种是基于镜像新建一个容器并启动，另外一个是将在终止状态（`exited`）的容器重新启动。

使用 `docker run`新建启动，当利用 `docker run` 来创建容器时，Docker 在后台运行的标准操作包括：

- 检查本地是否存在指定的镜像，不存在就从 [registry](https://yeasy.gitbook.io/docker_practice/repository) 下载
- 利用镜像创建并启动一个容器
- 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
- 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
- 从地址池配置一个 ip 地址给容器
- 执行用户指定的应用程序
- 执行完毕后容器被终止

### 4.3 容器查看

### 4.4 容器再启动

### 4.5 容器停止和重启

### 4.6 后台模式与进入

### 4.7 容器导出和导入

### 4.8 强制停止容器

### 4.9 容器删除

### 4.10 容器别名及操作

### 4.11 容器错误日志



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

Dockerfile 由一行行命令语句组成，并且支持以 `#` 开头的注释行。

Dockerfile 一般分为四部分：

- 基础镜像信息
- 维护者信息
- 镜像操作指令
- 容器启动时执行指令。

> **Example1**

```dockerfile
# This dockerfile uses the ubuntu image
# VERSION 2 - EDITION 1
# Author: docker_user
# Command format: Instruction [arguments / command] ..

# Base image to use, this must be set as the first line
FROM ubuntu

# Maintainer: docker_user <docker_user at email.com> (@docker_user)
MAINTAINER docker_user docker_user@email.com

# Commands to update the image
RUN echo "deb http://archive.ubuntu.com/ubuntu/ raring main universe" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y nginx
RUN echo RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf

# Commands when creating a new container
CMD /usr/sbin/nginx
```

- 开始指明所基于镜像名称
- 接下来知名维护者信息
- 之后是镜像操作指令，例如 `RUN` 指令，`RUN` 指令将对镜像执行跟随的命令。每运行一条 `RUN` 指令，镜像添加新的一层，并提交。
- 最后是 `CMD` 指令，来指定运行容器时的操作命令。

> **Example2**

```dockerfile
# Nginx
#
# VERSION               0.0.1

FROM      ubuntu
MAINTAINER Victor Vieux <victor@docker.com>

RUN apt-get update && apt-get install -y inotify-tools nginx apache2 openssh-server

# Firefox over VNC
#
# VERSION               0.3

FROM ubuntu

# Install vnc, xvfb in order to create a 'fake' display and firefox
RUN apt-get update && apt-get install -y x11vnc xvfb firefox
RUN mkdir /.vnc
# Setup a password
RUN x11vnc -storepasswd 1234 ~/.vnc/passwd
# Autostart firefox (might not be the best way, but it does the trick)
RUN bash -c 'echo "firefox" >> /.bashrc'

EXPOSE 5900
CMD    ["x11vnc", "-forever", "-usepw", "-create"]

# Multiple images example
#
# VERSION               0.1

FROM ubuntu
RUN echo foo > bar
# Will output something like ===> 907ad6c2736f

FROM ubuntu
RUN echo moo > oink
# Will output something like ===> 695d7793cbe4

# You᾿ll now have two images, 907ad6c2736f with /bar, and 695d7793cbe4 with
# /oink.
```

### 6.2 指令

指令的一般格式为 `INSTRUCTION argument`，指令包括 `FROM、MAINTAINER、RUN` 等。

> **FROM**

格式为 `FROM <image>` 或者 `FROM <image>:<tag>`。 

docker tag : 标记本地镜像，将其归入某一仓库。

第一条指令必须为 `FROM` 指令。并且，如果在同一个 Dockerfile 中创建多个镜像时，可以使用多个 `FROM` 指令（每个镜像一次）。

> **MAINTAINER**

格式为 `MAINTAINER <name>`，指定维护者信息。

> **RUN**

格式为 `RUN <command>` 或 `RUN ["executable", "param1", "param2"]`。

前者将在 `shell` 终端中运行命令，即 `/bin/sh -c`；

后者则使用 `exec` 执行。

指定使用其它终端可以通过第二种方式实现，例如 `RUN ["/bin/bash", "-c", "echo hello"]`。

每条 `RUN` 指令将在当前镜像基础上执行指定命令，并提交为新的镜像。当命令较长时可以使用 `\` 来换行。

> **CMD**

`CMD` 支持三种格式

- `CMD ["executable","param1","param2"]` 使用 `exec` 执行，推荐方式；
- `CMD command param1 param2` 在 `/bin/sh` 中执行，提供给需要交互的应用；
- `CMD ["param1","param2"]` 提供给 `ENTRYPOINT` 的默认参数；

指定启动容器时执行的命令，每个 `Dockerfile` 只能有一条 `CMD` 命令。**如果指定了多条命令，只有最后一条会被执行。**

如果用户启动容器时候指定了运行的命令，则会覆盖掉 CMD 指定的命令。

> **EXPOSE**

格式为 `EXPOSE <port> [<port>...]`。

告诉 `Docker` 服务端容器暴露的端口号，供互联系统使用。在启动容器时需要通过 `-P`，`Docker` 主机会自动分配一个端口转发到指定的端口。

> **ENV**

格式为 `ENV <key> <value>`

指定一个环境变量，会被后续 `RUN` 指令使用，并在容器运行时保持。

```dockerfile
ENV PG_MAJOR 9.3
ENV PG_VERSION 9.3.4
RUN curl -SL http://example.com/postgres-$PG_VERSION.tar.xz | tar -xJC /usr/src/postgress && …
ENV PATH /usr/local/postgres-$PG_MAJOR/bin:$PATH
```

> **ADD**

格式为 `ADD <src> <dest>`

复制指定的 `<src>` 到容器中的 `<dest>`。 其中 `<src>` 可以是 Dockerfile 所在目录的一个相对路径；也可以是一个 `URL`；还可以是一个 `tar` 文件（自动解压为目录）。

> **COPY**

格式为 `COPY <src> <dest>`。

复制本地主机的 `<src>`（为 Dockerfile 所在目录的相对路径）到容器中的 `<dest>`。

当使用本地目录为源目录时，推荐使用 COPY。

> **ENTRYPOINT**

两种格式：

- `ENTRYPOINT ["executable", "param1", "param2"]`
- `ENTRYPOINT command param1 param2`（shell中执行）。

配置**容器启动后执行的命令**，并且不可被 `docker run` 提供的参数覆盖。

每个 Dockerfile 中只能有一个 `ENTRYPOINT`，当指定多个时，只有最后一个起效。

> **VOLUME**

格式为 `VOLUME ["/data"]`。

创建一个可以从本地主机或其他容器挂载的挂载点，一般用来存放数据库和需要保持的数据等。

> **USER**

格式为 `USER daemon`。

指定运行容器时的用户名或 `UID`，后续的 `RUN` 也会使用指定用户。

当服务不需要管理员权限时，可以通过该命令指定运行用户。并且可以在之前创建所需要的用户，例如：`RUN groupadd -r postgres && useradd -r -g postgres postgres`。要临时获取管理员权限可以使用 `gosu`，而不推荐 `sudo`。

> **WORKDIR**

格式为 `WORKDIR /path/to/workdir`。

为后续的 `RUN、CMD、ENTRYPOINT` 指令配置工作目录。

可以使用多个 `WORKDIR` 指令，后续命令如果参数是相对路径，则会基于之前命令指定的路径。例如

```dockerfile
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
```

则最终路径为 `/a/b/c`。

> **ONBUILD**

格式为 `ONBUILD [INSTRUCTION]`。

配置当**所创建的镜像作为其它新创建镜像的基础镜像时**，所执行的操作指令。

例如，Dockerfile 使用如下的内容创建了镜像 image-A。

```dockerfile
[...]
ONBUILD ADD . /app/src
ONBUILD RUN /usr/local/bin/python-build --dir /app/src
[...]
```

如果基于 image-A 创建新的镜像时，新的 Dockerfile 中使用 FROM image-A 指定基础镜像时，会自动执行 ONBUILD 指令内容，等价于在后面添加了两条指令。

```dockerfile
FROM image-A

#Automatically run the following
ADD . /app/src
RUN /usr/local/bin/python-build --dir /app/src
使用 ONBUILD 指令的镜像，推荐在标签中注明，例如 ruby:1.9-onbuild。
```

### 6.3 创建镜像

编写完成 Dockerfile 之后，可以通过 `docker build` 命令来创建镜像。

基本的格式为 `docker build [选项] 路径`

该命令**将读取指定路径下（包括子目录）的 Dockerfile**，并将该路径下所有内容发送给 Docker 服务端，由服务端来创建镜像。

因此一般建议放置 Dockerfile 的目录为空目录。也可以通过 `.dockerignore` 文件（每一行添加一条匹配模式）来让 Docker 忽略路径下的目录和文件。

要指定镜像的标签信息，可以通过 `-t` 选项，例如

```dockerfile
sudo docker build -t myrepo/myapp /tmp/test1/
```

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
