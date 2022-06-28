
# 1.项目需求

## java题目一
- 现有一组无序无规律的中国各城市基础信息数据，经过简单的处理后被写进了一个excel表格，现在需要你获取到数据做进一步处理：
  - 1. 对所有的数据以行为单位，按照城市名称首字母进行排序（A->Z）;
  - 2. 城市首字母相同的情况下，按照GDP数据由大到小进行排序；
  - 3. 将处理之后的数据，写进sqlite数据库中，列名与excel表保持一致。

- 注意：
  - 1. 读取数据时应该做基本的无效数据过滤，比如Population 和 GDP不能为负数
  - 2. 数据库表明可以自定义。

## java题目二
- 现已做好前端，请根据前端的访问，利用Spring boot做框架，实现一个Web应用系统，接受前端的访问请求，具备如下子功能：
  - 1. 返回Java编程题目1所创建的数据库中存放的全部城市信息。
  - 2. 根据前端城市名称参数，来搜索并返回前端指定访问的城市信息。

- 注意：
  - 1. 以JSON形式返回信息给客户端
  ```JSON
  {
    "code": "200",
	  "count": "10",
    "cityInfo":
      [
          {"NO":xxx,"City_Name":"xxxx","Region":xxx,"Population":xxx,"GDP":xxx,"Remarks":"xxx"},
           .........
          {"NO":xxx,"City_Name":"xxxx","Region":xxx,"Population":xxx,"GDP":xxx,"Remarks":"xxx"}
      ]
  }
  ```
  - 2. 指定访问的信息只有一条
  ```JSON
     {"NO":xxx,"City_Name":"xxxx","Region":xxx,"Population":xxx,"GDP":xxx,"Remarks":"xxx"}
  ```
  - 3. JSON对象的定义为：
  - 4. uri:/ota/queryCityInfo?cityname=xi'an

# 2.环境配置
- Navigator 

- 建表语句
```sql
create table city(
   no int auto_increament primary key not null,
   city_name varchar(50),
   region int,
   population int,
   gdp int,
   comment text
 );
 ```
- insert
```sql
	insert into city (`no`,`city_name`,`region`,`population`,`gdp`,`comment`)
   		values(1,"Xi'an",4,10000,8568346,"");
```




#
