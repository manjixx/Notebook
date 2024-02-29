# Optional

## 一、Optional 介绍

Null 值处理不好会导致 NullPointerException 空指针异常。

因此代码中频繁充斥着 Null 值检查，Optional 的出现是为了安全优雅地处理空指针检查。

## 二、为什么要引入 Optional

User 实例：代表具体用户
UserRepository：增删改查用户

```java

public class User {
    String name;
    String fullName;
}

public class UserRepository{
    public User findUserByName(String name){
        if (name.euqals("Albert")){
            return new User("Albert", "Albert test")
        } else {
            return null;
        }
    }
}

public Static void main(String[] args){
    UserRepository userRepository = new UserRepository();

    User user = userRepository.findByName("Albert");

    // 如果 findByName 入参不是“Albert” 就会出现空指针异常。
    System.out.println(user.getFullName());

    if(user != null){
        System.out.println(user.getFullName());
    } else {
        User defaultUser = new User("Neo","Thomas Anderson");
        System.out.println(defaultUser.getFullName);
    }
}
```

Optional 像是一个容器，他可以包含某种类型的盒子，也可不包含任何值。

并且可以提供一系列的方法，来方便的操作内部的值

- get()
- orElse()
- orElseGet()
- orElseThrow()

Optional 设计还考虑了函数式编程，因此可以与Lambda表达式和Stream API等特性结合使用，可以优雅的进行链式调用。

## 三、 Optional 的基本使用方法

## 四、 Optional 的最佳实践

## 五、 不合理的使用场景
