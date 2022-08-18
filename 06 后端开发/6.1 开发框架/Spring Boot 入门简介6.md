
# 六、数据访问

## 1、整合JDBC数据源

1、新建项目 spring-boot-06-data-jdbc

- WEB
- Mysql
- JDBC
- SpringBoot1.5

2、编写配置文件appliction.yml

```yaml
spring:
  datasource:
    username: root
    password: Welcome_1
    url: jdbc:mysql://192.168.179.131:3306/jdbc
    driver-class-name: com.mysql.jdbc.Driver
```

3、编写测试类测试

```java
@RunWith(SpringRunner.class)
@SpringBootTest
public class SpringBoot06DataJdbcApplicationTests {

    @Autowired
    DataSource dataSource;

    @Test
    public void contextLoads() throws SQLException {
        System.out.println(dataSource.getClass());

        Connection connection = dataSource.getConnection();
        System.out.println(connection);
        connection.close();
    }

}
```

4、测试结果

```
class org.apache.tomcat.jdbc.pool.DataSource
ProxyConnection[PooledConnection[com.mysql.jdbc.JDBC4Connection@c35af2a]]
```

数据源相关配置都在DataSourceProperties属性里

自动配置原理

E:\Develop\Maven_Repo\org\springframework\boot\spring-boot-autoconfigure\1.5.13.RELEASE\spring-boot-autoconfigure-1.5.13.RELEASE.jar!\org\springframework\boot\autoconfigure\jdbc

### 1、DataSource

参考DataSourceConfiguration,根据配置创建数据源，默认是使用tomcat连接池，可以使用spring.datasource.type指定自定义的数据源

### 2、SpringBoot默认支持

```
Tomcat数据源
HikariDataSource
dbcp.BasicDataSource
dbcp2.BasicDataSource
```

### 3、自定义数据源

```java
 */
@ConditionalOnMissingBean(DataSource.class)
@ConditionalOnProperty(name = "spring.datasource.type")
static class Generic {

   @Bean
   public DataSource dataSource(DataSourceProperties properties) {
       //使用builder创建数据源，利用反射创建相应的type数据源，并绑定数据源
      return properties.initializeDataSourceBuilder().build();
   }

}
```

### 4、运行sql建表

在DataSourceAutoConfiguration中**DataSourceInitializer**类

监听器

作用：

1）、postConstruct -》runSchemaScript 运行建表sql文件

2）、runDataScript运行插入数据的sql语句；

默认只需要将文件命名为：

```sql
schema-*.sql data-*.sql
默认规则：schema.sql ,schema-all.sql;
```

**举个栗子**

创建department表

1、department.sql

```sql
/*
Navicat MySQL Data Transfer

Source Server         : 192.168.179.131
Source Server Version : 50719
Source Host           : 192.168.179.131:3306
Source Database       : jdbc

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2018-05-14 14:28:52
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for department
-- ----------------------------
DROP TABLE IF EXISTS `department`;
CREATE TABLE `department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `departmentName` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

```

2、将department.sql命名为schema-all.sql

![45.schema-all](E:\工作文档\SpringBoot\images\45.schema-all.jpg)

3、运行测试类

自定义sql的文件名，department.sql在配置文件中

```yaml
schema:
  - classpath:department.sql
```

-----

### 5、操作JdbcTemplate

**FBI warning**:将department.sql删除或者改名，因为运行文件会将表中数据清除

1、新建一个Controller

```java
@Controller
public class HelloController {

    @Autowired
    JdbcTemplate jdbcTemplate;

    @ResponseBody
    @GetMapping("/hello")
    public Map<String ,Object> hello(){

        List<Map<String, Object>> list = jdbcTemplate.queryForList("select * from department");
        return list.get(0);
    }
}
```

2、表中添加数据

![46.department](E:\工作文档\SpringBoot\images\46.department.jpg)



3、访问请求查询数据

![47.hello](E:\工作文档\SpringBoot\images\47.hello.jpg)



## 2、自定义数据源

1、导入Druid的依赖

```xml
<!-- https://mvnrepository.com/artifact/com.alibaba/druid -->
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid</artifactId>
    <version>1.1.9</version>
</dependency>

```

2、修改配置文件

```yaml
spring:
  datasource:
    username: root
    password: Welcome_1
    url: jdbc:mysql://192.168.179.131:3306/jdbc
    driver-class-name: com.mysql.jdbc.Driver
    type: com.alibaba.druid.pool.DruidDataSource
#    schema:
#      - classpath:department.sql
server:
  port: 9000
