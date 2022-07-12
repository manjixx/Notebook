# 1.了解SQL

- 数据库：保存有组织的数据的容器（通常是一个文件或一组文件）。

- 表：某种特定类型数据的结构化清单。数据库中表的名字应该是唯一的，不同数据库中表名可以相同

- 模式：用来描述数据库中特定的表以及整个数据库(和其中表的关系)。关于数据库和表的布局及特性的信息。

- 列：表中的一个字段。所有表都是由一个或多个列组成的。

- 数据类型：所容许的数据的类型。每个表列都有相应的数据类型，它限制（或容许）该列中存储的数据。

- 行：表中的一个记录。

- 主键：一列（或一组列），其值能够唯一区分表中每个行。
  - 任意两行都不具有相同的主键值；
  - 每个行都必须具有一个主键值（主键列不允许NULL值）。

- 主键使用习惯：
  - 不更新主键列中的值；
  -  不重用主键列的值；
  -  不在主键列中使用可能会更改的值。（例如，如果使用一个名字作为主键以标识某个供应商，当该供应商合并和更改其
名字时，必须更改这个主键。）

- SQL(Structured Query Language):结构化查询语言，专门用来与数据库通信的语言

# 2. MySQL简介

- MySQL是一种数据库管理系统DBMS，是一种数据库软件

- DBMS分为两种：
  - 基于共享文件系统的DBMS
  - 基于客户机—服务器的DBMS，MySQL、 Oracle以及Microsoft SQL Server等数据库是基于客户机—服
务器的数据库。客户机—服务器应用分为两个不同的部分。 服务器部分是负责所有数据访问和处理的一个软件。客户机是与用户打交道的软件

- MySQL工具
  - mysql命令行实用程序
    - 进入命令行使用工具后，使用；或\g结束
    - 输入 help 或者 \h 获取帮助
    - 输入 quit 或 exit 退出命令行实用工具 
  ```bash
  <!--完整的命令行选项和参数列表-->
  mysql --help
  ```
  
  - MySQL Administrator
  - MySQL Query Browser，用来编写和执行MySQL命令 

# 3. 使用MySQL

```SQL
<!--选择数据库-->
USE Database;

<!--查看允许的SHOW语句-->
HELP SHOW;

<!--显示数据库列表-->
SHOW DATABASES;

<!--显示数据库内的表  -->
SHOW TABLES;

<!--显示表列-->
SHOW CLOUMNS FROM tablename;

DESCRIBE tablename;

<!--显示服务器状态信息  -->
SHOW STATUS;

<!--显示创建特定的数据库语句-->
SHOW CREATE DATABASE;

<!--显示特定的创建表语句-->
SHOW CREATE TABLE;

<!-- 显示授予用户的安全权限 -->
SHOW GRANTS;

<!--显示服务器错误-->
SHOW ERRORS;

<!--显示服务器告警信息-->
SHOW WARNINGS;
```

# 4. 检索数据

```sql
<!-- 检索单个列-->
SELECT COLUMN FROM TABLENAME;

<!--检索多列-->
SELECT COLUMN1,COLUMN2,...,COLUMNN FROM TABLENAME;

<!--检索所有列-->
SELECT * FROM TABLENAME;

<!--检索不同的行-->
SELECT **DISTINCT** COLUMN FROM TABLENAME;

<!--限制结果-->
<!--结果不多于5行-->
SELECT COLUMN FROM TABLES 
LILMIT 5;

<!--开始检索的行和行数,从第5行开始的6行-->
SELECT COLUMN FROM TABLES 
LILMIT 5,6; 

<!--完全限定表名和列名-->
SELECT TABLE.CLOUMN FROM DATABASE.TABLE;

```

# 5. 排序检索数据

- 子句： SQL语句由子句构成，有些子句是必需的，而有的是可选的。一个子句通常由一个关键字和所提供的数据组成。FROM就是一种子句

