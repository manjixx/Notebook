# MySQL测试方法

- 测试正则表达式
  
在不使用数据库表的情况下可以用SELECT来测试正则表达式，REGEXP检查总是返回0(没有匹配)或1(匹配)

```SQL
  SELECT 'hello' REGEXP '[0-9]';
```

- 测试计算

```SQL
/*返回abc*/
SELECT Trim('abc');

/*当前日期和时间*/
SELECT Now();

/*返回6*/
SELECT(3*2);
```

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
  --完整的命令行选项和参数列表--
  mysql --help
  ```
  
  - MySQL Administrator
  - MySQL Query Browser，用来编写和执行MySQL命令 

# 3. 使用MySQL

```SQL
/*选择数据库*/
USE Database;

/*查看允许的SHOW语句 */
HELP SHOW;

/*显示数据库列表 */
SHOW DATABASES;

/* 显示数据库内的表   */
SHOW TABLES;

/* 显示表列 */
SHOW CLOUMNS FROM tablename;

DESCRIBE tablename;

/* 显示服务器状态信息 */
SHOW STATUS;

/* 显示创建特定的数据库语句 */
SHOW CREATE DATABASE;

/* 显示特定的创建表语句 */
SHOW CREATE TABLE;

/* 显示授予用户的安全权限 */
SHOW GRANTS;

/* 显示服务器错误 */
SHOW ERRORS;

/* 显示服务器告警信息 */
SHOW WARNINGS;
```

# 4. 检索数据

```sql
/*  检索单个列 */
SELECT COLUMN FROM TABLENAME;

/* 检索多列 */
SELECT COLUMN1,COLUMN2,...,COLUMNN FROM TABLENAME;

/* 检索所有列 */
SELECT * FROM TABLENAME;

/* 检索不同的行 */
SELECT **DISTINCT** COLUMN FROM TABLENAME;

/* 限制结果 */
/* 结果不多于5行 */
SELECT COLUMN FROM TABLES 
LILMIT 5;

/* 开始检索的行和行数,从第5行开始的6行 */
SELECT COLUMN FROM TABLES 
LILMIT 5,6; 

/* 完全限定表名和列名-->
SELECT TABLE.CLOUMN FROM DATABASE.TABLE;

```

# 5. 排序检索数据

- 子句： SQL语句由子句构成，有些子句是必需的，而有的是可选的。一个子句通常由一个关键字和所提供的数据组成。FROM就是一种子句

```sql
/* ORDER BY子句,排序数据 */
SELECT CLOUMN 
FROM TABLE
ORDER BY CLOUMN;

/* 按多个列排序 */
/*  先按价格后按名称排序 */
SELECT PROD_ID, PROD_PRICE, PROD_NAME
FORM PRODUCT
ORDER BY PROD_PRICE, PROD_NAME

```
- 降序排序关键字 DESC,只应用到直接位于其前面的列。对多个列上进行降序排序的时候，必须对每个列指定DESC。

- 生序排序关键字ASC,但是升序是默认的。

```sql
/* 单列降序 */
SELECT PROD_ID, PROD_PRICE,PROD_NAME
FORM PRODUCT
ORDER BY PROD_PRICE DESC;

/*  多列中的一列进行排序 */
SELECT PROD_ID, PROD_PRICE,PROD_NAME
FORM PRODUCT
ORDER BY PROD_PRICE DESC, PROD_NAME;

/* 多列降序 */

SELECT PROD_ID, PROD_PRICE,PROD_NAME
FORM PRODUCT
ORDER BY PROD_PRICE DESC, PROD_NAME DESC;

```

# 6. 过滤数据

- 使用WHERE子句指定搜索条件

- 在SELECT 语句中，数据根据WHERE子句中指定的搜索条件进行过滤。

- WHERE子句在表名(FROM子句)之后,当与ORDER BY同时使用时，**应该让ORDER BY位于 WHERE语句之后**。

- WHERE 子句操作符
  - =       等于
  - <>      不等于
  - !=      不等于
  - <       小于
  - <=      小于等于
  - \>       大于
  - \>=      大于等于
  - BETWEEN 在给定的两个值之间,包括开始值和结束值

```sql
/* 检查单个值 */
SELECT PROD_NAME, PROD_PRICE
FROM PRODUCTS
WHERE PROD_NAME = 'Fuses';

