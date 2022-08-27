
# 八、SpringBoot的自定义starter

starter：场景启动器

1、场景需要使用什么依赖？

2、如何编写自动配置

```java
@Configuration //指定这个类是一个配置类
@ConditionalOnXXX //在指定条件下成立的情况下自动配置类生效
@AutoConfigureAfter //指定自动配置类的顺序
@Bean //给容器中添加组件

@ConfigurationProperties //结合相关xxxProperties类来绑定相关的配置
@EnableConfigurationProperties //让xxxProperties生效加到容器中

自动配置类要能加载
将需要启动就加载的自动配置类，配置在META-INF/spring.factories
# Auto Configure
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
org.springframework.boot.autoconfigure.admin.SpringApplicationAdminJmxAutoConfiguration,\
org.springframework.boot.autoconfigure.aop.AopAutoConfiguration,\
```

3、模式

启动器空的jar只需要做依赖管理导入；

专门写一个自动配置模块；

启动器依赖自动配置，别人只需要引入starter

xxx-spring-boot-starter

### 新建一个starter

> 绕的你怀疑人生

#### 1、新建一个空项目工程

![56.starter01](E:\工作文档\SpringBoot\images\56.starter01.jpg)

2、项目命名

![57.starter02](E:\工作文档\SpringBoot\images\57.starter02.jpg)



3、导入module

![58.starter03](E:\工作文档\SpringBoot\images\58.starter03.jpg)

4、新建一个Maven工程

![59.starter04](E:\工作文档\SpringBoot\images\59.starter04.jpg)

5、项目命名

![60.starter05](E:\工作文档\SpringBoot\images\60.starter05.jpg)



![61.starter06](E:\工作文档\SpringBoot\images\61.starter06.jpg)

6、在新建一个autoconfiguration类的spring

![62.starter07](E:\工作文档\SpringBoot\images\62.starter07.jpg)

7、项目命名

![63.starter08](E:\工作文档\SpringBoot\images\63.starter08.jpg)

8、无需导入依赖

![64.starter09](E:\工作文档\SpringBoot\images\64.starter09.jpg)

9、next

![65.starter10](E:\工作文档\SpringBoot\images\65.starter10.jpg)

最后配置完成

#### 2、编写starter

##### autoconfigurer

对**lxy-spring-boot-starter-autoconfigurer**进行删减

目录

![66.starter-build01](E:\工作文档\SpringBoot\images\66.starter-build01.jpg)

2、pom文件修改

```xml
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>

    </dependencies>


</project>
```

3、编写相关的类

![67.starter-build02](E:\工作文档\SpringBoot\images\67.starter-build02.jpg)

4、HelloProperties

```java
package com.lxy.starter;


import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "lxy.hello")
public class HelloProperties {
    private String prefix;
    private String suffix;

    public String getPrefix() {
        return prefix;
    }

    public void setPrefix(String prefix) {
        this.prefix = prefix;
    }

    public String getSuffix() {
        return suffix;
    }

    public void setSuffix(String suffix) {
        this.suffix = suffix;
    }
}
```

5、HelloService

```java
package com.lxy.starter;

public class HelloService {

    HelloProperties helloProperties;

    public HelloProperties getHelloProperties() {
        return helloProperties;
    }

    public void setHelloProperties(HelloProperties helloProperties) {
        this.helloProperties = helloProperties;
    }

    public String sayHello(String name){
        return helloProperties.getPrefix()+name+helloProperties.getSuffix();
    }
}
```

6、HelloServiceAutoConfiguration



```java
package com.lxy.starter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnWebApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConditionalOnWebApplication
@EnableConfigurationProperties(HelloProperties.class)
public class HelloServiceAutoConfiguration {

    @Autowired
    HelloProperties helloProperties;
    @Bean
    public HelloService helloService(){
        HelloService service = new HelloService();
        service.setHelloProperties(helloProperties);
        return service;
    }

}
```

7、配置文件

```
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
com.lxy.starter.HelloServiceAutoConfiguration
```

8、修改lxy-spring-boot-starter 也就是之前的Maven项目，修改pom文件引入autoconfiguration依赖

```xml
<dependencies>
    <dependency>
        <groupId>com.lxy.starter</groupId>
        <artifactId>lxy-spring-boot-starter-autoconfigurer</artifactId>
        <version>0.0.1-SNAPSHOT</version>
    </dependency>
</dependencies>
```

9、install生成

![68.starter-build03](E:\工作文档\SpringBoot\images\68.starter-build03.jpg)

#### 3、测试

新建一个springboot 1.5+web

1、引入starter

```xml
    <dependency>
        <groupId>com.lxy.starter</groupId>
        <artifactId>lxy-spring-boot-starter</artifactId>
        <version>1.0-SNAPSHOT</version>
    </dependency>

</dependencies>
```

2、新建一个Controller用来测试

```java
@RestController
public class HelloController {

    @Autowired
    HelloService helloService;

    @GetMapping
    public  String hello(){
        return helloService.sayHello("test");
    }
}
```

3、编写配置文件制定前缀和后缀名

```properties
lxy.hello.prefix=Starter-
lxy.hello.suffix=-Success
```

4、运行访问http://localhost:8080/hello

![70.starter-build05](E:\工作文档\SpringBoot\images\70.starter-build05.jpg)

成功爽啊
