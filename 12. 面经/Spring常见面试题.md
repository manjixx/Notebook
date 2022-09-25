# Spring常见面试题

## 一、Spring基础

### 1.1 什么是Spring框架？


Spring是一款轻量级开源框架。一般我们所说Spring框架是指Spring Framework。是很多模块的集合，使用这些模块可以方便的协助我们进行开发。

比如Spring支持IOC(控制反转)和AoP(面向切面编程)、可以方便地支持我们对数据库进行访问，方便的集成第三方组件、对单元测试性支持比较好、支持RESTful Java应用的开发。

Spring 最核心的思想就是不重新造轮子，开箱即用，提高开发效率。


### 1.2 Spring包含哪些模块

> **Core Container**

Spring **框架的核心模块**，也可以说是基础模块，**主要提供 IoC 依赖注入功能的支持**。Spring 其他所有的功能基本都需要依赖于该模块。

> **AOP**

- spring-aspects ：该模块为与 AspectJ 的集成提供支持。
- spring-aop ：提供了面向切面的编程实现。

> **Data Access/Integration**

- spring-jdbc ：提供了对数据库访问的抽象 JDBC。不同的数据库都有自己独立的 API 用于操作数据库，而 Java 程序只需要和 JDBC API 交互，这样就屏蔽了数据库的影响。
- spring-tx ：提供对事务的支持。
- spring-orm ： 提供对 Hibernate、JPA 、iBatis 等 ORM 框架的支持。
- spring-oxm ：提供一个抽象层支撑 OXM(Object-to-XML-Mapping)，例如：JAXB、Castor、XMLBeans、JiBX 和 XStream 等。
- spring-jms : 消息服务。自 Spring Framework 4.1 以后，它还提供了对 spring-messaging 模块的继承。

> **Spring Web**

- spring-web ：对 Web 功能的实现提供一些最基础的支持。
- spring-webmvc ： 提供对 Spring MVC 的实现。
- spring-websocket ： 提供了对 WebSocket 的支持，WebSocket 可以让客户端和服务端进行双向通信。
- spring-webflux ：提供对 WebFlux 的支持。WebFlux 是 Spring Framework 5.0 中引入的新的响应式框架。与 Spring MVC 不同，它不需要 Servlet API，是完全异步。

> **Messaging**

- spring-messaging 是从 Spring4.0 开始新加入的一个模块，主要职责是为 Spring 框架集成一些基础的报文传送应用。

> **Spring Test**
Spring 团队提倡测试驱动开发（TDD）。有了控制反转 (IoC)的帮助，单元测试和集成测试变得更简单。

### 1.3 Spring、Spring MVC与Spring Boot

- Spring包含了多个模块，主要是Spring Core(提供依赖注入功能的支持)模块，Spring中其他模块(比如Spring MVC)的功能都依赖于该模块
- Spring MVC是Spring中非常重要的一个模块，主要赋予Spring快速构建MVC架构的Web应用的功能。MVC的是模型(Model)、视图(View)、控制器(Controller)的简写。其核心思想是通过将业务、数据、显示分离来组织代码
- 由于Spring在开发过程中需要使用xml或Java进行显示配置，所以Spring Boot诞生用于简化配置，如果你需要构建 MVC 架构的 Web 程序，你还是需要使用 Spring MVC 作为 MVC 框架，只是说 Spring Boot 帮你简化了 Spring MVC 的很多配置，真正做到开箱即用！

## 二、Spring IoC

### 2.1 谈一谈你对Spring IoC的了解

IoC(Inverse Of Control)控制反转，是一种设计思想，而不是一个具体的技术实现。

IoC的思想是原本在程序中手动创建对象的控制权，交由Spring框架来管理。但IoC并非Spring特有，在其他语言中也有应用。

### 2.2 为什么叫控制反转

- 控制:指的是对象创建(实例化、管理)的权力
- 反转:控制权交给外部环境(Spring框架、IoC容器)

