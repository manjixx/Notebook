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

- `<T>` 声明此方法为泛型方法，定义泛型方法时，必须在返回值前边加一个`<T>`，来声明这是一个泛型方法，持有一个泛型T，然后才可以用泛型T作为方法的返回值
- `T` 声明此方法返回值类型为类型T
- `Class<T>` 指明泛型 T 的具体类型
- `c` 用来创建泛型 T 代表的类型的对象。因为是泛型方法，就代表着我们不知道具体的类型是什么，也不知道构造方法如何，因此没有办法去new一个对象，但可以利用变量c的`newInstance`方法去创建对象，也就是利用反射创建对象。
  
**调用泛型方法**

```java
Generic genric = new Generic;
// 此时 obj 就是 User 类的实例
Object object = generic.getObject(Class.forName("com.java.test.User"));
```

泛型方法要求的参数是`Class<T>`类型，而`Class.forName()`方法的返回值也是`Class<T>`，因此可以用Class.forName()作为参数。其中，forName()方法中的参数是何种类型，返回的`Class<T>`就是何种类型。

**案例**：写一个 print 方法，去打印任意变量

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

泛型方法同样可以传入多个参数

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

**泛型上下限引入**

```java
class A{}
class B extends A {}

// 如下两个方法不会报错
public static void funA(A a) {
    // ...          
}
public static void funB(B b) {
    funA(b);
    // ...             
}

// 如下funD方法会报错
public static void funC(List<A> listA) {
    // ...          
}
public static void funD(List<B> listB) {
    // Unresolved compilation problem: The method doPrint(List<A>) in the type test is not applicable for the arguments (List<B>)
    funC(listB); 
    // ...             
}
```

**解决方案：** 为了解决泛型中隐含的转换问题，Java 泛型加入了类型参数的上下边界机制。`<? extends A>`表示该类型参数可以是A(上边界)或者A的子类类型。编译时擦除到类型A，即用A类型代替类型参数。这种方法可以解决开始遇到的问题，编译器知道类型参数的范围，如果传入的实例类型B是在这个范围内的话允许转换，这时只要一次类型转换就可以了，运行时会把对象当做A的实例看待。

**泛型上限**

```java
class Info<T extends Number>{    // 此处泛型只能是Number 及其子类型
    private T var ;              // 定义泛型变量
    public void setVar(T var){
        this.var = var ;
    }
    public T getVar(){
        return this.var ;
    }
    public String toString(){    // 直接打印
        return this.var.toString() ;
    }
}
public class demo1{
    public static void main(String args[]){
        Info<Integer> i1 = new Info<Integer>() ;        // 声明Integer的泛型对象
    }
}
```

**泛型下限**

```java
class Info<T>{
    private T var ;        // 定义泛型变量
    public void setVar(T var){
        this.var = var ;
    }
    public T getVar(){
        return this.var ;
    }
    public String toString(){    // 直接打印
        return this.var.toString() ;
    }
}
public class GenericsDemo21{
    public static void main(String args[]){
        Info<String> i1 = new Info<String>() ;        // 声明String的泛型对象
        Info<Object> i2 = new Info<Object>() ;        // 声明Object的泛型对象
        i1.setVar("hello") ;
        i2.setVar(new Object()) ;
        fun(i1) ;
        fun(i2) ;
    }
    public static void fun(Info<? super String> temp){    // 只能接收String 类型及其父类型，String类的父类只有Object类
        System.out.print(temp + ", ") ;
    }
}

```

**小结**

```java
<?> 无限制通配符
<? extends E> extends 关键字声明了类型的上界，表示参数化的类型可能是所指定的类型，或者是此类型的子类
<? super E> super 关键字声明了类型的下界，表示参数化的类型可能是指定的类型，或者是此类型的父类

// 使用原则《Effictive Java》
// 为了获得最大限度的灵活性，要在表示 生产者或者消费者 的输入参数上使用通配符，使用的规则就是：生产者有上限、消费者有下限
1. 如果参数化类型表示一个 T 的生产者，使用 < ? extends T>;
2. 如果它表示一个 T 的消费者，就使用 < ? super T>；
3. 如果既是生产又是消费，那使用通配符就没什么意义了，因为你需要的是精确的参数类型。
```

