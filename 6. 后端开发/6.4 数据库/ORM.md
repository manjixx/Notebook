# 一、 ORM框架

## 1.1 什么是ORM

ORM也可以称为数据库持久层框架

对象-关系映射(Object-Relational Mapping 简称ORM)。目前**面向对象**的开发方法是企业级应用开发环境中的主流开发方法，**关系数据库**是企业级应用环境中存放数据的主流数据存储系统。

**对象和关系数据**是业务实体的两种表现形式，**业务实体在内存中表现为对象**，**在数据库中表现为关系数据。**

内存中的对象之间存在关联和继承关系，而在数据库中，关系数据无法直接表达多对多关联和继承关系。因此，对象-关系映射(ORM)系统一般以中间件的形式存在，主要实现**程序对象到关系数据库数据的映射**。

![ORM框架](https://img2020.cnblogs.com/blog/1342524/202005/1342524-20200521211715572-265303909.png)

## 1.2 为什么使用ORM？

对象关系映射（Object Relational Mapping，简称ORM），**主要实现程序对象到关系数据库数据的映射**

## 1.3 对象关系映射解释

- 简单：ORM以最基本的形式建模数据。比如ORM会将MySQL的一张表映射成一个Java类（模型），表的字段就是这个类的成员变量 

- 精确：ORM使所有的mysql数据表都按照统一的标准精确地映射成java类，使系统在代码层面保持准确统一 

- 易懂：ORM使数据库结构文档化。比如MySQL数据库就被ORM转换为了java程序员可以读懂的java类，java程序员可以只把注意力放在他擅长的java层面（当然能够熟练掌握MySQL更好） 

- 易用：ORM包含对持久类对象进行CRUD操作的API，例如create(), update(), save(), load(), find(), find_all(), where()等，也就是讲sql查询全部封装成了编程语言中的函数，通过函数的链式组合生成最终的SQL语句。通过这种封装避免了不规范、冗余、风格不统一的SQL语句，可以避免很多人为Bug，方便编码风格的统一和后期维护。

## 1.4 ORM优缺点

> **优点**

- 提高开发效率，降低开发成本 
- 使开发更加对象化 
- 可移植 
- 可以很方便地引入数据缓存之类的附加功能 

> **缺点**

- 自动化进行关系数据库的映射需要消耗系统性能。其实这里的性能消耗还好啦，一般来说都可以忽略之。 
- 在处理多表联查、where条件复杂之类的查询时，ORM的语法会变得复杂


# 二、JPA

## 2.1 基本概念

> **什么是JPA**
JPA(Java Persistence API)，JAVA持久层应用接口，是一个基于O/R映射的标准规范（目前最新版本是JPA 2.1 ）。所谓规范即只定义标准规则（如注解、接口），不提供实现，软件提供商可以按照标准规范来实现，而**使用者只需按照规范中定义的方式来使用**，而不用和软件提供商的实现打交道。

JPA是一套ORM规范，Hibernate实现了JPA规范！

![JPA规范与ORM框架之间的关系](https://img2018.cnblogs.com/i-beta/1543609/201911/1543609-20191119102137991-188046511.png)


> **JPA与JDBC的区别**

Java 持久层框架访问数据库的方式大致分为两种。一种以 SQL 核心，封装一定程度的 JDBC 操作，比如： MyBatis。另一种是以 Java 实体类为核心，将实体类的和数据库表之间建立映射关系，也就是我们说的ORM框架，如：Hibernate、Spring Data JPA。

本质而言，jdbc是数据库的统一接口标准，jpa是orm框架的统一接口标准。用法有区别，jdbc更注重数据库，orm则更注重于java代码，**但是实际上jpa实现的框架底层还是用jdbc去和数据库打交道**。

![JDBC示意图](https://upload-images.jianshu.io/upload_images/18864448-7ba78c82026a62d3.png?imageMogr2/auto-orient/strip|imageView2/2/w/629/format/webp)

![JPA示意图](https://upload-images.jianshu.io/upload_images/18864448-45da016e5d8f9997.png?imageMogr2/auto-orient/strip|imageView2/2/w/653/format/webp)

> **JPA、Spring Data JPA、Hibernate和Mybatis的区别**

- JPA是java持久化规范，是ORM框架的标准
- Spring Data JPA是对JPA规范的再次抽象，底层还是用的实现JPA的Hibernate技术
- Hibernate是一个标准的orm框架，实现jpa接口
- Mybatis也是一个持久化框架，但不完全是一个ORM框架，不是依照的jpa规范。

## 2.2 JPA提供的技术

- ORM映射元数据：JPA支持XML和JDK 5.0注解两种元数据的形式，元数据描述对象和表之间的映射关系，框架据此**将实体对象持久化到数据库表中**；

- JPA 的API：**定义规范，以操作实体对象**，执行CRUD操作，框架在后台替我们完成所有的事情，开发者从繁琐的JDBC和SQL代码中解脱出来。

- 查询语言：**通过面向对象而非面向数据库的查询语言查询数据**，避免程序的SQL语句紧密耦合。定义`JPQL`和`Criteria`两种查询方式。

## 2.3 实体生命周期

> **实体生命周期**
- New，新创建的实体对象，没有主键(identity)值
- Managed，对象处于Persistence Context(持久化上下文）中，被EntityManager管理
- Detached，对象已经游离到Persistence Context之外，进入Application Domain
- Removed, 实体对象被删除

> **EntityManager提供的管理实体对象的生命周期**

- persist, 将新创建的或已删除的实体转变为Managed状态，数据存入数据库。
- remove，删除受控实体
- merge，将游离实体转变为Managed状态，数据存入数据库。

如果使用了事务管理，则事务的commit/rollback也会改变实体的状态。

## 2.4 ID生成策略

> **JPA提供了如下几种ID生成策略**

- **GeneratorType.AUTO**，由JPA自动生成
  
- **GenerationType.IDENTITY**，使用数据库的自增长字段，需要数据库的支持（如SQL Server、MySQL、DB2、Derby等）
  
- **GenerationType.SEQUENCE**，使用数据库的序列号，需要数据库的支持（如Oracle
  
- **GenerationType.TABLE**，使用指定的数据库表记录ID的增长，需要定义一个TableGenerator，在@GeneratedValue中引用。
  
```java
// 定义TableGenerator
@TableGenerator( name=“myGenerator”, table=“GENERATORTABLE”, pkColumnName = “ENTITYNAME”, pkColumnValue=“MyEntity”, valueColumnName = “PKVALUE”, allocationSize=1)
// 在@GeneratedValue中引用
@GeneratedValue(strategy = GenerationType.TABLE,generator=“myGenerator”)
```

## 2.5 实体关系映射(ORM)

> **基本映射**

|   对象端   |    数据端    |   annotion    |   可选annotion    |
|   -----   |    -----    |    -----    |    -----    |
|   Class   |    Table    |    @Entity    |   @Table(name=“tablename”)    |
|   property   |    column    |   –    |   @Column(name = “columnname”)   |
|   property   |    primary key    |   @Id    |   @GeneratedValue 详见ID生成策略   |
|   property   |    NONE    |   @Transient    |      |

> **映射关系**

JPA如下四种关系
- one-to-one
- one-to-many
- many-to-one
- many-to-many 4种关系
  
可使用joinColumns来标注外键、使用 @Version来实现乐观锁。

**关联关系**还可以定制**延迟加载**和**级联操作**的行为

- 通过设置`fetch=FetchType.LAZY`或 `fetch=FetchType.EAGER`来决定关联对象是**延迟加载或立即加载。**
  
- 通过设置`cascade={options}`可以设置级联操作的行为
  - CascadeType.MERGE 级联更新
  - CascadeType.PERSIST 级联保存
  - CascadeType.REFRESH 级联刷新
  - CascadeType.REMOVE 级联删除
  - CascadeType.ALL 级联上述4种操作

> **查询方式**

- 对于简单的静态查询 - 可能优选基于字符串的JPQL查询（例如Named Queries）非查询类型安全
- 对于在运行时构建的动态查询 - 可能首选Criteria API查询类型安全,jpa动态查询方式，过程大致就是，创建builder => 创建Query => 构造条件 => 查询

```JAVA
/** JPQL */

//1.查询
TypedQuery<Country> query = em.createQuery("SELECT c FROM Country c", Country.class);
List<Country> results = query.getResultList();
//2.更新
Query query = em.createQuery("update Order as o set o.amount=o.amount+10");
query.executeUpdate();

/**Criteria */
//1.创建builder<script src="https://localhost01.cn/js/jquery-2.0.0.min.js"></script>
CriteriaBuilder builder = em.getCriteriaBuilder();
CriteriaQuery<Student> query = 
//2.创建Query
builder.createQuery(Student.class);
Root<Student> root = query.from(Student.class);
//3.构造条件
Predicate p1 = builder.like(root.<String> get("name"), "%" + student.getName() + "%");
Predicate p2 = builder.equal(root.<String> get("password"), student.getPassword());
query.where(p1, p2);
//4.查询
query.getRestriction();
```

# 二、Mybatis

## 2.1 Mybatis基本概念

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

## 2.2 Mybatis解析和运行原理
> **Mybatis工作原理**

![Mybatis工作流程](https://segmentfault.com/img/bVbMnUc)
> **Mybatis功能架构**

- **API接口层：** 提供给外部使用的接口API，开发人员通过这些本地API来操纵数据库。接口层一接收到调用请求就会调用数据处理层来完成具体的数据处理。
- **数据处理层：** 负责具体的SQL查找、SQL解析、SQL执行和执行结果映射处理等。它主要的目的是根据调用的请求完成一次数据库操作。
- **基础支撑层：** 负责最基础的功能支撑，包括连接管理、事务管理、配置加载和缓存处理，这些都是共用的东西，将他们抽取出来作为最基础的组件。为上层的数据处理层提供最基础的支撑。

![Mybatis功能架构](https://upload-images.jianshu.io/upload_images/9033085-45f641094a702061.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

## 2.3 Mybatis数据源与连接池

## 2.4 Mybatis 缓存


# 三、Hibernate

# 四、Spring Data JPA

spirng data jpa是spring提供的一套简化JPA开发的框架，按照约定好的【方法命名规则】写dao层接口，就可以在不写接口实现的情况下，实现对数据库的访问和操作。同时提供了很多除了CRUD之外的功能，如分页、排序、复杂查询等等。

Spring Data JPA 可以理解为 JPA 规范的再次封装抽象，底层还是使用了 Hibernate 的 JPA 技术实现。如图：

![](https://img2018.cnblogs.com/i-beta/1543609/201911/1543609-20191119102243558-811602737.png)

> Spring-Data-JPA核心接口
- crudRepository 继承了 Repository 接口，实现了CRUD的方法；
- PagingAndSortingRepository 继承了 Repository 接口，实现了分页排序的功能
- JpaRepository 继承了 PagingAndSortingRepoistory 接口，实现了JPA规范的相关方法