```

已经替换了原来的tomcat数据源

3、配置Druid数据源配置

```yaml
spring:
  datasource:
    username: root
    password: Welcome_1
    url: jdbc:mysql://192.168.179.131:3306/jdbc
    driver-class-name: com.mysql.jdbc.Driver
    type: com.alibaba.druid.pool.DruidDataSource
	# 初始化大小，最小，最大  
    initialSize: 5
    minIdle: 5
    maxActive: 20
    # 配置获取连接等待超时的时间  
    maxWait: 60000
    # 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒 
    timeBetweenEvictionRunsMillis: 60000
    # 配置一个连接在池中最小生存的时间，单位是毫秒 
    minEvictableIdleTimeMillis: 300000
    validationQuery: SELECT 1 FROM DUAL
    testWhileIdle: true
    testOnBorrow: false
    testOnReturn: false
    poolPreparedStatements: true
    # 配置监控统计拦截的filters,去掉监控界面sql无法统计，‘wall’用于防火墙
    filters: stat,wall,log4j
    maxPoolPreparedStatementPerConnectionSize: 20
    userGlobalDataSourceStat: true
    # 通过connectProperties属性来打开mergeSql功能；慢SQL记录  
    connectionProperties: druid.stat.mergeSql=true;druid.stat.slowSqlMillis=500
#    schema:
#      - classpath:department.sql
server:
  port: 9000
```

4、Druid配置监控

```java
@Configuration
public class DruidConfig {

    @ConfigurationProperties(prefix = "spring.datasource")
    @Bean
    public DataSource druid(){
        return  new DruidDataSource();
    }

    //配置Druid的监控
    //1、配置一个管理后台
    @Bean
    public ServletRegistrationBean statViewServlet(){
        ServletRegistrationBean bean = new ServletRegistrationBean(new StatViewServlet(),"/druid/*");
        Map<String,String> initParams =new HashMap<>();
        initParams.put("loginUsername", "admin");
        initParams.put("loginPassword", "123456");
        bean.setInitParameters(initParams);
        return bean;
    }
    //2、配置监控的filter
    @Bean
    public FilterRegistrationBean webstatFilter(){
        FilterRegistrationBean bean = new FilterRegistrationBean();
        bean.setFilter(new WebStatFilter());

        Map<String,String> initParams =new HashMap<>();
        initParams.put("exclusions", "*.js,*.css,/druid/*");
        bean.setInitParameters(initParams);
        bean.setUrlPatterns(Arrays.asList("/*"));
        return bean;
    }

}
```

5、运行测试，访问 localhost:9000/druid

![48.druid](E:\工作文档\SpringBoot\images\48.druid.jpg)

输入刚才调好的用户名密码即可访问

## 3、整合Mybatis

1、新建工程，SpringBoot1.5+web+JDBC+Mysql

导入依赖

```xml
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>1.3.2</version>
</dependency>
<!-- https://mvnrepository.com/artifact/com.alibaba/druid -->
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid</artifactId>
    <version>1.1.9</version>
</dependency>
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>
```

2、导入配置文件中关于Druid的配置

​	2.1、导入依赖

​	2.2、配置文件application.yml（指定用户名密码...配置Druid的配置参数，修改sql文件加载的默认名）

​	2.3、将Druid组件加入到容器中（监控）重点

​	具体同上

3、创建数据表department和employee表

​	3.1、根据sql文件，新建两张表

​	3.2、修改加载的sql名（默认为schema.sql和schema-all.sql）

```yaml
spring:
  datasource:
    schema:
      - classpath:sql/department.sql
      - classpath:sql/employeee.sql
```

​	3.3、运行程序检查数据库是否创建成功

4、创建数据库对应的JavaBean （驼峰命名，getter/setter toString/注释掉schema防止重复创建） 

在配置文件中修改驼峰命名开启 ,不写配置文件就写配置类

```yaml
mybatis:
  configuration:
    map-underscore-to-camel-case: true
```

```java
//类名冲突所以全类名
@org.springframework.context.annotation.Configuration
public class MyBatisConfig {

    @Bean
    public ConfigurationCustomizer configurationCustomizer(){

        return new ConfigurationCustomizer() {
            @Override
            public void customize(Configuration configuration) {
                configuration.setMapUnderscoreToCamelCase(true);
            }
        };
    }
}
```

### 注解方式

5、新建mapper

```yaml
//指定是一个mapper
@Mapper
public interface DepartmentMapper {

    @Insert("insert into department(dept_name) value(#{deptName})")
    public int insertDept(Department department);