将对象间相互依赖的关系交由IoC容器来管理，并由IoC容器完成对象注入，这样可以很大程度上简化应用的开发，把应用从复杂的依赖关系中解放出来。

![](https://camo.githubusercontent.com/dd18c750a56f6d68652a5cb0e050e354ff20cbab0e8328f491a46e0b59323931/68747470733a2f2f67756964652d626c6f672d696d616765732e6f73732d636e2d7368656e7a68656e2e616c6979756e63732e636f6d2f6a6176612d67756964652d626c6f672f6672632d33363566616365623536393766303466333133393939333763303539633136322e706e67)

### 2.2 什么是IoC容器

IoC容器就像是一个工厂一样，当我们需要创建一个对象时，只要配置好配置文件/注解即可，完全不用考虑对象是如何创建被创建出来。

在Spring中，IoC容器是Spring实现IoC的载体，其本质上是一个Map(key，Value),Map中存放的是各种对象。

### 2.3什么是Spring Bean?

简而言之，Spring Bean就是IoC容器所管理的对象。

我们是通过元数据来定义，告诉IoC容器帮助我们管理哪些对象。配置元数据可以是XML文件、注解、Java配置类。

![](https://camo.githubusercontent.com/ce0b88d5486ec515b5e60b78f3859efbf3b65158ab005186fdebd830776a51b5/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f30363262343232626437616334643533616664323866623734623262633934642e706e67)

### 2.4 将一个类声明为Bean的注解有哪些

- @Componet：**通用的注解**，可标注任意类为 Spring 组件。如果一个 Bean 不知道属于哪个层，可以使用@Component 注解标注。
- @Repository： **对应持久层**即 Dao 层，主要用于数据库相关操作。
- @Service：**对应服务层**，主要涉及一些复杂的逻辑，需要用到 Dao 层。
- @Controller：**对应 Spring MVC 控制层**，主要用户接受用户请求并调用 Service 层返回数据给前端页面。

### 2.5 @Component 和 @Bean 的区别是什么？

- @Component 注解作用于类，而@Bean注解作用于方法。
- @Component通常是通过类路径扫描来自动侦测以及自动装配到 Spring 容器中（我们可以使用 @ComponentScan 注解定义要扫描的路径从中找出标识了需要装配的类自动装配到 Spring 的 bean 容器中）。@Bean 注解通常是我们在标有该注解的方法中定义产生这个 bean,@Bean告诉了 Spring 这是某个类的实例，当我需要用它的时候还给我。
- @Bean 注解比 @Component 注解的自定义性更强，而且很多地方我们只能通过 @Bean 注解来注册 bean。比如当我们引用第三方库中的类需要装配到 Spring容器时，则只能通过 @Bean来实现。

### 2.6 进入Bean的注解有哪些


| Annotaion    | Package                            | Source       |
| ------------ | ---------------------------------- | ------------ |
| `@Autowired` | `org.springframework.bean.factory` | Spring 2.5+  |
| `@Resource`  | `javax.annotation`                 | Java JSR-250 |
| `@Inject`    | `javax.inject`                     | Java JSR-330 |

### 2.7 @Autowired和@Resource的区别
- `@Autowired` 是 Spring 提供的注解，`@Resource` 是 JDK 提供的注解。
- `Autowired` 默认的注入方式为`byType`（根据类型进行匹配），`@Resource`默认注入方式为 `byName`（根据名称进行匹配）。
- 当一个接口存在多个实现类的情况下，`@Autowired` 和`@Resource`都需要通过名称才能正确匹配到对应的 Bean。`Autowired` 可以通过 `@Qualifier` 注解来显示指定名称，`@Resource`可以通过 `name` 属性来显示指定名称。

## 三、Spring AoP

### 3.1 谈一谈自己对AoP的理解

AoP(Aspect-Oriented Programming:面向切面编程):能够将与业务无关，但被业务共同调用的逻辑或责任(事务处理、日志管理、权限管理)等封装起来，便于减少代码的重复，降低模块间的耦合性，有利于未来的拓展性和可维护性。

Spring AOP 就是基于动态代理的

**如果要代理的对象实现了某个接口**，那么 Spring AOP 会使用 **JDK Proxy**，去创建代理对象;

**对于没有实现接口的对象**，就无法使用 JDK Proxy 去进行代理了，这时候 Spring AOP 会使用 Cglib 生成一个被代理对象的子类来作为代理，如下图所示：

![](https://camo.githubusercontent.com/0404566c09d07416889e4e1c65a17338dc1d295b31ed8c2cb98c5211614235ed/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f696d675f636f6e766572742f32333061653538376133323264366534643039353130313631393837643334362e6a706567)

### 3.2 AspectJ与Spring AoP

- SpringAoP属于运行时增强，而AspectJ是编译时增强
- SpringAoP基于代理，而AspectJ基于字节码操作
- SpringAoP已经集成AspectJ,AspectJ是Java生态系统中，最完整的AOP框架了。AspectJ 相比于 Spring AOP 功能更加强大，但是 Spring AOP 相对来说更简单。

## 四、Spring MVC

### 4.1 什么是Spring MVC

MVC 是模型(Model)、视图(View)、控制器(Controller)的简写，其核心思想是通过将业务逻辑、数据、显示分离来组织代码。

**MVC 是一种设计模式**，Spring MVC 是一款很优秀的 MVC 框架。Spring MVC 可以帮助我们进行更简洁的 Web 层的开发，并且它天生与 Spring 框架集成。Spring MVC 下我们一般把后端项目分为 Service 层（处理业务）、Dao 层（数据库操作）、Entity 层（实体类）、Controller 层(控制层，返回数据给前台页面)。

### 4.2 Spring MVC核心组建有哪些

- DispatcherServerlet:核心中央处理器，负责接收请求、分发并给予客户端响应
- HandlerMapping:处理器映射，根据uri去匹配查找能处理的Handler,并会将请求涉及到的拦截器和 Handler 一起封装。
- HanderAdapter:处理器适配器，根据HandlerMapping找到的Handler,适配对应的Handler
- Handler:处理器，处理实际请求
- ViewResolver:视图解析器，根据Handler返回的逻辑视图/视图，解析并渲染真正的视图，并传递给DispatcherServlet响应客户端。

### 4.3 Spring MVC工作原理

![](https://camo.githubusercontent.com/0fd35900c32b252a18ff38855ae52192f90f8884f1622bb5f92578fe68c6cb2f/68747470733a2f2f696d672d626c6f672e6373646e696d672e636e2f696d675f636f6e766572742f64653664326232313366313132323937323938663365323233626630386632382e706e67)


### 4.4 统一异常处理怎么做？

推荐使用注解的方式统一异常处理，具体会使用到 @ControllerAdvice + @ExceptionHandler 这两个注解 。

## 五、Spring用到的设计模式

- **单例模式**:Spring 中的 Bean 默认都是单例的。
- **代理设计模式**:Spring AOP 功能的实现。
- **工厂设计模式**: Spring 使用工厂模式通过 BeanFactory、ApplicationContext 创建 bean 对象。
- **模板方法设计模式**: Spring 中 jdbcTemplate、hibernateTemplate 等以 Template 结尾的对数据库操作的类，它们就使用到了模板模式。
- **包装器设计模式**: 我们的项目需要连接多个数据库，而且不同的客户在每次访问中根据需要会去访问不同的数据库。这种模式让我们可以根据客户的需求能够动态切换不同的数据源。
- **观察者设计模式**:Spring 事件驱动模型就是观察者模式很经典的一个应用。
- **适配器模式**:Spring AOP 的增强或通知(Advice)使用到了适配器模式、spring MVC 中也是用到了适配器模式适配Controller。