**案例**

```java
private  <E extends Comparable<? super E>> E max(List<? extends E> e1) {
    if (e1 == null){
        return null;
    }
    //迭代器返回的元素属于 E 的某个子类型
    Iterator<? extends E> iterator = e1.iterator();
    E result = iterator.next();
    while (iterator.hasNext()){
        E next = iterator.next();
        if (next.compareTo(result) > 0){
            result = next;
        }
    }
    return result;
}
```

- 上述代码中的类型参数 E 的范围是`<E extends Comparable<? super E>>`，我们可以分步查看：
- 要进行比较，所以 E 需要是可比较的类，因此需要 `extends Comparable<…>`（注意这里不要和继承的 extends 搞混了，不一样）
- `Comparable< ? super E>` 要对 E 进行比较，即 E 的消费者，所以需要用 super
- 而参数 `List< ? extends E>`表示要操作的数据是 E 的子类的列表，指定上限，这样容器才够大

**多个限制，使用符号&**

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

> **泛型数组申明**

```java
List<String>[] list11 = new ArrayList<String>[10]; //编译错误，非法创建 
List<String>[] list12 = new ArrayList<?>[10]; //编译错误，需要强转类型 
List<String>[] list13 = (List<String>[]) new ArrayList<?>[10]; //OK，但是会有警告 
List<?>[] list14 = new ArrayList<String>[10]; //编译错误，非法创建 
List<?>[] list15 = new ArrayList<?>[10]; //OK 
List<String>[] list6 = new ArrayList[10]; //OK，但是会有警告
```

- 讨巧的使用场景

```java
public class GenericsDemo30{  
    public static void main(String args[]){  
        Integer i[] = fun1(1,2,3,4,5,6) ;   // 返回泛型数组  
        fun2(i) ;  
    }  
    public static <T> T[] fun1(T...arg){  // 接收可变参数  
        return arg ;            // 返回泛型数组  
    }  
    public static <T> void fun2(T param[]){   // 输出  
        System.out.print("接收泛型数组：") ;  
        for(T t:param){  
            System.out.print(t + "、") ;  
        }  
    }  
}
```

- 合理使用

```java
public ArrayWithTypeToken(Class<T> type, int size) {
    array = (T[]) Array.newInstance(type, size);
}
```

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

### 3.1 如何理解 Java 中的泛型是伪泛型？ 泛型中类型擦除

Java 泛型这个特性是从JDK 1.5才开始加入的，因此为了兼容之前的版本，**Java泛型的实现采取了“伪泛型”的策略，即Java在语法上支持泛型，但是在编译阶段会进行所谓的“类型擦除”（Type Erasure），将所有的泛型表示（尖括号中的内容）都替换为具体的类型（其对应的原生态类型），就像完全没有泛型一样**。理解类型擦除对于用好泛型是很有帮助的，尤其是一些看起来“疑难杂症”的问题，弄明白了类型擦除也就迎刃而解了。

> **泛型的类型擦除原则**

- 消除类型参数声明，即删除`<>`及其包围的部分。
- 根据类型参数的上下界推断并替换所有的类型参数为原生态类型：
  - 如果类型参数是**无限制通配符或没有上下界限定**则替换为O**bject**
  - 如果存在**上下界限定则根据子类替换原则取类型参数的*最左边限定类型（即父类）***。
- 为了保证类型安全，必要时插入强制类型转换代码。
- 自动产生 **“桥接方法”**以保证擦除类型后的代码**仍然具有泛型的“多态性”**。

> **泛型如何擦除**

- 擦除类定义中的类型参数 - 无限制类型擦除

当类定义中的类型参数没有任何限制时，在类型擦除中直接被替换为Object，即形如`<T>`和`<?>`的类型参数都被替换为Object。

