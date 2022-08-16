# 一、Mybatis基本概念

> **Mybatis是什么**

MyBatis 是一款优秀的持久层框架，**一个半 ORM（对象关系映射）框架**，它支持定制化 SQL、存储过程以及高级映射。MyBatis 避免了几乎所有的 JDBC 代码和手动设置参数以及 获取结果集。MyBatis 可以使用简单的 XML 或注解来**配置和映射**原生类型、接口和 Java的POJO（Plain Old Java Objects，普通老式 Java 对象）为数据库中的记录。

> **为什么说Mybatis是半自动的ORM映射工具**
- Hibernate属于全自动ORM映射工具，使用Hibernate查询关联对象或者关联集合对象时，**可以根据对象关系模型直接获取**，所以它是全自动的。
- Mybatis在查询关联对象或关联集合对象时，**需要手动编写sql来完成**，所以，称之为半自动ORM映射工具。


> **Mybatis如何解决JDBC编程中不足**

|   问题     |   Mybatis解决方案      |
|   ----     |      ----            |
|   数据库链接创建、释放频繁造成系统资源浪费从而影响系统性能，如果使用数据库连接池可解决此问题。     |      在mybatis-config.xml中配置数据链接池，使用连接池管理数据库连接。 |
|   Sql语句写在代码中造成代码不易维护，实际应用sql变化的可能较大，sql变动需要改变 java代码。     |      将Sql语句配置在XXXXmapper.xml文件中与java代码分离 |
|   向sql语句传参数麻烦，因为sql语句的where条件不一定，可能多也可能少，占位符需要和参数一一对应。     |      Mybatis自动将java对象映射至sql语句 |
|   对结果集解析麻烦，sql变化导致解析代码变化，且解析前需要遍历，如果能将数据库记 录封装成pojo对象解析比较方便     |     Mybatis自动将sql执行结果映射至java对象   |

> **Mybatis的优缺点**

- **优点**
  - 基于SQL语句编程，相当灵活，不会对应用程序或者数据库的现有设计造成任何影响，SQL 写在XML里，解除sql与程序代码的耦合，便于统一管理；提供XML标签，支持编写动态 SQL语句，并可重用
  - 与JDBC相比，减少了50%以上的代码量，消除了JDBC大量冗余的代码，不需要手动开关连接
  - 很好的与各种数据库兼容（因为MyBatis使用JDBC来连接数据库，所以只要JDBC支持的数 据库MyBatis都支持）
  - 能够与Spring很好的集成

- **缺点**
  - SQL语句的编写工作量较大，尤其当字段多、关联表多时，对开发人员编写SQL语句的功底 有一定要求
  - SQL语句依赖于数据库，导致数据库移植性差，不能随意更换数据库

> **Mybatis适用场景**

MyBatis专注于SQL本身，是一个足够灵活的DAO层解决方案。对性能的要求很高，或者需求变化较多的项目，如互联网项目，MyBatis将是不错的选择。

> **Hibernate与Mybatis的区别**

- **相同点：** 都是对jdbc的封装，都是持久层的框架，都用于dao层的开发。

- **映射关系不同**
  -  ***MyBatis*** 是一个半自动映射的框架，配置Java对象与sql语句执行结果的对应关系，多表关联关系配置简单；
  - ***Hibernate*** 是一个全表映射的框架，配置Java对象与数据库表的对应关系，多表关联关系配置复杂

- **SQL优化和移植性：**
  - ***Hibernate*** 对SQL语句封装，提供了日志、缓存、级联（级联比 MyBatis 强大）等特性， 此外还提供 HQL（Hibernate Query Language）操作数据库，数据库无关性支持好，但 会多消耗性能。如果项目需要支持多种数据库，代码开发量少，但SQL语句优化困难
  - ***MyBatis*** 需要手动编写 SQL，支持动态 SQL、处理列表、动态生成表名、支持存储过程。 开发工作量相对大些。直接使用SQL语句操作数据库，不支持数据库无关性，但sql语句优 化容易。
- **开发难易程度和学习成本：**
  - ***Hibernate 是重量级框架***，学习使用门槛高，适合于需求相对稳定，中小型的项目，比如： 办公自动化系统
  - ***MyBatis 是轻量级框架***，学习使用门槛低，适合于需求变化频繁，大型的项目，比如：互 联网电子商务系统
 
- **总结**
  -  MyBatis 是一个小巧、方便、高效、简单、直接、半自动化的持久层框架； 
  -  Hibernate 是一个强大、方便、高效、复杂、间接、全自动化的持久层框架。

# 二、Mybatis解析和运行原理

## 2.1 Mybatis工作原理

### Mybatis编译步骤主要包括如下5步：
- 1.构造会话工厂SqlSessionFactory
- 2.通过SqlSessionFactory创建会话对象SqlSession
- 3.通过SqlSession执行数据库操作
- 4.通过调用session.commit()提交事务
- 5.通过session.close()关闭会话

