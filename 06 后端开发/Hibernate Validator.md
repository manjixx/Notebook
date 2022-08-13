# 前言

> 参数校验

开发中经常需要写一些字段校验的代码，如字段非空、字段长度限制，邮箱格式验证等，因为这些内容与业务逻辑关系不大，开发过程中会遇到如下问题:

- 验证代码繁琐，重复劳动
- 方法内代码显得冗长
- 每次要看哪些参数验证是否完整，需要去翻阅验证逻辑代码

Hibernate Validator 框架刚好解决了这些问题，可以很优雅的方式实现参数的校验，让业务代码 和 校验逻辑 分开,不再编写重复的校验逻辑。

# 一、Hibernate Validator 

> **Hibernate Validator 简介**
` Hibernate Validator`是`Bean Validation`的参考实现。`Hibernate Validator` 提供了 JSR 303 规范中所有内置 constraint 的实现，除此之外还有一些附加的 constraint。

[Hibernate Validator官方文档](https://docs.jboss.org/hibernate/stable/validator/reference/en-US/html_single/#section-provider-specific-settings)

`Bean Validation`为 JavaBean 验证定义了相应的元数据模型和API。缺省的元数据是 Java Annotations，通过使用 XML 可以对原有的元数据信息进行覆盖和扩展。Bean Validation 是一个运行时的数据验证框架，在验证之后验证的错误信息会被马上返回。

> **Hibernate Validator的作用**

- 验证逻辑与业务逻辑之间进行了分离，降低了程序耦合度；
- 统一且规范的验证方式，无需你再次编写重复的验证代码；


# 二、Hibernate Validator的使用

> **Hibernate Validator的两种使用方式**

- 接口api 的入参校验
- 封装工具类 在代码中校验

## 2.1 引入jar包

`spring-boot-starter-web`包里面有`hibernate-validator`包，不需要引用`hibernate validator`依赖。

```XML
<dependency>
      <groupId>org.hibernate</groupId>
      <artifactId>hibernate-validator</artifactId>
      <version>6.0.9.Final</version>
</dependency>
```

## 2.2 Java对象添加约束注解

```JAVA
package com.example.demo.bean;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Length;
import org.springframework.format.annotation.DateTimeFormat;
import java.util.Date;
/**
 * @date 2018/4/12 11:08
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Account {
    private String id;
    @NotNull
    @Length(max = 20)
    private String userName;
    @NotNull
    @Pattern(regexp = "[A-Z][a-z][0-9]")
    private String passWord;
    @DateTimeFormat(pattern = "yyy-MM-dd")
    private Date createTime;
    private String alias;
    @Max(10)
    @Min(1)
    private Integer level;
    private Integer vip;
}
```

## 2.3 API接口入参校验

- 对接口入参添加`@valid`注解，对入参进行校验

```JAVA
@PostMapping("/saveAccount")
    public Object saveAccount(@RequestBody @Valid Account account){
        accountService.saveAccount(account);
        return "保存成功";
}
```

- PostMan测试接口

```bash
# 请求参数：
requestbody:{"alias":"kalakala","userName":"wokalakala"}
```

- 测试结果

服务器返回400的状态码，响应结果中可查看到提示 passWord 字段不能为null。具体的响应报文有点长，就不贴出来啦。

## 2.4 封装工具类在代码中校验

- **封装工具类**
  
```java

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;

import lombok.Data;
import org.hibernate.validator.HibernateValidator;
public class ValidationUtil {
    /**
     * 开启快速结束模式 failFast (true)
     */
    private static Validator validator = Validation.byProvider(HibernateValidator.class).configure().failFast(false).buildValidatorFactory().getValidator();
    /**
     * 校验对象
     *
     * @param t bean
     * @param groups 校验组
     * @return ValidResult
     */
    public static <T> ValidResult validateBean(T t,Class<?>...groups) {
        ValidResult result = new ValidationUtil().new ValidResult();
        Set<ConstraintViolation<T>> violationSet = validator.validate(t,groups);
        boolean hasError = violationSet != null && violationSet.size() > 0;
        result.setHasErrors(hasError);
        if (hasError) {
            for (ConstraintViolation<T> violation : violationSet) {
                result.addError(violation.getPropertyPath().toString(), violation.getMessage());
            }
        }
        return result;
    }
    /**
     * 校验bean的某一个属性
     *
     * @param obj          bean
     * @param propertyName 属性名称
     * @return ValidResult
     */
    public static <T> ValidResult validateProperty(T obj, String propertyName) {
        ValidResult result = new ValidationUtil().new ValidResult();
        Set<ConstraintViolation<T>> violationSet = validator.validateProperty(obj, propertyName);
        boolean hasError = violationSet != null && violationSet.size() > 0;
        result.setHasErrors(hasError);
        if (hasError) {
            for (ConstraintViolation<T> violation : violationSet) {
                result.addError(propertyName, violation.getMessage());
            }
        }
        return result;
    }
    /**
     * 校验结果类
     */
    @Data
    public class ValidResult {

        /**
         * 是否有错误
         */
        private boolean hasErrors;

        /**
         * 错误信息
         */
        private List<ErrorMessage> errors;

        public ValidResult() {
            this.errors = new ArrayList<>();
        }
        public boolean hasErrors() {
            return hasErrors;
        }

        public void setHasErrors(boolean hasErrors) {
            this.hasErrors = hasErrors;
        }

        /**
         * 获取所有验证信息
         * @return 集合形式
         */
        public List<ErrorMessage> getAllErrors() {
            return errors;
        }
        /**
         * 获取所有验证信息
         * @return 字符串形式
         */
        public String getErrors(){
            StringBuilder sb = new StringBuilder();
            for (ErrorMessage error : errors) {
                sb.append(error.getPropertyPath()).append(":").append(error.getMessage()).append(" ");
            }
            return sb.toString();
        }

        public void addError(String propertyName, String message) {
            this.errors.add(new ErrorMessage(propertyName, message));
        }
    }

    @Data
    public class ErrorMessage {

        private String propertyPath;

        private String message;

        public ErrorMessage() {
        }

        public ErrorMessage(String propertyPath, String message) {
            this.propertyPath = propertyPath;
            this.message = message;
        }
    }
}
```

- **使用工具类校验参数**

```java
    @Test
    public void test5() throws IOException {
        Account account = new Account();
        account.setAlias("kalakala");
        account.setUserName("wokalakala");
        account.setPassWord("密码");
        ValidationUtil.ValidResult validResult = ValidationUtil.validateBean(account);
        if(validResult.hasErrors()){
            String errors = validResult.getErrors();
            System.out.println(errors);
        }
    }
```

- **测试结果**

```xml
passWord:需要匹配正则表达式"[A-Z][a-z][0-9]" 
```

# 三、hibernate的两种校验模式

failFast：true  快速失败返回模式    false 普通模式 

> **普通模式(默认模式)**

会校验完所有的属性，然后返回所有的验证失败信息


> **快速失败返回模式**

快速失败返回模式

> **两种验证模式配置方式**


```java
// failFast: true 快速失败返回模式，false 普通模式
ValidatorFactory validatorFactory = Validation.byProvider( HibernateValidator.class )
        .configure()
        .failFast( true )
        .buildValidatorFactory();
Validator validator = validatorFactory.getValidator();
```

```java
// hibernate.validator.fail_fast: true 快速失败返回模式，false 普通模式

ValidatorFactory validatorFactory = Validation.byProvider( HibernateValidator.class )
        .configure()
        .addProperty( "hibernate.validator.fail_fast", "true" )
        .buildValidatorFactory();
Validator validator = validatorFactory.getValidator();
```

# 四、Hibernate校验

## 4.1 请求参数校验

## 4.2 GET参数校验

## 4.3 Model校验

## 4.4 对象级联校验


## 4.5 分组校验

## 4.6 自定义校验器

# 五、参考链接

[Hibernate Validator校验](https://cloud.tencent.com/developer/article/1796453)

[springboot使用hibernate validator校验](https://www.cnblogs.com/mr-yang-localhost/p/7812038.html)

[Hibernate Validator 使用介绍](https://www.jianshu.com/p/0bfe2318814f)