/* 小于某个值 */
SELECT PROD_NAME,PROD_PRICE
FORM PRODUCT
WHERE PROD_PRICE < 10;

/* 小于等于某个值 */
SELECT PROD_NAME, PROD_PRICE
FROM PRODUCTS
WHERE PROD_PRICE <= 10;

/* 不匹配检查，不等于检查 */
SELECT PROD_NAME,PROD_PRICE
FROM PRODUCTS
WHERE PROD_NAME != 1000;


SELECT PROD_NAME,PROD_PRICE
FROM PRODUCTS
WHERE PROD_NAME <> 1000;

/* 检查范围内的值 */
SELECT PROD_NAME,PROD_PRICE
FORM PRODUCTS
WHERE PROD_PRICE BETWEEN 5 AND 10;

/* 空值检查 */
SELECT PROD_NAME
FROM PRODUCTS
WHERE PROD_PRICE IS NULL;
```

# 7. 数据过滤

- 组合WHERE子句:MySQL允许给出多个WHERE子句。这些子句以两种方式使用，以AND子句的方式或OR子句的方式使用

- 操作符(operator):用来联结或者改变WHERE子句中的子句关键字，也称为逻辑操作符(logic operator);

- AND: 用在WHERE子句中的关键字，用来指示检索满足所有给定条件的行, 添加多个过滤条件，每添加一条就要使用一个AND。

- OR：表示匹配任一条件的行

- AND 优先级 高于 OR

- IN: Z指定条件范围，对圆括号中的任一条件进行匹配

- NOT：否定其后所跟的任何条件

```SQL
/*  AND附加条件  */
SELECT PROD_ID,PROD_PRICE,PROD_NAME
FORM PRODUCTS
WHERE VEND_ID = 1003 AND PRDE_PRICE <= 10;

/*  OR操作符  */

SELECT PROD_NAME PROD_PRICE
FROM PRODUCT
WHERE VEND_ID = 1002 OR VEND_ID = 1003

/*  计算由1002或1003制作且价格为10美元以上的商品  */

SELECT PROD_NAME PROD_PRICE
FORM PRODUCT
WHERE (VEND_ID = 1002 OR VEND_ID = 1003) AND PROD_PRICE >= 10;

/*  IN操作符  */
SELECT PROD_NAME,PROD_PRICE
FORM PRODUCT
WHERE VEND_ID IN (1002,1003)
ORDER BY PROD_NAME;

/*  NOT 操作符  */
SELECT PROD_NAME,PROD_PRICE
FROM PRODUCT
WHERE VEND_ID NOT IN (1002,1003)
ORDER BY PROD_NAME;

```

# 8. 使用通配符进行过滤


## LIKE操作符

- 通配符：用来匹配值得一部分的特殊字符

- 搜索模式：由字面值、通配符或者两者组合形成的搜索条件

### SQL常见通配符
- 百分号通配符 % ： 表示任何字符出现任意次数
- 下化线通配符 _ : 其用途与%一致，但是表示只匹配单个字符而不是多个字符

```sql
/*  % 通配符  */
/*  该语句表示匹配开头为jet的任意商品名  */
SELECT PROD_NAME,PROD_PRICE
FORM PRODUCT
WHERE PROD_NAME LIKE 'jet%';

/*  _ 通配符  */
/*  表示匹配开头为jet其后一个字符为任意字符的商品名  */
SELECT PROD_NAME,PROD_PRICE
FROM PRODUCT
WHERE PROD_NAME LIKE 'jet_';
```

# 9. 使用正则表达式进行搜索

- REGEXP：正则表达关键字

## 基本字符匹配

- REGEXP与LIKE的区别
  - REGEXP 在列值内匹配，如果被匹配的文本在列值中出现，REGEXP将会找到它，相应的行将被返回
  - LIKE匹配整列，如果被匹配的文本在列值中出现，LIKE也不会找到它，相应的行也不会被返回（除非使用通配符）
 
- . 在正则表达式中表示匹配任意一个字符
```sql
/*  一般正则表达式的使用  */
SELECT PROD_NAME
FORM PRODUCTS
WHERE PROD_NAME REGEXP '1000'
ORDER BY PROD_NAME;

/*  正则表达式中 . 的使用  */
SELECT PROD_NAME
FORM PRODUCTS
WHERE PROD_NAME REGEXP '.000'
ORDER BY PROD_NAME;

