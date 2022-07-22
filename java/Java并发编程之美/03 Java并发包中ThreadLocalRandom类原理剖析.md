# 前言

从技术发展历史来讲Servlet编程开发早于JSP技术，即先有了Servlet，而后受到微软ASP技术的启发才有了JSP技术的发展，在整个JavaWEB开发过程中，只有Servlet是属于唯一的一种CGI实现组件。

最早的动态WEB实现技术主要依赖的就是CGI技术标准，但传统的CGI技术采用了多进程的方式来处理，其问题在于：每一次进程的启动和销毁都需要耗费资源

Java在产生初期所强调的最强的性能解决方案是采用多线程编程，所以使用Java实现的CGI技术是基于多线程开发实现的，与传统CGI相比性能是非常高的，而Servlet就是Java实现CGI技术的组件。

# 公共网关接口 CGI(Common gateway interface)

CGI仅仅是一个通信标准，受到早期硬件性能和软件技术的限制，大多数都采用的是多进程的处理技术，即：每一个用户请求对于操作系统内部都要启动一个相应的进程进行请求处理

![CGI](https://pic1.zhimg.com/80/v2-146dd92968211c1f8ae96ad4178fa66c_720w.jpg)

[万法归宗-GCI](https://zhuanlan.zhihu.com/p/25013398)

# Servlet

## 概述

- Servlet是Java实现CGI技术(Common Gateway Interface，公共网关接口)是Java为实现动态WEB开发在较早时期推出的一项技术，同时也是现在项目开发中必不可少的一项技术。

- 通过Java实现的CGI的线程技术，充分发挥了Java语言中多线程的技术特点，采用线程的形式实现了用户的HTTP请求与响应。

![Servlet多线程](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSJSsduEhxZVG-nxmAEWdEPNuumOc2Xd4VcQ&usqp=CAU)


- Servlet设计性能如此之高，为什么要提出JSP开发呢？
  - 在WEB开发技术中，除了核心技术的请求处理之外，最重要就是“颜值”
  - Servlet最严重的缺陷就是没有考虑到页面输出响应的繁琐程度。

- 早期JavaWEB开发阶段，为了解决页面显示问题，自己尝试做一个显示的模板页面，在最终需要生成的时候，利用IO流的形式进行文件读取，随后再整合成一个完整的HTML页面

- 后来由于推出了JSP，因此上述繁琐的流程被彻底简化了。


## 什么是Servlet？

## Servlet的优势

- 更好的性能
- 可移植性
- 稳健：JVM管理Servlet，所以我们不需要担心内存泄漏、垃圾回收等问题。
- 安全性

### 接口
### Servlet API

java.servlet和javax.servlet.http包表示servlet api的接口和类。

- java servlet包包含了许多被servelet或web容易使用的接口和类，并不针对任何协议
- javax.servlet.http包包含只负责http请求的接口和类


### Servlet 接口

Servlet接口为所有Servlet提供了共同的行为。Servlet接口定义了所有Servlet必须实现的方法。在创建任何servelet(直接或间接)时实现。它提供了5个方法

- 3个生命周期方法，用于初始化servlet，为请求提供服务以及销毁servlet
  - public void init()
  - public void service(ServletRequest request, ServletResponse response)
  - public void destroy() 
- 2个非生命周期方法
  - public ServletConfig getServeletConfig()
  - public String getServeletInfo() 

### ServletRequest接口

ServletRequest对象用于向Servlet提供客户端请求信息，如内容类型、内容长度、参数名称和值、头信息、属性等

### RequestDispatcher接口

RequestDispatcher接口提供了将请求分配给另一资源的功能，他可能是html、servlet或jsp。这个接口也可以用来包括另一个资源的内容，他是sevrvlet协作的方式之一。

- forward
- include

### HttpServletResponse接口

HttpServletResponse接口的sendRedirect()方法可以用来重定向响应到另一资源，它可以是servlet、jsp和html文件。

它接受相对和绝对的url。它在客户端工作，因为它使用浏览器的URL栏来进行另一个请求。因此他可以在服务器内部和外部工作。
