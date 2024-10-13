# Annotation 注解

## 一、注解基础

注解是JDK1.5版本开始引入的一个特性，**用于对代码进行说明，可以对包、类、接口、字段、方法参数、局部变量等进行注解**。它主要的作用有以下四方面：

- 生成文档，通过代码里**标识的元数据生成 javadoc 文档**
- **编译检查**，通过代码里标识的元数据让编译器在编译期间进行检查验证。
- **编译时动态处理**，编译时通过代码里标识的元数据动态处理，例如*动态生成代码*。
- **运行时动态处理**，运行时通过代码里标识的元数据动态处理，例如*使用反射注入实例*。

注解的常见分类如下：

- Java自带的标准注解，包括`@Override、@Deprecated`和`@SuppressWarnings`，分别用于**标明重写某个方法**、**标明某个类或方法过时**、**标明要忽略的警告**，用这些注解标明后编译器就会进行检查。
- 元注解，**元注解是用于定义注解的注解**，包括`@Retention、@Target、@Inherited、@Documented`
  - `@Retention`用于标明注解被保留的阶段
  - `@Target`用于标明注解使用的范围
  - `@Inherited`用于标明注解可继承
  - `@Documented`用于标明是否生成javadoc文档。
- 自定义注解，可以根据自己的需求定义注解，并可用元注解对自定义注解进行注解。

### 1.1 Java 内置注解

从最为常见的Java内置的注解开始说起，先看下下面的代码：

```java
class A{
    public void test() {
        
    }
}

class B extends A{

    /**
        * 重载父类的test方法
        */
    @Override
    public void test() {
    }

    /**
        * 被弃用的方法
        */
    @Deprecated
    public void oldMethod() {
    }

    /**
        * 忽略告警
        * 
        * @return
        */
    @SuppressWarnings("rawtypes")
    public List processList() {
        List list = new ArrayList();
        return list;
    }
}
```

Java 1.5开始自带的标准注解，包括`@Override`、`@Deprecated`和`@SuppressWarnings`：

- `@Override`：表示当前的方法定义将覆盖父类中的方法
- `@Deprecated`：表示代码被弃用，如果使用了被`@Deprecated`注解的代码则编译器将发出警告
- `@SuppressWarnings`：表示关闭编译器警告信息

接下来将了解这个内置注解，同时通过这几个内置注解中的元注解的定义引出元注解。

> **内置注解-@Override**