```

## 进行OR匹配
- 为搜索两个串之一(或者为整个串，或者为另一个串)，使用 | 

- 两个以上的OR条件，'1000 | 2000 | 3000'将匹配1000或2000或3000

```sql
/*  匹配其中之一 */
SELECT PROD_NAME 
FORM PRODUCTS
WHERE PROD_NAME REGEXP '1000 | 2000'
ORDER BY PROD_NAME;
```

## 匹配几个字符之一

- REGEXP '[123] TON' 表示匹配1或2或3

- '[123] TON' 是 '[1|2|3] TON'的简写，注意此处[]不可省略，否则表示1或2或3 TON

- 否定字符集合，匹配除指定字符集合意外的任何东西 '[^123] TON',表示除 1 TON, 2 TON, 3 TON以外的所有字段

```sql
SELECT PROD_NAME
FORM PRODUCTS
WHERE PROD_NAME REGEXP '[123] TON';

```

## 匹配范围
- [0-9] 表示将匹配[0123456789]
- [a-z]匹配任意字母字符

```sql
SELECT PROD_NAME
FROM PRODUCTS
WHERE PROD_NAME REGEXP '[1-5] TON'
ORDER BY PROD_NAME;
```

## 匹配特殊字符
```sql
SELECT PROD_NAME
FROM PRODUCTS
WHERE PROD_NAME REGEXP '[1-5] TON'
ORDER BY PROD_NAME;

/*  输出结果为 
  .5 ton anvil  
  1 ton anvil 
  2 ton anvil
  其中.5 ton anvil由于5 ton匹配，所以返回 .5 ton
 */
```

## 匹配特殊字符

- 现阶段接触到的特殊字符 . [] | -
- 如果需要匹配这些特殊字符则必须以\\为前导

- \\也用来引用元字符
  -  \\f 换页
  -  \\n 换行
  -  \\r 回车
  -  \\t 制表
  -  \\v 纵向制表

- \ 或\\?
  
  多数正则表达式使用单个反斜杠转义特殊字符，以便能使用这些字符本身，但MySQL要求两个反斜杠，MySQL自己解释一个，正则表达式库解释另一个
  
```sql
/* 正则匹配 . */
SELECT VEND_NAME
FROM VENDORS
WHERE VENDER_NAME REGEXP '\\.'
ORDER BY VEND_NAME;

```

## 匹配字符类

- 为方便期间可以将自己经常使用的数字、所有字母字符或所有数字字母字符等的匹配。可以使用预定义的字符集，称为字符类

- 字符类
  - [:alnum:] 任意字母和数字，同[a-zA-Z0-9]
  - [:alpha:] 任意字符,同[a-zA-Z]
  - [:blank:] 空格和制表，同[\\t]
  - [:cntrl:] ASCII控制字符(ASCII 0到31 和 127)
  - [:digit:] 任意数字(同[0-9])
  - [:graph:] 与[:print:]相同，但不包括空格
  - [:lower:] 任意小写字母(同[a-z])
  - [:print:] 任意可打印字符
  - [:punct:] 既不在[:alnum:]又不在[:cntrl:]中的任意字符
  - [:sapce:] 包括空格在内的任意空白字符(同[\\f\\n\\r\\t\\v])
  - [:upper:] 任意大写字母(同[A-Z])
  - [:xdigit:] 任意十六进制数字(同[a-fA-F0-9])

## 匹配多个实例
- 正则表达式重复元字符
  - *     0个或多个匹配
  - +     1个或多个匹配,等于{1,}
  - ?     0个或1个匹配，等于{0,1}
  - {n}   指定匹配数目
  - {n,}  不少于指定数目的匹配
  - {n,m} 匹配数目范围(m不超过255）
```sql
/* '\\([0-9] sticks?\\)'
    \\(     匹配(
    [0-9]   匹配任意数字
    sticks? 匹配stick和sticks,因为s后的?表示s可以出现0次或者1次
    \\)     匹配)
*/
SELECT PROD_NAME
FROM PRODUCTS
WHERE PROD_NAME REGEXP '\\([0-9] sticks?\\)'
ORDER BY PROD_NAME;

/*
  匹配任意4位数字
  '[[:digit:]]{4}'
    [:digit:] 匹配任意数字
    {4} 要求它前面的字符任意数字出现4次
*/
SELECT PROD_NAME
FROM PRODUCTS
WHERE PROD_NAME REGEXP '[[:digit:]]{4}'
ORDER BY PROD_NAME;

