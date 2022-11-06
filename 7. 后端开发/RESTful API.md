# 前言

- 在互联网并没有完全流行的初期，移动端也没有那么盛行，页面请求和并发量也不高，那时候人们对接口的要求没那么高，一些动态页面(jsp)就能满足绝大多数的使用需求。

![](https://bigsai.oss-cn-shanghai.aliyuncs.com/img/image-20201204001441126.png)

- 但是随着互联网和移动设备的发展，人们对Web应用的使用需求也增加，**传统的动态页面由于低效率而渐渐被HTML+JavaScript(Ajax)的前后端分离所取代**，并且安卓、IOS、小程序等形式客户端层出不穷，**客户端的种类出现多元化**，而客户端和服务端就需要接口进行通信，但**接口的规范性就又成了一个问题**：

![](https://bigsai.oss-cn-shanghai.aliyuncs.com/img/image-20201204001702612.png)

**一套结构清晰、符合标准、易于理解、扩展方便让大部分人都能够理解接受的接口风格**就显得越来越重要，而RESTful风格的接口(RESTful API)刚好有以上特点，就逐渐被实践应用而变得流行起来。

![](https://bigsai.oss-cn-shanghai.aliyuncs.com/img/image-20201204001618944.png)


现在，RESTful是目前最流行的接口设计规范，在很多公司有着广泛的应用，其中Github 的API设计就是很标准的RESTful API，你可以参考学习。

在开发实践中我们很多人可能还是使用传统API进行请求交互，很多人其实并不特别了解RESTful API，对RESTful API的认知可能会停留在：
- 面向资源类型的
- 是一种风格
- (误区)接口传递参数使用斜杠(/)分割而不用问号(?)传参。

而其实一个很大的误区不要认为没有查询字符串就是RESTful API，也不要认为用了查询字符串就不是RESTful API，更不要认为用了JSON传输的API就是RESTful API。

# 一、REST介绍

> **REST诞生**

**REST**（英文：Representational State Transfer，简称REST，直译过来表现层状态转换）**是一种软件架构风格、设计风格，而不是标准**，只是**提供了一组设计原则和约束条件**。它主要用于客户端和服务器交互类的软件。基于这个风格设计的软件可以更简洁，更有层次，更易于实现缓存等机制。

它首次出现在 2000 年 Roy Thomas Fielding 的博士论文中，这篇论文定义并详细介绍了表述性状态转移（Representational State Transfer，REST）的架构风格，并且描述了 如何使用 REST 来指导现代 Web 架构的设计和开发。用他自己的原话说：
```
我写这篇文章的目的是：在符合架构原理前提下，理解和评估基于网络的应用软件的架构设计，得到一个功能强、性能好、适宜通信的架构
```

需要注意的是**REST并没有一个明确的标准，而更像是一种设计的风格**，满足这种设计风格的程序或接口我们称之为RESTful(从单词字面来看就是一个形容词)。所以RESTful API 就是满足REST架构风格的接口。

> **REST架构特征**

既然知道REST和RESTful的联系和区别，现在就要开始好好了解RESTful的一些约束条件和规则，**RESTful是一种风格而不是标准，而这个风格大致有以下几个主要特征**：

- **以资源为基础：** 资源可以是一个图片、音乐、一个XML格式、HTML格式或者JSON格式等网络上的一个实体，除了一些二进制的资源外普通的文本资源更多以JSON为载体、面向用户的一组数据(通常从数据库中查询而得到)。
- **统一接口：** **对资源的操作包括获取、创建、修改和删除**，这些操作正好对应HTTP协议提供的GET、POST、PUT和DELETE方法。换言而知，使用RESTful风格的接口，**从接口上你可能只能定位其资源，但是无法知晓它具体进行了什么操作**，需要具体了解其发生了什么操作动作要从其HTTP请求方法类型上进行判断。具体的HTTP方法和方法含义如下：
  - **GET（SELECT）**：从服务器取出资源（一项或多项）。
  - **POST（CREATE）**：在服务器新建一个资源。
  - **PUT（UPDATE）**：在服务器更新资源（客户端提供完整资源数据）。
  - **PATCH（UPDATE）**：在服务器更新资源（客户端提供需要修改的资源数据）。
  - **DELETE（DELETE）**：从服务器删除资源。 
  ![RESTful API和传统API大致架构](https://bigsai.oss-cn-shanghai.aliyuncs.com/img/image-20201204001311359.png)

- **URI指向资源:** URI = Universal Resource Identifier 统一资源标志符，用来标识抽象或物理资源的一个紧凑字符串。**URI包括URL和URN**，在这里更多时候可能代指URL(统一资源定位符)。RESTful是面向资源的，**每种资源可能由一个或多个URI对应，但一个URI只指向一种资源**。

- **无状态：** **服务器不能保存客户端的信息， 每一次从客户端发送的请求中，要包含所有必须的状态信息**，会话信息由客户端保存， 服务器端根据这些状态信息来处理请求。 当客户端可以切换到一个新状态的时候发送请求信息， 当一个或者多个请求被发送之后, 客户端就处于一个状态变迁过程中。 每一个应用的状态描述可以被客户端用来初始化下一次的状态变迁。

> **REST架构限制条件**

Fielding在论文中提出**REST架构的6个限制条件**，也可称为**RESTful 6大原则**， 标准的REST约束应满足以下6个原则：

- **客户端-服务端(client-server)**：这个更专注客户端和服务端的分离，服务端独立可更好服务于前端、安卓、IOS等客户端设备。

- **无状态(Stateless)**:服务端不保存客户端状态，客户端保存状态信息每次请求携带状态信息。

- **可缓存性(Cacheability)**:服务端需回复是否可以缓存以让客户端甄别是否缓存提高效率。

- **统一接口(Uniform Interface)**:通过一定原则设计接口降低耦合，简化系统架构，这是RESTful设计的基本出发点。当然这个内容除了上述特点提到部分具体内容比较多详细了解可以参考[REST论文内容](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)

- **分层系统(Layered System)**:客户端无法直接知道连接的到终端还是中间设备，分层允许你灵活的部署服务端项目。

- **按需代码(Code-on-Demand)**:按需代码允许我们灵活的发送一些看似特殊的代码给客户端例如JavaScript代码。


# 二、RESTful API设计规范

了解了RESTful的一些规则和特性，**那么具体该怎么去设计一个RESTful API呢？** 本文从URL路径、HTTP请求动词、状态码和返回结果等方面详细考虑。至于其他的方面例如错误处理、过滤信息等规范未进行详细介绍。

## 2.1 URL设计规范

> **完整的URL组成路径**

URL为统一资源定位器 ,接口属于服务端资源，首先要通过URL这个定位到资源才能去访问，而通常一个完整的URL组成由以下几个部分构成：

```ini
URI = scheme "://" host  ":"  port "/" path [ "?" query ][ "#" fragment ]
```

- scheme:指底层用的协议，如http、https、ftp
- host:服务器的IP地址或者域名
- port: 端口，http默认为80端口
- path: 访问资源的路径，就是各种web 框架中定义的route路由
- query:**查询字符串，为发送给服务器的参数**，在这里更多发送数据分页、排序等参数。
- fragment: 锚点，定位到页面的资源

> **RESTful path组成**

**通常一个RESTful API的path组成如下：**
```ini
/{version}/{resources}/{resource_id}
```

- **version**:API版本号，有些版本号放置在头信息中也可以，通过控制版本号有利于应用迭代
- **resources**：资源，RESTful API推荐用小写英文单词的复数形式。
- **resource_id**:资源的id，访问或操作该资源。

**有时候可能资源级别较大，其下还可细分很多子资源也可以灵活设计URL的path**:
```ini
/{version}/{resources}/{resource_id}/{subresources}/{subresource_id}
```
**可能增删改查无法满足业务要求，可以在URL末尾加上action**,其中action就是对资源的操作。

```ini
/{version}/{resources}/{resource_id}/action
```
> **RESTful API的URL设计规范如下：**
- 不用大写字母，所有单词使用英文且小写
- 连字符用中杠"-"而不用下杠"_"
- 正确使用 "/"表示层级关系,URL的层级不要过深，并且越靠前的层级应该相对越稳定
- 结尾不要包含正斜杠分隔符"/"
- URL中不出现动词，用请求方式表示动作
- 资源表示用复数不要用单数
- 不要使用文件扩展名

## 2.2 HTTP请求

> **HTTP请求方法**


**在`non-RESTful`风格的API中**，我们通常使用GET请求和POST请求完成增删改查以及其他操作，查询和删除一般使用GET方式请求，更新和插入一般使用POST请求。从请求方式上无法知道API具体是干嘛的，所有在URL上都会有操作的动词来表示API进行的动作，例如：query，add，update，delete等等。

**而 `RESTful 风格`的API则要求在URL上都以名词的方式出现**，从几种请求方式上就可以看出想要进行的操作，这点与非RESTful风格的API形成鲜明对比。在RESTful API中，不同的HTTP请求方法有各自的含义，如下表示`GET`,`POST`,`PUT`,`DELETE`几种请求API的设计与含义分析。针对不同操作，具体的含义如下:
```bash
# 从服务器查询资源的列表（数组）
GET /collection

# 从服务器查询单个资源
GET /collection/resource

# 在服务器创建新的资源
POST /collection

# 更新服务器资源
PUT /collection/resource

# 从服务器删除资源
DELETE /collection/resource
```

如果要实现对dog资源的增删改查，下述表格为`非RESTful` 和`RESTful接口`对比：

|   API name    |           非 RESTful          |       RESTful            |
|       ----    |               ----            |       ----    |
|    获取dog     |       /dogs/query/{dogid}     |   GET： /dogs/{dogid}    |
|    插入dog     |       /dogs/add               |   POST：/dogs            |
|    更新dog     |       /dogs/update/{dogid}    |   PUT：/dogs/{dogid}     |
|    删除dog     |       /dogs/delete/{dogid}    |   DELETE：/dogs/{dogid}  |


**上述四种方法的安全性与幂等性**

|   HTTP Method    |    安全性    |    幂等性    |    解释    |
|       ----       |     ----    |     ----    |    ----    |
|       GET        |     安全     |     幂等    |    读操作安全，查询一次多次结果一致    |
|       POST        |     非安全     |     非幂等    |    写操作非安全，每多插入一次都会出现新结果    |
|       PUT        |     非安全     |     幂等    |    写操作非安全，一次和多次更新结果一致    |
|       DELETE        |     非安全     |     幂等    |    写操作非安全，一次和多次删除结果一致    |


> **状态码和返回数据**

服务端处理完成后客户端也可能不知道具体成功了还是失败了，**服务器响应时，包含状态码和返回数据两个部分。**

**状态码**
- 1xx：相关信息
- 2xx：操作成功
- 3xx：重定向
- 4xx：客户端错误
- 5xx：服务器错误

**主要常用状态码**
- `200 OK - [GET]`: 服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）
- `201 CREATED - [POST/PUT/PATCH]`:用户新建或修改数据成功。
- `202 Accepted - [*]`:表示一个请求已经进入后台排队（异步任务）
- `204 NO CONTENT - [DELETE]`:用户删除数据成功。
- `400 INVALID REQUEST - [POST/PUT/PATCH]`: 用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
- `401 Unauthorized - [*]`:表示用户没有权限（令牌、用户名、密码错误）。
- `403 Forbidden - [*]`:表示用户得到授权（与401错误相对），但是访问是被禁止的。
- `404 NOT FOUND - [*]`:用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
- `406 Not Acceptable - [GET]`:用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
- `410 Gone -[GET]`:用户请求的资源被永久删除，且不会再得到的。
- `422 Unprocesable entity - [POST/PUT/PATCH]`:当创建一个对象时，发生一个验证错误。
- `500 INTERNAL SERVER ERROR - [*]`:服务器发生错误，用户将无法判断发出的请求是否成功。

**返回数据**

针对不同操作，服务器向用户返回数据，而各个团队或公司封装的返回实体类也不同，但**都返回JSON格式数据给客户端。**

# 三、 RESTful的极致HATEOAS

RESTful 的极致是 hateoas ，但是这个基本不会在实际项目中用到。

实际上，**RESTful API 最好做到 Hypermedia**，即返回结果中提供链接，连向其他 API 方法，使得用户不查文档，也知道下一步应该做什么。

比如，当用户向 api.example.com 的根目录发出请求，会得到这样一个返回结果：

```json
{"link": {
  "rel":   "collection https://www.example.com/classes",
  "href":  "https://api.example.com/classes",
  "title": "List of classes",
  "type":  "application/vnd.yourformat+json"
}}
```

上述代码中表示：
- `link`: 用户读取这个属性就知道下一步该调用什么 API 了
- `rel`: 表示这个 API 与当前网址的关系（collection 关系，并给出该 collection 的网址）
- `href`:表示 API 的路径
- `title`:表示 API 的标题
- `type`: 表示返回类型

**`Hypermedia API`的设计被称为HATEOAS。**

在 Spring 中有一个叫做 HATEOAS 的 API 库，通过它我们可以更轻松的创建出符合 HATEOAS 设计的 API。

> **Spring中实现HATEOAS参考文档**

- [在 Spring Boot 中使用 HATEOAS](https://blog.aisensiy.me/2017/06/04/spring-boot-and-hateoas/)
- [Building REST services with Spring](https://spring.io/guides/tutorials/rest/)
- [An Intro to Spring HATEOAS](https://www.baeldung.com/spring-hateoas-tutorial)
- [spring-hateoas-examples](https://github.com/spring-projects/spring-hateoas-examples/tree/master/hypermedia)
- [Spring HATEOAS ](https://spring.io/projects/spring-hateoas#learn)

## 参考链接