```sql
<!--ORDER BY子句,排序数据-->
SELECT CLOUMN 
FROM TABLE
ORDER BY CLOUMN

<!--按多个列排序-->
<!-- 先按价格后按名称排序-->
SELECT PROD_ID, PROD_PRICE, PROD_NAME
FORM PRODUCT
ORDER BY PROD_PRICE, PROD_NAME

```
- 降序排序关键字 DESC,只应用到直接位于其前面的列。对多个列上进行降序排序的时候，必须对每个列指定DESC。

- 生序排序关键字ASC,但是升序是默认的。

```sql
<!--单列降序-->
SELECT PROD_ID, PROD_PRICE,PROD_NAME
FORM PRODUCT
ORDER BY PROD_PRICE DESC;

<!-- 多列中的一列进行排序-->
SELECT PROD_ID, PROD_PRICE,PROD_NAME
FORM PRODUCT
ORDER BY PROD_PRICE DESC, PROD_NAME;

<!--多列降序-->

SELECT PROD_ID, PROD_PRICE,PROD_NAME
FORM PRODUCT
ORDER BY PROD_PRICE DESC, PROD_NAME DESC;

```

# 6. 过滤数据

- 使用WHERE子句指定搜索条件

- 在SELECT 语句中，数据根据WHERE子句中指定的搜索条件进行过滤。

- WHERE子句在表名(FROM子句)之后,当与ORDER BY同时使用时，应该让ORDER BY位于 WHERE语句之后。

- WHERE 子句操作符
  - =       等于
  - <>      不等于
  - !=      不等于
  - <       小于
  - <=      小于等于
  - >       大于
  - >=      大于等于
  - BETWEEN 在给定的两个值之间,包括开始值和结束值

```sql
<!--检查单个值-->
SELECT PROD_NAME, PROD_PRICE
FROM PRODUCTS
WHERE PROD_NAME = 'Fuses';

<!--小于某个值-->
SELECT PROD_NAME,PROD_PRICE
FORM PRODUCT
WHERE PROD_PRICE < 10;

<!--小于等于某个值-->
SELECT PROD_NAME, PROD_PRICE
FROM PRODUCTS
WHERE PROD_PRICE <= 10;

<!--不匹配检查，不等于检查-->
SELECT PROD_NAME,PROD_PRICE
FROM PRODUCTS
WHERE PROD_NAME != 1000;


SELECT PROD_NAME,PROD_PRICE
FROM PRODUCTS
WHERE PROD_NAME <> 1000;

<!--检查范围内的值-->
SELECT PROD_NAME,PROD_PRICE
FORM PRODUCTS
WHERE PROD_PRICE BETWEEN 5 AND 10;

<!--空值检查-->
SELECT PROD_NAME
FROM PRODUCTS
WHERE PROD_PRICE IS NULL;
```

# 7. 数据过滤

- 组合WHERE子句:MySQL允许给出多个WHERE子句。这些子句以两种方式使用，以AND子句的方式或OR子句的方式使用

- 操作符(operator):用来联结或者改变WHERE子句中的子句关键字，也称为逻辑操作符(logic operator);

- AND: 用在WHERE子句中的关键字，用来指示检索满足所有给定条件的行

- OR：表示匹配任一条件的行

- AND 优先级 高于 OR

- IN:对圆括号中的任一条件进行匹配

- NOT：否定其后所跟的任何条件


# 8. 使用通配符进行过滤

# 9. 使用正则表达式进行搜索

# 10. 创建计算字段

# 11. 使用数据处理函数

# 12. 汇总数据

# 13. 分组数据

# 14. 使用子查询

# 15. 连结表

# 16. 创建高级连结

# 17. 组合查询

# 18. 全文本搜索

# 19. 插入数据

# 20. 更新和删除数据

# 21. 创建和操纵表

# 22. 使用视图

# 23. 使用存储过程

# 24. 使用游标

# 25. 使用触发器

# 26. 管理事务

# 27. 全球化和本地话

# 28. 安全管理

# 29. 数据库维护

# 30. 改善性能
