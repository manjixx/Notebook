# Shiro 简易教程

## 一、前言

### 1.1 权限管理

不同身份的人进入系统所完成的操作不同，如下图，当一个系统包含左侧所有菜单功能时，要求不同人员登录展示不同权限下的菜单。

![](https://img-blog.csdnimg.cn/83004cb70c764602a741a499f643b814.png)

> **基于主页的权限管理**

设计多种页面，当不同权限的用户访问时，跳转不同的页面。适用于用户级别较少的无法实现动态分配权限。

![](https://img-blog.csdnimg.cn/d0449ac4fe9345988f6a43d921c4a91c.png)

> **基于用户和权限的权限管理**

利用用户表、用户权限表、权限表三张表，每个用户在中间表分配权限，实现权限的动态分配，但是每个用户对应一个用户权限，10个人就得10个，数据比较冗余。

![](https://img-blog.csdnimg.cn/4fb180984d7e4385b76f47793a9715d0.png)

> **基于角色的访问控制（RBAC)**

创建**用户表、角色表、权限表**和**用户角色表、角色权限表**共计五张表，每次**新加用户时只需要授予角色就可获得相对的权限**。

![](https://img-blog.csdnimg.cn/238222c7f48b45f28acc4f0c67d6d49e.png)

给同类人员的其中一个人授予权限可以再加一张用户权限表，直接授予权限。

![](https://img-blog.csdnimg.cn/00c7caca662042e2bed19b67a4e47d17.png)

### 1.2 认证与授权

- 认证:对用户的身份进行检查（登录验证）
- 授权：对用户的权限进行检查（是否有对应的操作权限）

![](https://img-blog.csdnimg.cn/f9e7d5e3ec7a4c90842359edc22ea33e.png)

## 二、Shiro简介

### 2.1 Shiro简介

[Shiro官网](http://shiro.apache.org/)

Apache Shiro是一个强大且易用的Java安全框架,执行身份验证、授权、密码和会话管理。Shiro 可以非常容易的开发出足够好的应用，其不仅可以用在 JavaSE 环境，也可以用在 JavaEE 环境。

### 2.2 Shiro架构

> **外部视角**

![](https://img-blog.csdnimg.cn/img_convert/706a31d50a7a7ca01a78da4817de8ccf.png)

*Subject*：即“当前操作用户”。但是，在Shiro中，Subject这一概念并不仅仅指人，也可以是第三方进程、后台帐户（Daemon Account）或其他类似事物。它仅仅意味着“当前跟软件交互的东西”。

*SecurityManager*：**它是`Shiro`框架的核心，典型的`Facade`模式**，`Shiro`通过`SecurityManager`来管理内部组件实例，并通过它来提供安全管理的各种服务。`Subject`代表了当前用户的安全操作，`SecurityManager`则管理所有用户的安全操作。

*Realm：*

- `Realm`充当了`Shiro`与应用安全数据间的“桥梁”或者“连接器”。也就是说，当对用户执行认证（登录）和授权（访问控制）验证时，**`Shiro`会从应用配置的`Realm`中查找用户及其权限信息**。
- 从这个意义上讲，`Realm`实质上是一个安全相关的`DAO`：它封装了数据源的连接细节，并在需要时将相关数据提供给`Shiro`。当配置`Shiro`时，你必须至少指定一个`Realm`，用于认证和（或）授权。配置多个Realm是可以的，但是至少需要一个。
- `Shiro`内置了可以连接大量安全数据源（又名目录）的`Realm`，如LDAP、关系数据库（JDBC）、类似INI的文本配置资源以及属性文件等。如果缺省的`Realm`不能满足需求，你还可以插入代表自定义数据源的自己的`Realm`实现。

![](https://img-blog.csdnimg.cn/375879e2e1e04bea8a2eda5df40c0236.png)

> **内部视角**

![](https://img-blog.csdnimg.cn/d84812d46e8043b69502880966c80670.png)

**最上层的是我们的各种语言编写的应用程序**，而这些应用程序都是通过Subject与Shiro进行交互的。Subject与整个SecurityManager进行交互。

对于**整个SecurityManager**，包括以下组件：

- **Subject**：代表任何与应用程序发送交互的用户。
- **SecurityManager**：相当于`SpringMVC`的`Dispatcher`，是`Shiro`的心脏。所有交互都会通过`SecurityManager`进行控制，它管理着所有`Subject`，且负责进行认证、授权、会话以及缓存的管理。
- **Authenticator**：负责`Subject`认证，是一个拓展点，可以自定义实现。可以使用认证策略（`Authentication Strategy`），即在什么情况下算用户认证通过了。
- **Authorizer**：授权器，即访问控制器，用来决定主体是否有权进行相应的操作，即控制着用户能访问应用中的哪些功能。
- **Realm**：安全实体数据源。即是提供安全数据的源头，数据源可以是JDBC操作的数据库数据，也可以是缓存中的数据。该实体由用户提供，一般在应用中都需要实现自己的Realm。可以有一个或者多个Realm。
- **SessionManager**：管理Session生命周期的组件。Shiro不仅仅可以在Web环境，也可以在普通的JavaSE环境中。
- **CacheManager**：缓存控制器，来管理如用户、角色、权限等信息的缓存。由于这些数据基本上很少发生变动，所以存放在缓存中可以提供访问的性能。
- **Cryptography**：密码模块。Shiro提供了一些常见的加密组件用于密码的加密/解密。

### 2.3 基本功能

![](https://img-blog.csdnimg.cn/img_convert/4be541ef2b5b188c8b20b59a6cd2fe8e.png)

- *Authentication*：即是“认证”功能，说白了登录。我们可以利用Shiro实现登录效果，通过Shiro帮我们完成密码匹配的工作
- *Authorization*：即是“授权”功能，当我们点一个链接或按钮的时候，Shiro会帮我们判断操作者有没有权限访问该服务。
- *Session Management*：即是“会话管理”功能，在Web系统下(即JavaEE)环境下，是对Http的Session进行托管。而在JavaSE下是由Shiro单独提供一种Session机制。
- *Cryptography*：即是“加密”功能，我们可以很容易的使用Shiro为密码进行“加盐”加密。
- *Web Support*：对于Web进行支持。Shiro可以很容易的与JavaEE工程进行集成。
- *Concurency*：在多线程的情况下，来进行授权认证。例如在一个线程中开启另外一个线程，能把权限自动传播过去。
- *Caching*：Shiro的缓存模块，让系统的授权机制运行速度更快。
- *Run As*：让已经登录的用户，以另外一个用户的身份来操作当前的项目和系统。
- *Remember Me*：即“记住我”，是一个十分常见的功能，即是一次登录后，下次再次访问则不需要登录。
- *Testing*：Shiro提供测试支持。

### 2.4 Shiro 和 Spring Security的区别

> **Spring Security**

`Spring Security`是一个灵活和强大的身份验证和访问控制框架，以确保基于`Spring`的`Java Web`应用程序的安全。

Spring Security 主要实现了:

- Authentication（认证，解决who are you? ）
- Access Control（访问控制，也就是what are you allowed to do？，也称为Authorization）。
  
Spring Security在架构上将认证与授权分离，并提供了扩展点。“认证”是为用户建立一个其声明的角色的过程，这个角色可以一个用户、一个设备或者一个系统。“验证”指的是一个用户在你的应用中能够执行某个操作。在到达授权判断之前，角色已经在身份认证过程中建立了。

**特点：**Shiro能实现的，Spring Security 基本都能实现，依赖于Spring体系，但是好处是Spring全家桶的一员，集成上更加契合，在使用上，比Shiro略功能强大（但是一般Shiro够用）

> **Shiro 和 Spring Security区别**

- `Shiro`比`Spring Security`更容易使用，也就是实现上简单一些，同时基本的授权认证`Shiro`也基本够用
- `Spring Security`社区支持度更高（但是安装`Spring Security`很难），`Spring`社区支持力度和更新维护上有优势，同时和`Spring`这一套的结合较好
- `Shiro`功能强大且简单、灵活。是Apache 下的项目比较可靠，且不跟任何的框架或者容器绑定，可以独立运行

**总结：**

- Shiro 首选 ，上手快 ，也足够用，自由度高，Spring Security中有的，Shiro也基本都有（项目没有使用Spring这一套，不用考虑，直接Shiro）
- 如果开发项目使用Spring这一套，用Spring Security可能更合适一些；虽然Spring Security 比较复杂，但与Spring 家族结合能力更强，是一个可以放心选择的框架结构


## 三、SpringBoot 整合 Shiro

### 3.1 原生整合

> **创建项目**

创建一个 Spring Boot 项目，只需要添加 Web 依赖即可。

> **添加Shiro依赖**

项目创建成功后，加入 Shiro 相关的依赖，完整的 pom.xml 文件中的依赖如下

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.apache.shiro</groupId>
        <artifactId>shiro-web</artifactId>
        <version>1.4.0</version>
    </dependency>
    <dependency>
        <groupId>org.apache.shiro</groupId>
        <artifactId>shiro-spring</artifactId>
        <version>1.4.0</version>
    </dependency>
</dependencies>
```

> **创建 Realm**

```java
/**
在 Realm 中实现简单的认证操作即可，不做授权，授权的具体写法和 SSM 中的 Shiro 一样
 */
public class MyRealm extends AuthorizingRealm {
    @Override
    protected AuthorizationInfo doGetAuthorizationInfo(PrincipalCollection principals) {
        return null;
    }
    @Override
    protected AuthenticationInfo doGetAuthenticationInfo(AuthenticationToken token) throws AuthenticationException {
        /**证表示用户名必须是 javaboy ，用户密码必须是 123*/
        String username = (String) token.getPrincipal();
        if (!"javaboy".equals(username)) {
            throw new UnknownAccountException("账户不存在!");
        }
        return new SimpleAuthenticationInfo(username, "123", getName());
    }
}
```

> **配置Shiro**

在这里进行 Shiro 的配置主要配置 3 个 Bean ：

- 首先需要提供一个 Realm 的实例。
- 需要配置一个 SecurityManager，在 SecurityManager 中配置 Realm。
- 置一个 `ShiroFilterFactoryBean` ，在 `ShiroFilterFactoryBean` 中指定路径拦截规则等。
- 配置登录和测试接口。

其中 `ShiroFilterFactoryBean` 的配置稍微多一些，配置含义如下：

- `setSecurityManager` 表示指定 `SecurityManager`。
- `setLoginUrl` 表示指定登录页面。
- `setSuccessUrl` 表示指定登录成功页面。
- 接下来的 Map 中配置了路径拦截规则，注意，要有序。

**拦截规则：**

- anon 匿名用户可访问
- authc  认证用户可访问
- user 使用RemeberMe的用户可访问  
- perms  对应权限可访问
- role  对应的角色可访问

```java
@Configuration
public class ShiroConfig {
    @Bean
    MyRealm myRealm() {
        return new MyRealm();
    }
    
    @Bean
    SecurityManager securityManager() {
        DefaultWebSecurityManager manager = new DefaultWebSecurityManager();
        manager.setRealm(myRealm());
        return manager;
    }
    
    @Bean
    ShiroFilterFactoryBean shiroFilterFactoryBean() {
        ShiroFilterFactoryBean bean = new ShiroFilterFactoryBean();
        bean.setSecurityManager(securityManager());
        bean.setLoginUrl("/login");
        bean.setSuccessUrl("/index");
        bean.setUnauthorizedUrl("/unauthorizedurl");
        Map<String, String> map = new LinkedHashMap<>();
        map.put("/doLogin", "anon");
        map.put("/**", "authc");
        bean.setFilterChainDefinitionMap(map);
        return bean;
    }
}
```

## 四、Spring 整合 Shiro