### Mybatis工作原理

如下图所示为Mybatis工作原理：

![Mybatis工作原理](https://segmentfault.com/img/bVbMnUc)

- **读取Mybatis配置文件：**  mybatis-config.xml 为 MyBatis 的全局配置文件，配置了 MyBatis 的运行环境等信息，例如数据库连接信息
- 加载映射文件：映射文件即SQL映射文件，该文件中配置了操作数据库的SQL语句，需要在Mybatis配置文件中加载。**Mybatis配置文件可以加载多个映射文件，每个文件对应数据库中的一张表**。
- **构造会话工厂：** 通过 MyBatis 的环境等配置信息构建会话工厂 SqlSessionFactory。
- 创建会话对象：由会话工厂创建 SqlSession 对象，该对象中包含了执行 SQL 语句的所有方法。
- **Executor 执行器：** MyBatis 底层定义了一个 Executor 接口来操作数据库，它将根据 SqlSession 传递的参数动态地生成需要执行的 `SQL` 语句，同时负责查询缓存的维护。
- **MappedStatement对象:** 在`Executor`接口的执行方法中有一个`MappedStatement`类型的参数，该参数是对映射信息的封装，用于存储要映射的`SQL`语句的 id、参数等信息。
- **输入参数映射：** 输入参数类型可以是 Map、List 等集合类型，也可以是基本数据类型和 POJO 类型。输入参数映射过程类似于 JDBC 对 preparedStatement 对象设置参数的过程。
- **输出结果映射：** 输出结果类型可以是 Map、 List 等集合类型，也可以是基本数据类型 和 POJO 类型。输出结果映射过程类似于 JDBC 对结果集的解析过程。

### 常见问题

> **什么是预编译，为什么需要预编译**

SQL预编译是指数据库驱动在发送SQL语句和参数给DBMS之前对SQL语句进行编译，这样DBMS执行SQL时，就不需要重新编译

**预编译可以优化SQL的执行：**
- 预编译之后的 SQL 多数情况下可以直接执行，DBMS 不需要再次编译；
- 越复杂的SQL，编译的复杂度将越大，预编译阶段可以合并多次操作为一个操作；
- 预编译语句对象可以重复利用。把一个 SQL预编译后产生的 PreparedStatement 对象缓 存下来，下次对于同一个SQL，可以直接使用这个缓存的PreparedState 对象。


> ** Mybatis都有哪些Executor执行器，它们之间区别是什么？**

Mybatis有三种基本的Executor执行器，`SimpleExecutor`、`ReuseExecutor`、 `BatchExecutor`。

- **SimpleExecutor：** 默认的执行器，对每条sql语句进行预编译、设置参数、执行等操作。每执行一次update或select，就开启一个Statement对象，用完立刻关闭Statement对象；
- **ReuseExecutor：** REUSE 执行器会重用预处理语句 （prepared statements）。执行update或select，以sql作为key查找Statement对象，存在就使用，不存在就创建，用完后，不关闭Statement对象，而是放置于Map内，供下一次使用；
- **BatchExecutor：** 批量执行器，执行update（没有select，JDBC批处理不支持select），将所有sql都添加到批处理中（addBatch()），等待统一执行（executeBatch()），它缓存了多个Statement对象，每个Statement对象都是addBatch()完毕后，等待逐一执行executeBatch()批处理。与JDBC批处理相同。

- **作用范围：** Executor的这些特点，都严格限制在SqlSession生命周期范围内。

> **Mybatis如何指定使用哪一种Executor执行器？**

- 在Mybatis配置文件中，可以指定默认的ExecutorType执行器类型
- 手动给DefaultSqlSessionFactory的创建SqlSession的方法传递ExecutorType类型参数
## 2.2 Mybatis功能架构

- **API接口层：** 提供给外部使用的接口API，开发人员通过这些本地API来操纵数据库。接口层一接收到调用请求就会调用数据处理层来完成具体的数据处理。
- **数据处理层：** 负责具体的SQL查找、SQL解析、SQL执行和执行结果映射处理等。它主要的目的是根据调用的请求完成一次数据库操作。
- **基础支撑层：** 负责最基础的功能支撑，包括连接管理、事务管理、配置加载和缓存处理，这些都是共用的东西，将他们抽取出来作为最基础的组件。为上层的数据处理层提供最基础的支撑。

![Mybatis功能架构](https://upload-images.jianshu.io/upload_images/9033085-45f641094a702061.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

# 三、Mybatis数据源与连接池

# 四、Mybatis 缓存

# 五、参考链接
[Mybatis教程](https://www.cnblogs.com/diffx/p/10611082.html)
[Mybatis教程](https://blog.csdn.net/wanglei19891210/article/details/105653841)