![](https://pdai.tech/images/java/java-basic-generic-1.png)
  
- 擦除类定义中的类型参数 - 有限制类型擦除

当类定义中的类型参数存在限制（上下界）时，在类型擦除中替换为类型参数的上界或者下界，比如形如`<T extends Number>`和`<? extends Number>`的类型参数被替换为`Number，<? super Number>`被替换为`Object`。

![](https://pdai.tech/images/java/java-basic-generic-2.png)

- 擦除方法定义中的类型参数
擦除方法定义中的类型参数原则和擦除类定义中的类型参数是一样的，这里仅以擦除方法定义中的有限制类型参数为例。

![](https://pdai.tech/images/java/java-basic-generic-3.png)

### 3.2 证明类型擦除

结合如下两段代码可以证明 Java 类型擦除

- 原始类型相等

```java
public class Test {

    public static void main(String[] args) {

        ArrayList<String> list1 = new ArrayList<String>();
        list1.add("abc");

        ArrayList<Integer> list2 = new ArrayList<Integer>();
        list2.add(123);

        System.out.println(list1.getClass() == list2.getClass()); // true
    }
}
```

上述代码中，定义了两个 ArrayList 数组，一个为`ArrayList<String>`泛型类型，只可以存储字符串；一个为`ArrayList<Integer>`泛型类型的，只能存储整数。

通过`list1`对象和`list2`对象的`getClass()`方法获取他们的类的信息，最后发现结果为`true`。

**说明泛型类型`String`和`Integer`都被擦除掉了，只剩下原始类型。**

- 通过反射添加其他类型元素

```java
public class Test {

    public static void main(String[] args) throws Exception {

        ArrayList<Integer> list = new ArrayList<Integer>();

        list.add(1);  //这样调用 add 方法只能存储整形，因为泛型类型的实例为 Integer，编译前会进行类型检查。

        list.getClass().getMethod("add", Object.class).invoke(list, "asd");

        for (int i = 0; i < list.size(); i++) {
            System.out.println(list.get(i));
        }
    }
}
```

在程序中定义了一个`ArrayList`泛型类型实例化为`Integer`对象，

- 如果直接调用`add()`方法，那么只能存储整数数据
- 当我们**利用反射调用`add()`方法的时候**，却可以存储字符串\
  
**这说明了`Integer`泛型实例在编译之后被擦除掉了，只保留了原始类型。**

### 3.3 原始类型

在上面，两次提到了原始类型，什么是原始类型？

原始类型 就是擦除去了泛型信息，最后**在字节码中的类型变量的真正类型**，无论何时定义一个泛型，相应的原始类型都会被自动提供，类型变量擦除，并使用其限定类型（无限定的变量用Object）替换。

- 原始类型Object

```java
class Pair<T> {  
    private T value;  
    public T getValue() {  
        return value;  
    }  
    public void setValue(T  value) {  
        this.value = value;  
    }  
} 

// pair 的原始类型为
class Pair {  
    private Object value;  
    public Object getValue() {  
        return value;  
    }  
    public void setValue(Object  value) {  
        this.value = value;  
    }  
}
```

在`Pair<T>`中，T 是一个无限定的类型变量，所以用`Object`替换，其结果就是一个普通的类，如同泛型加入Java语言之前的已经实现的样子。在程序中可以包含不同类型的Pair，如`Pair<String>`或`Pair<Integer>`，但是擦除类型后他们的就成为原始的`Pair`类型了，原始类型都是`Object`。

- 如果类型变量有限定，那么**原始类型就用第一个边界的类型变量类替换**。

```java
public class Pair<T extends Comparable> {}
```

如上声明中，Pair 的原始类型就是 `Comparable`。

- 在调用泛型方法时，可以指定泛型，也可以不指定泛型:
  - 在**不指定泛型的情况下**，泛型变量的类型为该方法中的**几种类型的同一父类的最小级**，直到Object
  - 在指定泛型的情况下，该方法的几种类型必须是该泛型的实例的类型或者其子类

```java
public class Test {  
    public static void main(String[] args) {  

        /**不指定泛型的时候*/  
        int i = Test.add(1, 2); //这两个参数都是Integer，所以T为Integer类型  
        Number f = Test.add(1, 1.2); //这两个参数一个是Integer，一个是Float，所以取同一父类的最小级，为Number  
        Object o = Test.add(1, "asd"); //这两个参数一个是Integer，一个是String，所以取同一父类的最小级，为Object  

        /**指定泛型的时候*/  
        int a = Test.<Integer>add(1, 2); //指定了Integer，所以只能为Integer类型或者其子类  
        int b = Test.<Integer>add(1, 2.2); //编译错误，指定了Integer，不能为Float  
        Number c = Test.<Number>add(1, 2.2); //指定为Number，所以可以为Integer和Float  
    }  

    //这是一个简单的泛型方法  
    public static <T> T add(T x,T y){  
        return y;  
    }  
}
```

- Object泛型

```java
public static void main(String[] args) {  
    ArrayList list = new ArrayList();  
    list.add(1);  
    list.add("121");  
    list.add(new Date());  
}
```

### 3.4 如何理解泛型的编译期检查？

既然说类型变量会在编译的时候擦除掉，那为什么我们往 `ArrayList<String>` 创建的对象中添加整数会报错呢？不是说泛型变量String会在编译的时候变为Object类型吗？为什么不能存别的类型呢？既然类型擦除了，如何保证我们只能使用泛型变量限定的类型呢？

> **原因**

Java编译器是通过**先检查代码中泛型的类型**，然后**再进行类型擦除**，**再进行编译**。

**举例**

```java
public static  void main(String[] args) {  
    ArrayList<String> list = new ArrayList<String>();  
    list.add("123");  
    list.add(123);//编译错误  
}
```

在上面的程序中，使用`add`方法添加一个整型，在`IDEA`中，直接会报错，说明这就是在编译之前的检查，因为如果是在编译之后检查，类型擦除后，原始类型为Object，是应该允许任意引用类型添加的。可实际上却不是这样的，这说明了关于泛型变量的使用，是会在编译之前检查的。

> **类型检查针对谁的呢？**

我们先看看参数化类型和原始类型的兼容。以 ArrayList 为例：

```java
// 旧写法
ArrayList list = new ArrayList(); 
// 现在写法
ArrayList<String> list = new ArrayList<String>();

// 为了与旧写法兼容，必然会出现如下情况：
ArrayList<String> list1 = new ArrayList(); //case 1
ArrayList list2 = new ArrayList<String>(); //case 2
```

与旧代码兼容的两种都是没有错误的，但在编译时会告警。在第一种情况，可以实现与完全使用泛型参数一样的效果，第二种则没有效果。

**类型检查就是编译时完成的**，`new ArrayList()`只是在内存中开辟了一个存储空间，可以存储任何类型对象，而**真正涉及类型检查的是它的引用**，因为我们是使用它引用`list1`来调用它的方法，比如说调用`add`方法，**所以`list1`引用能完成泛型类型的检查。而引用`list2`没有使用泛型，所以不行**。

**举例**

```java
public class Test {  

    public static void main(String[] args) {  

        ArrayList<String> list1 = new ArrayList();  
        list1.add("1"); //编译通过  
        list1.add(1); //编译错误  
        String str1 = list1.get(0); //返回类型就是String  

        ArrayList list2 = new ArrayList<String>();  
        list2.add("1"); //编译通过  
        list2.add(1); //编译通过  
        Object object = list2.get(0); //返回类型就是Object  

        new ArrayList<String>().add("11"); //编译通过  
        new ArrayList<String>().add(22); //编译错误  

        String str2 = new ArrayList<String>().get(0); //返回类型就是String  
    }  
} 
```

上述例子表明：类型检查就是针对引用的，谁是一个引用，用这个引用调用泛型方法，就会对这个引用调用的方法进行类型检测，而无关它真正引用的对象。

> **泛型中参数话类型为什么不考虑继承关系？**

在Java中，像下面形式的引用传递是不允许的:

```java
ArrayList<String> list1 = new ArrayList<Object>(); //编译错误  
ArrayList<Object> list2 = new ArrayList<String>(); //编译错误
```

- 情况一：

我们先看第一种情况，将第一种情况拓展成下面的形式：

```java
ArrayList<Object> list1 = new ArrayList<Object>();  
list1.add(new Object());  
list1.add(new Object());  
ArrayList<String> list2 = list1; //编译错误
```

**在第4行代码的时候，就会有编译错误**。

我们先假设它编译没错。那么当我们使用`list2`引用的`get()`方法取值的时候，返回的都是`String`类型的对象（上面提到了，类型检测是根据引用来决定的），可是它里面实际上已经被我们存放了`Object`类型的对象，这样就会有`ClassCastException`了。所以为了避免这种极易出现的错误，Java不允许进行这样的引用传递。（这也是泛型出现的原因，就是为了解决类型转换的问题，我们不能违背它的初衷）。

- 情况二

再看第二种情况，将第二种情况拓展成下面的形式：

```java
ArrayList<String> list1 = new ArrayList<String>();  
list1.add(new String());  
list1.add(new String());

ArrayList<Object> list2 = list1; //编译错误
```

这样的情况比第一种情况好的多，至少在使用`list2`取值的时候不会出现`ClassCastException`，因为是从`String`转换为`Object`。

可是，这样做有什么意义呢，泛型出现的原因，就是为了解决类型转换的问题。我们使用了泛型，但最终还是要自己强转，违背了泛型设计的初衷。所以java不允许这么干。

此外，如果又用`list2`往里面`add()`新的对象，最终取值时，如何确定取出来的是`String`类型的，还是`Object`类型的呢？

### 3.5 如何理解泛型的多态？泛型的桥接方法

类型擦除会造成多态的冲突，而JVM解决方法就是桥接方法。

> **引例**

```java
// 泛型类
class Pair<T> {  

    private T value;  

    public T getValue() {  
        return value;  
    }  

    public void setValue(T value) {  
        this.value = value;  
    }  
}

// 子类继承泛型类
class DateInter extends Pair<Date> {  

    @Override  
    public void setValue(Date value) {  
        super.setValue(value);  
    }  

    @Override  
    public Date getValue() {  
        return super.getValue();  
    }  
}
```

上述代码中，设定父类的泛型类型为`Pair<Date>`，在子类中，我们覆盖了父类的两个方法，即将父类的泛型类型限定为Date，那么父类里面的两个方法的参数都为Date类型。

从上述逻辑来看，在子类中重写这两个方法不存在任何问题，实际上，从`@Override`标签中也可以看到，一点问题也没有，实际上是这样的吗？

> **分析**

实际上，类型擦除后，父类的的泛型类型全部变为了原始类型Object，**所以父类编译之后会变成下面的样子**：

```java
class Pair {  
    private Object value;  

    public Object getValue() {  
        return value;  
    }  

    public void setValue(Object  value) {  
        this.value = value;  
    }  
} 
```

子类的两个重写的方法的类型：

```java
@Override  
public void setValue(Date value) {  
    super.setValue(value);  
}  
@Override  
public Date getValue() {  
    return super.getValue();  
}
```

先来**分析`setValue`方法**，父类的类型是`Object`，而子类的类型是`Date`，参数类型不一样，这如果实在普通的继承关系中，**根本就不会是重写，而是重载**。 我们在一个main方法测试一下：

```java
public static void main(String[] args) throws ClassNotFoundException {  
        DateInter dateInter = new DateInter();  
        dateInter.setValue(new Date());                  
        dateInter.setValue(new Object()); //编译错误  
}
```

如果是重载，那么子类中两个`setValue`方法，一个是参数`Object`类型，一个是`Date`类型，可是我们发现，根本就没有这样的一个子类继承自父类的`Object`类型参数的方法。**所以说，确实是重写，而不是重载。**

> **为什么会是重写而非重载呢？**

原因是这样的，我们传入父类的泛型类型是`Date`，`Pair<Date>`，我们的本意是将泛型类变为如下：

```java
class Pair {  
    private Date value;  
    public Date getValue() {  
        return value;  
    }  
    public void setValue(Date value) {  
        this.value = value;  
    }  
}
```

然后在子类中重写参数类型为`Date`的那两个方法，实现继承中的多态。

可是由于种种原因，**虚拟机并不能将泛型类型变为`Date`，只能将类型擦除掉，变为原始类型`Object`**。这样，我们的本意是进行重写，实现多态。可是类型擦除后，只能变为了重载。这样，类型擦除就和多态有了冲突。

JVM知道本意吗？ --- 知道！！！
可是它能直接实现吗? ---不能！！！
如果真的不能的话，那我们怎么去重写我们想要的Date类型参数的方法啊。

> **如何实现---桥方法**

于是JVM采用了一个特殊的方法，来完成这项功能，那就是桥方法。

- 首先，我们用`javap -c className`的方式反编译`DateInter`子类的字节码，结果如下：

```java
class com.tao.test.DateInter extends com.tao.test.Pair<java.util.Date> {  
  com.tao.test.DateInter();  
    Code:  
       0: aload_0  
       1: invokespecial #8                  // Method com/tao/test/Pair."<init>":()V  
       4: return  

  public void setValue(java.util.Date);  //我们重写的setValue方法  
    Code:  
       0: aload_0  
       1: aload_1  
       2: invokespecial #16                 // Method com/tao/test/Pair.setValue:(Ljava/lang/Object;)V  
       5: return  

  public java.util.Date getValue();    //我们重写的getValue方法  
    Code:  
       0: aload_0  
       1: invokespecial #23                 // Method com/tao/test/Pair.getValue:()Ljava/lang/Object;  
       4: checkcast     #26                 // class java/util/Date  
       7: areturn  

  public java.lang.Object getValue();     //编译时由编译器生成的桥方法  
    Code:  
       0: aload_0  
       1: invokevirtual #28                 // Method getValue:()Ljava/util/Date 去调用我们重写的getValue方法;  
       4: areturn  

  public void setValue(java.lang.Object);   //编译时由编译器生成的桥方法  
    Code:  
       0: aload_0  
       1: aload_1  
       2: checkcast     #26                 // class java/util/Date  
       5: invokevirtual #30                 // Method setValue:(Ljava/util/Date; 去调用我们重写的setValue方法)V  
       8: return  
}
```

从编译的结果来看，我们本意重写`setValue`和`getValue`方法的子类，竟然有4个方法，其实不用惊奇，**最后的两个方法，就是编译器自己生成的桥方法**。

可以看到**桥方法的参数类型都是`Object`**。即**子类中真正覆盖父类两个方法**的就是这两个看不到的桥方法。而我们自己定义的`setvalue`和`getValue`方法上面的`@Oveerride`只不过是假象。**而桥方法的内部实现，就只是去调用我们自己重写的那两个方法。**

> **注意：setValue和getValue这两个桥方法的意义有所不同**

`setValue`方法是为了解决类型擦除与多态之间的冲突。

`getValue`方法却有普遍意义，即这在普通的类继承中也是普遍存在的重写，这就是协变。如果这是一个普通的继承关系：

```java
// 父类的 getValue 方法如下
public Object getValue() {  
    return super.getValue();  
}

// 而子类重写的方法是：
public Date getValue() {  
    return super.getValue();  
}
```

有一点也许会有疑问，子类中的桥方法`Object getValue()`和`Date getValue()`是同时存在的，可是如果是常规的两个方法，他们的方法签名是一样的，也就是说虚拟机根本不能分别这两个方法。如果是我们自己编写`Java`代码，这样的代码是无法通过编译器的检查的，但是虚拟机却是允许这样做的，**因为虚拟机通过参数类型和返回类型来确定一个方法**，所以编译器为了实现泛型的多态允许自己做这个看起来“不合法”的事情，然后交给虚拟器去区别。

### 3.6 如何理解基本类型不能作为泛型类型？

比如，我们没有`ArrayList<int>`，只有`ArrayList<Integer>`, 为何？

**因为当类型擦除后，`ArrayList`的原始类型变为`Object`，但是`Object`类型不能存储`int`值**，只能引用`Integer`的值。

另外需要注意，我们能够使用`list.add(1)`是因为**Java基础类型的自动装箱拆箱操作**。

### 3.7 如何理解泛型类型不能实例化？

不能实例化泛型类型, **这本质上是由于类型擦除决定的**。

我们可以看到如下代码会在编译器中报错：

```java
T test = new T(); // ERROR
```

因为**在 `Java` 编译期没法确定泛型参数化类型，也就找不到对应的类字节码文件**，所以自然就不行了。此外由于`T` 被擦除为 `Object`，如果可以 `new T()` 则就变成了 `new Object()`，失去了本意。  

如果我们确实需要实例化一个泛型，应该如何做呢？可以通过反射实现：

```java
static <T> T newTclass (Class < T > clazz) throws InstantiationException, IllegalAccessException {
    T obj = clazz.newInstance();
    return obj;
}
```

### 3.8 泛型数组

> **泛型数组：能不能采用具体的泛型类型进行初始化？**

**Oracle 官网案例**

```java
List<String>[] lsa = new List<String>[10]; // Not really allowed.
Object o = lsa;
Object[] oa = (Object[]) o;
List<Integer> li = new ArrayList<Integer>();
li.add(new Integer(3));
oa[1] = li; // Unsound, but passes run time store check
String s = lsa[1].get(0); // Run-time error ClassCastException.
```

由于 JVM 泛型的擦除机制，所以上面代码**可以给 `oa[1]` 赋值为 `ArrayList` 也不会出现异常**，但是**在取出数据的时候却要做一次类型转换**，所以就会出现 `ClassCastException`。

如果**可以进行泛型数组的声明则上面说的这种情况在编译期不会出现任何警告和错误，只有在运行时才会出错**，但是泛型的出现就是为了消灭 `ClassCastException`，所以如果 Java 支持泛型数组初始化操作就是搬起石头砸自己的脚。

而对于下面的代码来说是成立的：

```java
List<?>[] lsa = new List<?>[10]; // OK, array of unbounded wildcard type.
Object o = lsa;
Object[] oa = (Object[]) o;
List<Integer> li = new ArrayList<Integer>();
li.add(new Integer(3));
oa[1] = li; // Correct.
Integer i = (Integer) lsa[1].get(0); // OK
```

所以说**采用通配符的方式初始化泛型数组是允许的**，因为对于通配符的方式最后取出数据是要做显式类型转换的，符合预期逻辑。

综述上所述：**Java 的泛型数组初始化时，数组类型不能是具体的泛型类型，只能是通配符的形式**。因为具体类型会导致可存入任意类型对象，在取出时会发生类型转换异常，会与泛型的设计思想冲突，而通配符形式本来就需要自己强转，符合预期。

更进一步的，我们看看如下的代码：

```java
List<String>[] list11 = new ArrayList<String>[10]; //编译错误，非法创建 
List<String>[] list12 = new ArrayList<?>[10]; //编译错误，需要强转类型 
List<String>[] list13 = (List<String>[]) new ArrayList<?>[10]; //OK，但是会有警告 
List<?>[] list14 = new ArrayList<String>[10]; //编译错误，非法创建 
List<?>[] list15 = new ArrayList<?>[10]; //OK 
List<String>[] list6 = new ArrayList[10]; //OK，但是会有警告
```

> **泛型数组：如何正确的初始化泛型数组实例？**

这个无论我们通过`new ArrayList[10]`的形式还是**通过泛型通配符的形式初始化泛型数组实例都是存在警告的，也就是说仅仅语法合格，运行时潜在的风险需要我们自己来承担**，因此那些方式初始化泛型数组都不是最优雅的方式。

**优雅的初始化泛型数组**

- 尽量使用列表集合替换泛型数组
- 通过使用`java.lang.reflect.Array.newInstance(Class<T> componentType, int length)` 方法来创建一个具有指定类型和维度的数组

```java
public class ArrayWithTypeToken<T> {
    private T[] array;

    public ArrayWithTypeToken(Class<T> type, int size) {
        array = (T[]) Array.newInstance(type, size);
    }

    public void put(int index, T item) {
        array[index] = item;
    }

    public T get(int index) {
        return array[index];
    }

    public T[] create() {
        return array;
    }
}
//...

ArrayWithTypeToken<Integer> arrayToken = new ArrayWithTypeToken<Integer>(Integer.class, 100);
Integer[] array = arrayToken.create();
```

所以使用反射来初始化泛型数组算是优雅实现，因为泛型类型 T 在运行时才能被确定下来，我们能创建泛型数组也必然是在 Java 运行时想办法，而运行时能起作用的技术最好的就是反射了。

### 3.9 如何理解泛型类中的静态方法和静态变量？

泛型类中的**静态方法和静态变量不可以使用泛型类所声明的泛型类型参数**

**举例：**

```java
public class Test2<T> {    
    public static T one;   //编译错误    
    public static  T show(T one){ //编译错误    
        return null;    
    }    
}
```

因为泛型类中的**泛型参数的实例化是在定义对象的时候指定的**，而**静态变量和静态方法不需要使用对象来调用**。对象都没有创建，如何确定这个泛型参数是何种类型，所以当然是错误的。

但是要注意区分下面的一种情况：

```java
public class Test2<T> {    

    public static <T >T show(T one){ //这是正确的    
        return null;    
    }    
}
```

因为这是一个泛型方法，**在泛型方法中使用的T是自己在方法中定义的 T，而不是泛型类中的T**。

### 3.10 如何理解异常中使用泛型？

> **不能抛出也不能捕获泛型类的对象。**

事实上，泛型类扩展`Throwable`都不合法。

例如：下面的定义将不会通过编译：

```java
public class Problem<T> extends Exception {

}
```

**为什么不能扩展`Throwable`，因为异常都是在运行时捕获和抛出的，而在编译的时候，泛型信息全都会被擦除掉**

```java
/**
 * 如果假设上边编译可行，看如下定义
 */

try{

} catch(Problem<Integer> e1) {

} catch(Problem<Number> e2) {

} 

// 类型信息被擦除后，那么两个地方的catch都变为原始类型Object，那么也就是说，这两个地方的catch变的一模一样,就相当于下面的这样
try{

} catch(Problem<Object> e1) {

} catch(Problem<Object> e2) {

}

```

> **不能再catch子句中使用泛型变量**

```java
public static <T extends Throwable> void doWork(Class<T> t) {
    try {
        ...
    } catch(T e) { //编译错误
        ...
    }
}
```

因为泛型信息在编译的时候已经变为原始类型，也就是说上面的T会变为原始类型Throwable，那么如果可以在  `catch`子句中使用泛型变量，那么，下面的定义呢：

```java
public static <T extends Throwable> void doWork(Class<T> t){
    try {

    } catch(T e) { //编译错误

    } catch(IndexOutOfBounds e) {

    }                         
}
```

根据**异常捕获的原则**，**一定是子类在前面，父类在后面，那么上面就违背了这个原则**。即使你在使用该静态方法的使用 T 是`ArrayIndexOutofBounds`，在编译之后还是会变成`Throwable`，`ArrayIndexOutofBounds`是`IndexOutofBounds`的子类，违背了异常捕获的原则。

所以`java`为了避免这样的情况，禁止在`catch`子句中使用泛型变量。

> **在异常声明中可以使用类型变量。下面方法是合法的。**

```java
public static<T extends Throwable> void doWork(T t) throws T {
    try{
        ...
    } catch(Throwable realCause) {
        t.initCause(realCause);
        throw t; 
    }
}
```

### 3.11 如何获取泛型的参数类型?

既然类型被擦除了，那么如何获取泛型的参数类型呢？可以通过反射（`java.lang.reflect.Type`）获取泛型。

`java.lang.reflect.Type`是Java中所有类型的公共高级接口, 代表了Java中的所有类型。`Type`体系中类型的包括：

- 数组类型(`GenericArrayType`)
- 参数化类型(`ParameterizedType`)
- 类型变量(`TypeVariable`)
- 通配符类型(`WildcardType`)
- 原始类型(`Class`)
- 基本类型(`Class`)

以上这些类型都实现Type接口。

```java
public class GenericType<T> {
    private T data;

    public T getData() {
        return data;
    }

    public void setData(T data) {
        this.data = data;
    }

    public static void main(String[] args) {
        GenericType<String> genericType = new GenericType<String>() {};
        Type superclass = genericType.getClass().getGenericSuperclass();
        //getActualTypeArguments 返回确切的泛型参数, 如Map<String, Integer>返回[String, Integer]
        Type type = ((ParameterizedType) superclass).getActualTypeArguments()[0]; 
        System.out.println(type);//class java.lang.String
    }
}
```

其中 ParameterizedType:

```java
public interface ParameterizedType extends Type {
    // 返回确切的泛型参数, 如Map<String, Integer>返回[String, Integer]
    Type[] getActualTypeArguments();
    
    //返回当前class或interface声明的类型, 如List<?>返回List
    Type getRawType();
    
    //返回所属类型. 如,当前类型为O<T>.I<S>, 则返回O<T>. 顶级类型将返回null 
    Type getOwnerType();
}
```