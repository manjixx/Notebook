# Nginx的诞生

Nginx 同 Apache 一样都是一种 Web 服务器。基于 REST 架构风格，以统一资源描述符（Uniform Resources Identifier）URI 或者统一资源定位符（Uniform Resources Locator）URL 作为沟通依据，通过 HTTP 协议提供各种网络服务。

![架构图](https://pic1.zhimg.com/80/v2-e1826bab1d07df8e97d61aa809b94a10_720w.jpg)
上图基本上说明了当下流行的技术架构，其中Nginx有点入口网关的味道。


Apache服务器是毫无争议的世界第一大服务器，其具备：稳定、开源、跨平台等诸多优点

但Apache同时存在如下缺点：

- 不支持高并发，在 Apache 上运行数以万计的并发访问，会导致服务器消耗大量内存。
- 操作系统对其进行进程或线程间的切换也消耗了大量的 CPU 资源，导致 HTTP 请求的平均响应速度降低。、

由于如下几点Nginx火了：
- Nginx 使用基于事件驱动架构，使得其可以支持数以百万级别的 TCP 连接。

- 高度的模块化和自由软件许可证使得第三方模块层出不穷（这是个开源的时代啊）。

- Nginx 是一个跨平台服务器，可以运行在 Linux、Windows、FreeBSD、Solaris、AIX、Mac OS 等操作系统上。

# 基本概念

## 正向代理与反向代理

由于防火墙的原因，我们并不能直接访问谷歌，那么我们可以借助VPN来实现，这就是一个简单的正向代理的例子。这里你能够发现，正向代理“代理”的是客户端，而且客户端是知道目标的，而目标是不知道客户端是通过VPN访问的。

当我们在外网访问百度的时候，其实会进行一个转发，代理到内网去，这就是所谓的反向代理，即反向代理“代理”的是服务器端，而且这一个过程对于客户端而言是透明的。


# 参考链接
[](https://zhuanlan.zhihu.com/p/34943332)
[](https://mp.weixin.qq.com/s/XoqGvYBabW8YBl9xEeNYZw)
[](https://github.com/dunwu/nginx-tutorial)