SELECT PROD_NAME
FROM PRODUCTS
WHERE PROD_NAME REGEXP '[0-9][0-9][0-9][0-9]'
ORDER BY PROD_NAME;
```

## 定位符

- 为了匹配特定位置的文本，需要使用定位元字符
  - ^       文本的开始
  - $       文本的结尾
  - [[:<:]] 词的开始
  - [[:>:]] 词的结尾

- ^ 的双重用法：在集合中用来否定该集合(集合用[和]定义)，否则用来指示串的开始。

- 通过使用 ^ 与 $ 可以是REGEXP达到与LIKE一样的效果
 
```sql
/*匹配以0-9或者.开始商品名*/

SELECT PROD_NAME
FROM PRODUCTS
WHERE PROD_NAME REGEXP '^[0-9\\.]'
ORDER BY PROD_NAME;

```

# 10. 创建计算字段

## 计算字段
- 计算字段实际并不存在于数据库表中，计算字段是运行时在SELECT语句内创建的

- 字段(filed)基本上与列(column)的意思相同，经常互换使用，不过数据库列一般称为列，而术语字段通常用在计算字段的连接上

## 拼接字段

- 拼接(concatenate):将值连接在一起构成单个值

- MySQL使用 Concat()函数来拼接两个列

- 注：多数DBMS使用+或||来实现拼接，MySQL则使用Concat()函数来实现

```sql
/* 拼接供应商(位置)信息*/

SELECT Concat(VENDER_NAME, '(', VENDER_CONTORY ,')')
FROM VENDORS
ORDER BY VEND_NAME;
```

> 分析：Concat(VENDER_NAME, '(' VENDER_CONTORY ')') 连接如下4个元素
>   - 存储在vend_name列中的名字；
>   - 包含一个空格和一个左圆括号的串；
>   -  存储在vend_country列中的国家；
>   -  包含一个右圆括号的串。

- RTrim()函数去掉值右边的所有空格。通过使用RTrim()，各个列都进行了整理
- LTrim()函数去掉值左边的所有空格。

- 别名(alias)：是一个字段或值得替换名，别名用关键字AS赋予

```sql
SELECT Concat(RTrim(VEND_NAME), '(' , RTrim(VEND_COUNTRY), ')') AS VEND_TITLE
FORM VENDORS
ORDER BY VEND_NAME;
```

## 执行算术计算
```sql
SELECT PROD_ID,
       QUANTITY,
       QUANTITY * ITEM_PRICE AS EXPANDED_PRICE
FROM ORDERITEMS
WHERE ORDER_NUM = 20005;
```

- MySQL计算操作符
  - + 加
  - - 减
  - * 乘
  - / 除
    
# 11. 使用数据处理函数

- 多数SQL语句是可移植的，在SQL实现之间有差异时，这些差异通常不那么难处理。而函数的可移植性却不强。几乎每种主要的DBMS的实现都支持其
他实现不支持的函数，而且有时差异还很大。 

## 使用函数

- 大多数SQL支持实现以下类型的函数
  - 用于处理文本串（如删除或填充值，转换值为大写或小写）的文本函数。
  - 用于在数值数据上进行算术操作（如返回绝对值，进行代数运算）的数值函数。
  - 用于处理日期和时间值并从这些值中提取特定成分（例如，返回两个日期之差，检查日期有效性等）的日期和时间函数。
  - 返回DBMS正使用的特殊信息（如返回用户登录信息，检查版本细节）的系统函数。

### 文本处理函数
```sql
SELECT vend_name, Upper(vend_name) AS vend_name_upcase
FROM vendors
ORDER BY vend_name;
```
- 常见的文本处理函数
  - Left()    返回串左边的字符
  - Length()  返回串的长度
  - Locate()  找回串的第一个子串  
  - Lower()   将串转换为小写
  - LTrim()   去掉串左边的空格
  - Right()   返回串右边的字符
  - RTrim()   去掉串右边的空格
  - Soundex() 返回串的SOUNDEX值
  - Upper()   将串转换为大写
 
- SOUNDEX：是一个将任何文本串转换为描述其语音表示的字母数字模式的算法。SOUNDEX考虑了类似的发音字符和音节，使得能对串进行发音比较而不是字母比较。

```sql
/*soundex*/
```

### 日期和时间处理函数

- 常见的日期和时间处理函数
  - AddDate()     增加一个日期（天、周等）
  - AddTime()     增加一个时间（时、分等）
  - CurDate()     返回当前日期
  - CurTime()     返回当前时间
  - Date()        返回日期时间的日期部分
  - DateDiff()    计算两个日期之差
  - Date_Add()    高度灵活的日期运算函数
  - Date_Format() 返回一个格式化的日期或时间串
  - Day()         返回一个日期的天数部分
  - DayOfWeek()   对于一个日期，返回对应的星期几
  - Hour()        返回一个时间的小时部分
  - Minute()      返回一个时间的分钟部分
  - Month()       返回一个日期的月份部分
  - Now()         返回当前日期和时间
  - Second()      返回一个时间的秒部分
  - Time()        返回一个日期时间的时间部分
  - Year()        返回一个日期的年份部分

```sql
/* 基本日期查询 但该种查询方式不可靠，因为表格中时间值不可能全部是00:00:00 */
SELECT cust_id,order_num
FROM ORDERS
WHERE order_date = '2005-09-01';