注解定义：

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.SOURCE)
public @interface Override {
}
```

从它的定义我们可以看到，**这个注解可以被用来修饰方法**，并且它**只在编译时有效**，在编译后的class文件中便不再存在。

注解的作用：告诉编译器被修饰的方法是重写的父类的中的相同签名的方法，编译器会对此做出检查，若发现父类中不存在这个方法或是存在的方法签名不同，则会报错。

> **内置注解-@Deprecated**

注解定义：

```java
// 会被文档化
@Documented  
// 可以保留到运行时                       
@Retention(RetentionPolicy.RUNTIME)
// 能够修饰构造方法、属性、局部变量、方法、包、参数、类型
@Target(value={CONSTRUCTOR, FIELD, LOCAL_VARIABLE, METHOD, PACKAGE, PARAMETER, TYPE})
public @interface Deprecated {
}
```

从它的定义我们可以知道，它会被文档化，能够保留到运行时，能够修饰构造方法、属性、局部变量、方法、包、参数、类型。

注解作用：告诉编译器被修饰的程序元素已被“废弃”，不再建议用户使用。

> **内置注解 - @SuppressWarnings**

注解定义：

```java
// 修饰元素
@Target({TYPE, FIELD, METHOD, PARAMETER, CONSTRUCTOR, LOCAL_VARIABLE})
// 存活在源码时，取值为String[]
@Retention(RetentionPolicy.SOURCE)
public @interface SuppressWarnings {
    String[] value();
}
```

它能够修饰的程序元素包括类型、属性、方法、参数、构造器、局部变量，只能存活在源码时，取值为`String[]`。它的作用是告诉编译器忽略指定的警告信息，**它可以取的值如下所示**


参数 | 作用 | 原描述
---------|----------|---------
 all | 抑制所有警告	 | to suppress all warnings
 boxing | 抑制装箱、拆箱操作时候的告警 | to supress warnings relative to boxing/unboxing operations
 cast | 抑制映射相关的告警 | to suppress warning relative to cast operation
 dep-ann | 抑制启动注释的告警 | to supress warnings relative to deprecated annotation
 deprecation | 抑制过期方法告警 | to supress warning relative to deprecation
 fallthrough | 抑制在 switch 中缺失 breaks 的告警 | to supress warnings relative to missing breaks in switch statements
 finally | 抑制finally 模块没有返回的告警 | to supress warnings relative to finally block that don't return
 hiding | 抑制与隐藏变数的区域变数的相关告警 | to supress warnings relative to locals that hide variable()
 incomplete-switch | 忽略没有完整的 switch | to supress warnings relative to missing entries in a switch statement(enum case)
 nls | 忽略非nls格式的字符 | to suppress warnings relative to non-nls string literals
 null | 忽略对null的操作 | to suppress warnings relative to null analysis
 rawtype | 使用generics时忽略没有指定相应的类型 | to suppress warnings relative to un-specific types when using
 restriction | 抑制与使用不建议或禁止参照相关的警告 | to suppress warnings relative to usage of discouraged or
 serial | 忽略在serializable类中没有声明serialVersionUID变量 | to suppress warnings relative to missing serialVersionUID field for a serializable class
 static-access | 抑制不正确的静态访问方式警告 | to suppress warnings relative to incorrect static access
 synthetic-access | 抑制子类没有按最优方法访问内部类的警告 | to suppress warnings relative to unoptimized access from inner classes
 unchecked | 抑制没有进行类型检查操作的警告 | to suppress warnings relative to unchecked operations
 unqualified-field-access | 抑制没有权限访问的域的警告 | to suppress warnings relative to field access unqualified
 unused | 抑制没被使用过的代码的警告 | to suppress warnings relative to unused code

### 1.2 元注解

上述内置注解的定义中使用了一些元注解（注解类型进行注解的注解类），在`JDK 1.5`中提供了4个标准的元注解：`@Target`，`@Retention`，`@Documented`，`@Inherited`, 在`JDK 1.8`中提供了两个元注解 `@Repeatable`和`@Native`。

> **元注解 - @Target**

`@Target`注解的作用是：描述注解的使用范围（即：被修饰的注解可以用在什么地方） 。

注解可以用于修饰 packages、types（类、接口、枚举、注解类）、类成员（方法、构造方法、成员变量、枚举值）、方法参数和本地变量（如循环变量、catch参数）。

在定义注解类时使用了`@Target` 能够更加清晰的知道它能够被用来修饰哪些对象，它的取值范围定义在`ElementType` 枚举中。

```java
public enum ElementType {
 
    TYPE, // 类、接口、枚举类
 
    FIELD, // 成员变量（包括：枚举常量）
 
    METHOD, // 成员方法
 
    PARAMETER, // 方法参数
 
    CONSTRUCTOR, // 构造方法
 
    LOCAL_VARIABLE, // 局部变量
 
    ANNOTATION_TYPE, // 注解类
 
    PACKAGE, // 可用于修饰：包
 
    TYPE_PARAMETER, // 类型参数，JDK 1.8 新增
 
    TYPE_USE // 使用类型的任何地方，JDK 1.8 新增
 
}
```

> **元注解-@Retention&@RetentionTarget**

`Reteniton`注解的作用是：描述注解保留的时间范围（即：被描述的注解在它所修饰的类中可以被保留到何时） 。

`Reteniton`一共有三种策略，定义在`RetentionPolicy`枚举中

```java
public enum RetentionPolicy {
    SOURCE,    // 源文件保留
    CLASS,     // 编译期保留，默认值
    RUNTIME   // 运行期保留，可通过反射去获取注解信息
}
```

为了验证应用了这三种策略的注解类有何区别，分别使用三种策略各定义一个注解类做测试。

```java
@Retention(RetentionPolicy.SOURCE)
public @interface SourcePolicy {
 
}
@Retention(RetentionPolicy.CLASS)
public @interface ClassPolicy {
 
}
@Retention(RetentionPolicy.RUNTIME)
public @interface RuntimePolicy {
 
}
```

用定义好的三个注解类分别去注解一个方法。

```java
public class RetentionTest {
 