    @Delete("delete from department where id=#{id}")
    public int deleteDeptById(Integer id);

    @Update("update department set dept_Name=#{deptName} where id=#{id}")
    public int updateDept(Department department);

    @Select("select * from department where id=#{id}")
    public Department getDeptById(Integer id);

}
```

6、编写controller测试

```java
@RestController
public class DeptController {

    @Autowired
    DepartmentMapper departmentMapper;

    @RequestMapping("/getDept/{id}")
    public Department getDepartment(@PathVariable("id") Integer id){
        return departmentMapper.getDeptById(id);
    }

    @RequestMapping("/delDept/{id}")
    public int delDept(@PathVariable("id") Integer id){
        return departmentMapper.deleteDeptById(id);
    }

    @RequestMapping("/update/{id}")
    public int updateDept(@PathVariable("id") Integer id){
        return departmentMapper.updateDept(new Department(id, "开发部"));
    }

    @GetMapping("/insert")
    public int insertDept(Department department){
        return departmentMapper.insertDept(department);
    }
}
```

问题：

mapper文件夹下有多个mapper文件，加麻烦，可以直接扫描整个mapper文

件夹下的mapper

```java
//主配置类或者mybatis配置类
@MapperScan(value = "com.wdjr.springboot.mapper")
```

### 配置文件方式

1、新建文件

![50.mybatisxml](E:\工作文档\SpringBoot\images\50.mybatisxml.jpg)

2、新建mybatis的配置文件

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <settings>
        <setting name="mapUnderscoreToCamelCase" value="true"/>
    </settings>
</configuration>
```

3、新建Employee的接口方法

```java
public interface EmployeeMapper {

    public Employee getEmpById(Integer id);

    public void insetEmp(Employee employee);
}
```

4、新建Employee的mapper.xml的映射文件

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.wdjr.springboot.mapper.EmployeeMapper">
    <select id="getEmpById" resultType="com.wdjr.springboot.bean.Employee">
      select * from employee where id=#{id}
   </select>

    <insert id="insetEmp">
        INSERT  INTO employee(last_name,email,gender,d_id) VALUES (#{lastName},#{email},#{gender},#{dId})
    </insert>
</mapper>
```

5、修改application.yml配置文件

```yaml
mybatis:
  config-location: classpath:mybatis/mybatis-config.xml
  mapper-locations: classpath:mybatis/mapper/*.xml
```

6、新建一个Controller访问方法

```java
@RestController
public class EmployeeController {
    @Autowired
    EmployeeMapper employeeMapper;

    @RequestMapping("/getEmp/{id}")
    public Employee getEmp(@PathVariable("id") Integer id){
        return employeeMapper.getEmpById(id);
    }

    @GetMapping("/insertEmp")
    public Employee insertEmp(Employee employee){
        employeeMapper.insetEmp(employee);
        return employee;
    }
}
```
## 4、JPA数据访问

新建工程 springBoot1.5+Web+JPA+MYSQL+JDBC

目录结构

![51.JPA](E:\工作文档\SpringBoot\images\51.JPA.jpg)



1、新建一个实体类User

```java
//使用JPA注解配置映射关系
@Entity//告诉JPA这是一个实体类（和数据表映射的类）
@Table(name="tbl_user") //@Table来指定和那个数据表对应，如果省略默认表明就是user;

public class User {

    @Id //这是一个主键
    @GeneratedValue(strategy = GenerationType.IDENTITY)//自增组件
    private Integer id ;

    @Column(name="last_name",length = 50) //这是和数据表对应的一个列
    private String lastName;
    @Column//省略默认列名就是属性名
    private String email;
    @Column
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
```

2、新建一个UserRepository来继承jpa的绝大多数功能

```java
//继承jpaRepository
public interface UserRepository extends JpaRepository<User,Integer> {

}
```

3、编写配置文件application.yml

```yaml
spring:
  datasource:
    url: jdbc:mysql://192.168.179.131/jpa
    username: root
    password: Welcome_1
    driver-class-name: com.mysql.jdbc.Driver
  jpa:
    hibernate:
    #更新或创建
      ddl-auto: update
    show-sql: true
```

4、编写Controller测试

```java
@RestController
public class UserController {
    @Autowired
    UserRepository userRepository;

    @GetMapping("/user/{id}")
    public User getUser(@PathVariable("id") Integer id){
        User user = userRepository.findOne(id);
        return user;
    }

    @GetMapping("/insert")
    public User insertUser(User user){
        User user1 = userRepository.save(user);
        return  user1;
    }
}
```
