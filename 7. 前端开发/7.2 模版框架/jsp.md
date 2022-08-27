# 概述


# JSP脚本元素

在JSP中，可以使用脚本元素在JSP页面内编写java代码。脚本元素提供了在jsp中插入java代码的能力。有三种类型的脚本元素：

```jsp
<!-- 脚本标签-->
<% java source code %>

<!-- 表达式标签-->
<%= statement %>

<!-- 声明标签 -->
<%! field or method declaration %>
```

# JSP 隐式对象

有9个jsp隐式对象。这些对象是由web容器创建的，对所有的jsp页面都可用。可用的隐式对象有out、request、config、session、application等

|  Object     | Type                |
|  ----       | ----                |
|   out       | JspWriter           |
| request     | HttpServletRequest  |
| reponse     | HttpServletResponse |
| config      | ServletConfig       |
| application | ServletContextt     |
| session     | HttpSession         |
| pageContext | PageContext         |
| exception   | Throwable           |

# JSP 指令

jsp指令是告诉Web容器如何在JSP页面翻译成相应的servlet的消息，有三种类型的指令

```jsp
<!-- 页面指令 -->
<% @ page attribute = "value" %>

<!-- 包含指令 -->
<% @ include file = "resourceName" %>

<!-- 标签库指令 -->

<%@ taglib uri = "uriofthetaglibrary" prefix = "prefixoftaglibrary"%>
```

# JSP操作标签

有许多JSP操作标签或元素。每个JSP操作标签用于执行某些特定任务。操作标签用于控制页面之间的流动并使用Java Bean

|  JSP Action Tags     | Description                                     |
|  ----                | ----                                            |
|   jsp:forward        | 将请求和响应转发到另一个资源                     |
|   jsp:include        | 包括另一个资源                                  |
|   jsp:useBean        | 创建或定位bean对象                              |
|   jsp:setProperty    | 设置bean对象中的属性值                          |
|   jsp:getProperty    | 打印bean的属性值                                |
|   jsp:plugin         | 嵌入另一个组件，如小程序                        |
|   jsp:param          | 设置参数值，他用于转发，主要包括                  |
|   jsp:fallback       | 如果插件正在工作，可用于打印消息。用于jsp:plugin  |


# 表达式语言(EL) in jsp

表达式语言简化了存储在Java Bean组件中的数据的可访问性，以及其他对象如请求、会话、应用程序等。在EL中，有许多隐含的对象、运算符和保留字

```jsp
${exoression}
```
|  Object            | Object      |
|  ----              | ----        |
|  pageScope         | header      |
|  requestScope      | headerValues|
|  sessionScope      | cookie      |
|  applicationScope  | initParam   |
|  param             | PageContext |
|  paramValue        |             |

# JSP中的MVC

MVC代表模型视图和控制器。它是一种业务逻辑、表示逻辑和数据分开设计模式。

控制器充当视图和模型之间的借口。控制器拦截所有传入的请求。

模型表示应用程序的状态即数据。它还可以具有业务逻辑。

视图表示呈现，即UI，用户界面

![jsp MVC](https://img1.baidu.com/it/u=32510383,981726971&fm=253&fmt=auto&app=138&f=JPEG?w=830&h=467)