/*解决方法：使用Date()函数对日期进行检索*/
SELECT cust_id,order_num
FORM ORDERS
WHERE Date(order_data) = '2005-09-01';

/*查询2005年9月份下的所有订单*/

/*方式一*/
SELECT cust_id, order_num
FROM orders
WHERE Year(order_date) = 2005 AND Month(oreder_data) = 9;

/*方式二*/
SELECT cust_id, order_num
FROM orders
WHERE order_date BETWEEN '2005-09-01' AND '2005-09-30';
```

### 日期和时间处理函数

- 数字处理函数
  - Abs() 返回一个数的绝对值
  - Cos() 返回一个角度的余弦
  - Exp() 返回一个数的指数值
  - Mod() 返回除操作的余数
  - Pi() 返回圆周率
  - Rand() 返回一个随机数
  - Sin() 返回一个角度的正弦
  - Sqrt() 返回一个数的平方根
  - Tan() 返回一个角度的正切
 
# 12. 汇总数据

- 汇总数据而不用把它们实际检索出来，为此MySQL提供了专门的函数。使用这些函数，MySQL查询可用于检索数据，以便分析和报表生成。这种类型的检索例子有以下几种：
  - 确定表中行数
  - 获得表中行组的和
  - 找出表列的最大值、最小值和平均值

- 聚集函数：运行在行组上，计算和返回单个值的函数

- SQL聚集函数
  - AVG()   返回某列的平均值
  - COUNT() 返回某列的行数
  - MAX()   返回某列的最大值
  - MIN()   返回某列的最小值
  - SUM()   返回某列值之和   

## AVG()函数

AVG()通过对表中行数计数并计算特定列值之和，求得该列的平均值。AVG()可用来返回所有列的平均值，也可以用来返回特定列或行的平均值。

```sql
/*返回所有产品的平均价格*/
SELECT AVG(prod_price) AS avg_price
FROM products;

/ *确定特定列或行的平均值*/
SELECT AVG(prod_price) AS avg_price
FROM products
WHERE vend_id = 1003;
```

- 只用于单个列 AVG()只能用来确定特定数值列的平均值，而且列名必须作为函数参数给出。为了获得多个列的平均值，必须使用多个AVG()函数。

- NULL值 AVG()函数忽略列值为NULL的行

## COUNT()函数

- COUNT()函数可以进行计数，可以确定表中行的数目或者符合特定条件的行的数目

- COUNT()函数有两种使用方式
  - 使用COUNT(\*) 对表中行的数目进行计数，不管表列中包含的是空值（NULL）还是非空值

  - 使用COUNT(column)对特定列中具有值得行进行计数，忽略NULL值
  
```sql
SELECT COUNT(*) AS num_cust
FROM customers
 
SELECT COUNT(cust_email) AS num_cust
FROM customers;
```

## MAX()函数

- MAX()返回指定列中的最大值，MAX()要求指定列名

```sql
SELECT MAX(prod_price) AS max_price
FROM products
```

- 对非数值数据使用MAX() 虽然MAX()一般用来找出最大的数值或日期值，但MySQL允许将它用来返回任意列中的最大值，包括返回文本列中的最大值。在用于文本数据时，如果数据按相应的列排序，则MAX()返回最后一行

- NULL值 MAX()函数忽略列值为NULL的行

## MIN()函数

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

[设计数据密集型应用 - 中文翻译](https://github.com/Vonng/ddia)