    @SourcePolicy
    public void sourcePolicy() {
    }
 
    @ClassPolicy
    public void classPolicy() {
    }
 
    @RuntimePolicy
    public void runtimePolicy() {
    }
}
```

通过执行 `javap -verbose RetentionTest``命令获取到的RetentionTest` 的 `class` 字节码内容如下。

```java
{
  public retention.RetentionTest();
    flags: ACC_PUBLIC
    Code:
      stack=1, locals=1, args_size=1
         0: aload_0
         1: invokespecial #1                  // Method java/lang/Object."<init>":()V
         4: return
      LineNumberTable:
        line 3: 0

  public void sourcePolicy();
    flags: ACC_PUBLIC
    Code:
      stack=0, locals=1, args_size=1
         0: return
      LineNumberTable:
        line 7: 0

  public void classPolicy();
    flags: ACC_PUBLIC
    Code:
      stack=0, locals=1, args_size=1
         0: return
      LineNumberTable:
        line 11: 0
    RuntimeInvisibleAnnotations:
      0: #11()

  public void runtimePolicy();
    flags: ACC_PUBLIC
    Code:
      stack=0, locals=1, args_size=1
         0: return
      LineNumberTable:
        line 15: 0
    RuntimeVisibleAnnotations:
      0: #14()
}
```

从 `RetentionTest` 的字节码内容我们可以得出以下两点结论：

- 编译器并没有记录下 `sourcePolicy()` 方法的注解信息；
- 编译器分别使用了 `RuntimeInvisibleAnnotations` 和 `RuntimeVisibleAnnotations` 属性去记录了`classPolicy()`方法 和 `runtimePolicy()`方法 的注解信息；

> **元注解 - @Documented**

`Documented`注解的作用是：描述在使用 `javadoc` 工具为类生成帮助文档时是否要保留其注解信息。

以下代码在使用`Javadoc`工具可以生成`@TestDocAnnotation`注解信息。

```java
import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Target;
 
@Documented
@Target({ElementType.TYPE,ElementType.METHOD})
public @interface TestDocAnnotation {
    public String value() default "default";
}

```

```java
@TestDocAnnotation("myMethodDoc")
public void testDoc() {

}
```

> **元注解 - @Inherited**

`Inherited`注解的作用：被它修饰的`Annotation`将具有继承性。**如果某个类使用了被`@Inherited`修饰的`Annotation`，则其子类将自动具有该注解。**

测试该注解

- 定义`@Inherited`注解

```java
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE,ElementType.METHOD})
public @interface TestInheritedAnnotation {
    String [] values();
    int number();
}
```

- 使用注解

```java
@TestInheritedAnnotation(values = {"value"}, number = 10)
public class Person {
}

class Student extends Person{
    @Test
    public void test(){
        Class clazz = Student.class;
        Annotation[] annotations = clazz.getAnnotations();
        for (Annotation annotation : annotations) {
            System.out.println(annotation.toString());
        }
    }
}
```

- 输出

```java
xxxxxxx.TestInheritedAnnotation(values=[value], number=10)
```

即使`Student`类没有显示地被注解`@TestInheritedAnnotation`，但是它的父类`Person`被注解，而且`@TestInheritedAnnotation`被`@Inherited`注解，因此`Student`类自动有了该注解。

> **元注解 - @Repeatable (Java8)**

> **元注解 - @Native (Java8)**

使用 `@Native` 注解修饰成员变量，则表示这个变量可以被本地代码引用，常常被代码生成工具使用。

### 1.3 注解与反射接口

### 1.4 自定义注解

## 二、深入理解注解

> **Java8提供了哪些新的注解？**

> **注解支持继承吗？**


> **注解实现的原理？**

## 三、注解的应用场景

### 3.1 配置化到注解化 - 框架的演进


### 3.2 继承实现到注解实现 - Junit3到Junit4

### 3.3 自定义注解和AOP - 通过切面实现解耦