# Generics 泛型

## 为什么引入泛型

泛型的本质是为了参数化类型（在不创建新的类型的情况下，通过泛型指定的不同类型来控制形参具体限制的类型）。也就是说在泛型使用过程中，操作的数据类型被指定为一个参数，这种参数类型可以用在类、接口和方法中，分别被称为泛型类、泛型接口、泛型方法。

**引入泛型的意义：** 多种数据类型执行相同的代码，代码复用。

**Case1**:创建一个类打印 Integer 变量

当我们需要换一种类打印，比如 String, Float, Double 类等时，我们需要创建新的类。这样会导致代码的重复性。

```java
public class IntegerPrinter {
    Integer content;
    IntegerPrinter(Integer content) {
        this.content = content;
    }

    public void print() {
        System.out.println(content);
    }
}

public class Main {
    public static void main(String[] args) {
        IntegerPrinter printer = new IntegerPrinter(123);

        printer.print();
    }
}

```

**Case2:** 实现不同类型的加法

```java
# 旧代码

private static int add(int a, int b){
    System.out.println(a + "+" + b + "=" + (a + b));
    return a + b;
}

private static float add(float a, float b){
    System.out.println(a + "+" + b + "=" + (a + b));
    return a + b;
}

private static double add(double a, double b)
System.out.println(a + "+" + b + "=" + (a + b));
    return a + b;

// 通过泛型，实现方法复用

private static <T extends Number> double (T a, T b){
    System.out.println(a + "+" + b + "=" + (a.doubleValue() + b.doubleValue()));
    return a.doubleValue() + b.doubleValue();
}
```

## 二、泛型的基本使用

### 2.1 泛型类

- 通过在类名称后边增加 `<T>` 来定义泛型类，当然 T 可以用其他字符/字符串进行替代
- 泛型类本质是将类型作为一个参数传入
- 调用泛型类时，传入的类型参数（即尖括号中的类型）不能为 java 中的基本类型（primitive type）
- 泛型类可以传入多个参数

```java
public class Printer<T> {
    T content;
    Printer(T content){
        this.content = content;
    }

    public void print() {
        System.out.println(content);
    }
}

// 调用泛型类
public class Main {
    public static void main(String[] args){
        // 打印 Integer 类
        Printer<Integer> printer = new Printer<>(123);
        printer.print();
        // 打印 String 类
        Printer<String> s_printer = new Printer<>("hello world");
        s_printer.print();
    }
}
```

```java
// 多元泛型
public class Printer<T, K> {  // 此处指定了两个泛型类型
    T content;
    K content2;

    Printer(T content, K content2){
        this.content = content;
        this.content2 = content2;
    }

    public void print() {
        System.out.println(content);
        System.out.println(content2);    
    }
}

// 调用泛型类
public class Main {
    public static void main(String[] args){
        // 打印 Integer 类
        Printer<Integer, String> printer = new Printer<>(123,"456");
        printer.print();
    }
}

```

### 2.2 泛型接口

```java
interface Info<T>{  // 在接口上定义泛型
    public T getVar();  // 定义抽象方法，抽象方法返回值就是泛型类型
}

class InfoImpl<T> implements Info<T>{   // 泛型接口子类
    private T var;  //定义属性

    public InfoImple(T var){    // 通过构造方法设置属性内容
        this.setVar(var);
    }

    public void setVar(T var){
        this.var = var;
    }

    public T getVar(){
        return this.var;
    }
}

// 调用泛型类
public class Main {
    public static void main(String[] args){
        Info<String> info = null;   // 声明接口对象
        i = new InfoImpl<String>("Tom");    // 通过子类实例化对象
        System.out.println("内容" + i.getVar());
    }
}

```

### 2.3 泛型方法

泛型也经常使用在函数上，称之为 Generic method。

**泛型方法语法格式**

```java
/**
 * 泛型方法 
 * @param <T> 声明一个泛型 T
 * @param c 用来创建泛型对象
 * @return 
 * @throws InstantiationException
 * @throws IllegalAccessException
 */

public <T> T getObjcet(Class<T> c) throws InstantiationException, IllegalAccessException{
    // 创建泛型对象
    T t = c.newInstance();
    return t;
}
```

上述代码中从左往右依次表达内容如下：

- `<T>` 声明此方法为泛型方法
- `T` 声明此方法返回值类型为类型T
- `Class<T>` 指明泛型 T 的具体类型
- `c` 用来创建泛型 T 代表的类型的对象

**调用泛型方法**

```java
Generic genric = new Generic;
// 此时 obj 就是 User 类的实例
Object object = generic.getObject(Class.forName("com.java.test.User"));
```

需求：写一个 print 方法，去打印任意变量

```java
public class Main {
    public static void main(String[] args){
        print("hello world");
        print(123);
        print(new Car);

    }
    // <T> 告诉 Java 后续 T 为 Generic 类型
    private static <T> void print(T content) {
        System.out.println(content);
    }
}

```

- 在泛型方法中想要对参数类型进行约束，同样泛型类一样使用 extends 关键字实现类/接口，顺序同样为类在接口之前。

```java
public class Main {
    public static void main(String[] args){
        // error
        print("hello world");
        // error
        print(123);
        print(new Car);

    }
    // <T> 告诉 Java 后续 T 为 Generic 类型
    private static <T extends Vehicle & Thing> void print(T content) {
        System.out.println(content);
    }
}

```

- 泛型方法同样可以传入多个参数

```java
public class Main {
    public static void main(String[] args){
        print("hello world", 123);

    }
    // <T> 告诉 Java 后续 T 为 Generic 类型
    private static <T, K> void print(T content, K content2) {
        System.out.println(content);
        System.out.println(content2);
    }
}

```



### 2.4 泛型的上下限

- 用类型的方式约束：当需要类型参数可以做一些约束，比如传入类型参数必须是某个类型的子类型。此时可以用 `extends`
- 在 java 中 这被称为 Boundary Generics
- 用接口的方式约束：此时还需要使用 extends 而不能使用 implements 来实现接口
- 当同时使用类和接口进行约束时，类必须放在接口之前。
  
```java
// Vehicle 是一个类，Thing 是一个接口
public class Printer<T extends Vehicle & Thing> {
    T content;
    Printer(T content){
        this.content = content;
    }

    public void print() {
        System.out.println(content);
    }

}

// 调用泛型类

public class Main {
    public static void main(String[] args){
        // 打印 Integer 类，此时会报错，因为Integer 不是 Vehicle 的子类型
        Printer<Integer> printer = new Printer<>(123);
        printer.print();

        // 打印 S
        Printer<Car> s_printer = new Printer<>(new Car());
        s_printer.print();
    }
}
```

### 2.5 泛型数组

### 类型安全

在日常使用 java 时，我们总会有意无意使用泛型，比如使用集合框架。

疑问：使用集合框架时，能否添加任何元素呢？

- 可以这样使用，但是不建议这样使用
- Java 的类型检查发生在编译阶段，而不是运行阶段，因此例子中进行强制类型转换后IDEA不会报错，因为此时类型检查无误，但是运行时会报错。

```java

public class Main {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("hello world");
        list.add("123");
        System.out.println(list);
        
        
        // 类型安全例子
        List<Object> list = new ArrayList<>();
        list.add("hello world");
        list.add(1234);

        // 如果不增加强制类型转换，idea 将会报错，因为此时还不知道取出来的是什么类型
        // 而增加强制类型转换后，即使取出的类型为 int 类型，此时也不会报错 
        String item = (String) list.get(1);
        // 运行时将会报错。
        System.out.println(item);

    }
}

```

### 通配符

当遇到类型参数是 list 类型时，该如何处理呢？

需求：假如现在我们需要写一个能够打印存放 Integer 元素 List 的方法。

```java
public class Main {
    public static void main(String[] args){
        List<Integer> list = new ArrayList<>();

        list.add(123);
        list.add(456);

        print(list)
    }
    private static void print(List<Integer> content) {
        System.out.println(content);
    }
}

```

当我们需要写一个能够打印存放 String 元素的 List 的方法，则需要修改对应的方法。

当使用 `List<Object>` 时，调用 `print` 方法会报错，因为 String 虽然是 Object 的子类，但是 `List<String>` 不是 `List<Object>` 的子类

```java
public class Main {
    public static void main(String[] args){
        List<String> list = new ArrayList<>();

        list.add(123);
        list.add(456);

        print(list);
    }
    private static void print(List<Object> content) {
        System.out.println(content);
    }
}

```

解决方案：引入通配符 ?

- 上界限通配符，extends，传入类必须为 extends 后的一个子类
- 下界限通配符，super，传入类必须为 super 后类型的负累或其本身。

```java
public class Main {
    public static void main(String[] args){
        List<String> list = new ArrayList<>();

        list.add(123);
        list.add(456);

        print(list);
    }
    private static void print(List<?> content) {
        System.out.println(content);
    }

    // 上界限通配符，传入的类必须限定为 Vehicle 的一个子类
    private static void print(List<? extends Vehicle> content) {
        System.out.println(content);
    }

    // 下界限通配符，传入的类?必须限定为 Car 的一个父类，或其本身
    private static void print(List<? super Car> content) {
        System.out.println(content);
    }
}

```

## 三、深入理解泛型

> 如何理解 Java 中的泛型是伪泛型？ 泛型中类型擦出

> 如何证明类型擦除？

> 如何理解泛型的编译期检查？ 

> 如何理解泛型的编译期检查？

> 如何理解泛型的多态？泛型的桥接方法

> 如何理解基本类型不能作为泛型类型？

> 如何理解泛型类型不能实例化？

> 泛型数组：能不能采用具体的泛型类型进行初始化？

> 泛型数组：如何正确的初始化泛型数组实例？

> 如何理解泛型类中的静态方法和静态变量？

> 如何理解异常中使用泛型？

> 如何获取泛型的参数类型?

