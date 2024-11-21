# Exceptions 异常

Java 异常是 Java 提供的**一种识别及响应错误的一致性机制**，Java 异常机制可以**使程序中异常处理代码和正常业务代码分离**，保证程序代码更加优雅，并提高程序健壮性。

## 一、异常的层次结构

异常指不期而至的各种状况，如：文件找不到、网络连接失败、非法参数等。

异常是一个事件，它**发生在程序运行期间，干扰了正常的指令流程**。Java通过 `API`中`Throwable`类的众多子类描述各种不同的异常。因而，**`Java`异常都是对象，是`Throwable`子类的实例，描述了出现在一段编码中的错误条件**。

**当条件生成时，错误将引发异常**。

Java 异常类层次结构图

![](https://pdai.tech/images/java/java-basic-exception-1.png)

> **Throwable**

`Throwable` 是 `Java` 语言中**所有错误与异常的超类**。

`Throwable` 包含两个子类：`Error`（错误）和 `Exception`（异常），它们通常**用于指示发生了异常情况**。

`Throwable` 包含了其线程创建时线程执行堆栈的快照，它提供了 `printStackTrace()` 等接口用于获取堆栈跟踪数据等信息。

> **Error**

Error 类及其子类：程序中无法处理的错误，表示运行应用程序中出现了严重的错误。

此类错误**一般表示代码运行时 JVM 出现问题**。通常有:

- `Virtual MachineError`（虚拟机运行错误）
- `NoClassDefFoundError`（类定义错误）、
- `OutOfMemoryError`：内存不足错误
- `StackOverflowError`：栈溢出错误。
  
此类错误发生时，JVM 将终止线程。**这些错误是不受检异常，非代码性错误。因此，当此类错误发生时，应用程序不应该去处理此类错误。**

按照Java惯例，我们是不应该实现任何新的Error子类！

> **Exception**

程序本身可以捕获并且可以处理的异常。

Exception 这种异常又分为两类：运行时异常和编译时异常。

- **运行时异常**

RuntimeException 类及其子类异常，如`NullPointerException`(空指针异常)、`IndexOutOfBoundsException`(下标越界异常)等，这些异常是**不检查异常**，程序中可以选择捕获处理，也可以不处理。

这些异常一般是由程序逻辑错误引起的，程序应该从逻辑角度尽可能避免这类异常的发生。

运行时异常的特点是Java编译器不会检查它，也就是说，当程序中可能出现这类异常，即使没有用`try-catch`语句捕获它，也没有用`throws`子句声明抛出它，也会编译通过。

- **非运行时异常 （编译异常）**

`RuntimeException`以外的异常，类型上都属于`Exception`类及其子类。从程序语法角度讲是必须进行处理的异常，**如果不处理，程序就不能编译通过**。

如`IOException`、`SQLException`等以及用户自定义的`Exception`异常，一般情况下不自定义检查异常。

> **可查异常（checked Exceptions）和不可查异常（unchecked Exceptions）**

- **可查异常（编译器要求必须处置的异常）**：

正确的程序在运行中，很容易出现的、情理可容的异常状况。

**可查异常虽然是异常状况，但在一定程度上它的发生是可以预计的，而且一旦发生这种异常状况，就必须采取某种方式进行处理**。

除了`RuntimeException`及其子类以外，其他的`Exception`类及其子类都属于可查异常。

**这种异常的特点**是`Java`编译器会检查它，也就是说，当程序中可能出现这类异常，要么用`try-catch`语句捕获它，要么用`throws`子句声明抛出它，否则编译不会通过。

- **不可查异常（编译器不要求强制处置的异常）**

包括运行时异常（`RuntimeException`与其子类）和错误（`Error`）。

****

## 二、异常基础

### 2.1 异常关键字

`try` – **用于监听**。将要被监听的代码(可能抛出异常的代码)放在`try`语句块之内，当`try`语句块内发生异常时，异常就被抛出。
`catch` – **用于捕获异常**。`catch`用来捕获try语句块中发生的异常。
`finally` – `finally`语句块总是会被执行。它主要**用于回收在`try`块里打开的物力资源**(如数据库连接、网络连接和磁盘文件)。**只有`finally`块，执行完成之后，才会回来执行`try`或者`catch`块中的`return`或者`throw`语句**；如果`finally`中使用了`return`或者`throw`等终止方法的语句，则就不会跳回执行，直接停止。
`throw`– 用于抛出异常。
`throws` – 用在方法签名中，用于声明该方法可能抛出的异常。

### 2.2 异常的申明（throws）

在`Java`中，当前执行的语句必属于某个方法，`Java`解释器调用`main`方法执行开始执行程序。

若方法中**存在检查异常**，如果不对其捕获，**那必须在方法头中显式声明该异常**，以便于告知方法调用者此方法有异常，需要进行处理。

在方法中声明一个异常，方法头中使用关键字`throws`，后面接上要声明的异常。若声明多个异常，则使用逗号分割。如下所示：

```java
public static void method() throws IOException, FileNotFoundException{
    //something statements
}
```

注意：**若是父类的方法没有声明异常，则子类继承方法后，也不能声明异常。**

通常，**应该捕获那些知道如何处理的异常，将不知道如何处理的异常继续传递下去**。

传递异常可以在方法签名处使用 `throws` 关键字声明可能会抛出的异常。

```java
private static void readFile(String filePath) throws IOException {
    File file = new File(filePath);
    String result;
    BufferedReader reader = new BufferedReader(new FileReader(file));
    while((result = reader.readLine())!=null) {
        System.out.println(result);
    }
    reader.close();
}
```

`Throws`抛出异常的规则：（❌）

- 如果是**不可查异常（`unchecked exception`）**，即`Error、RuntimeException`或它们的子类，那么可以不使用`throws`关键字来声明要抛出的异常，编译仍能顺利通过，但在运行时会被系统抛出。
- **必须声明方法可抛出的任何可查异常（`checked exception`）**。即如果一个方法可能出现受可查异常，**要么用`try-catch`语句捕获，要么用`throws`子句声明将它抛出**，否则会导致编译错误。
- 仅当抛出了异常，该方法的调用者才必须处理或者重新抛出该异常。当方法的调用者无力处理该异常的时候，应该继续抛出，而不是囫囵吞枣。
- **调用方法必须遵循任何可查异常的处理和声明规则**。若覆盖一个方法，则不能声明与覆盖方法不同的异常。声明的任何异常必须是被覆盖方法所声明异常的同类或子类。

### 2.3 异常的抛出（throw）

如果代码可能会引发某种错误，可以创建一个合适的异常类实例并抛出它，这就是抛出异常。如下所示：

```java
public static double method(int value) {
    if(value == 0) {
        throw new ArithmeticException("参数不能为0"); //抛出一个运行时异常
    }
    return 5.0 / value;
}
```

**大部分情况下都不需要手动抛出异常**，因为Java的大部分方法要么已经处理异常，要么已声明异常。所以**一般都是捕获异常或者再往上抛。**

**有时我们会从 `catch` 中抛出一个异常**，目的是为了改变异常的类型。多用于在多系统集成时，当某个子系统故障，异常类型可能有多种，可以用统一的异常类型向外暴露，不需暴露太多内部异常细节。

```java
private static void readFile(String filePath) throws MyException {    
    try {
        // code
    } catch (IOException e) {
        MyException ex = new MyException("read file failed.");
        ex.initCause(e);
        throw ex;
    }
}
```

### 2.4 异常的自定义

定义一个异常类应包含两个构造函数，

- 一个无参构造函数
- 一个带有详细描述信息的构造函数（Throwable 的 toString 方法会打印这些详细信息，调试时很有用）

```java
public class MyException extends Exception {
    public MyException(){ }
    public MyException(String msg){
        super(msg);
    }
    // ...
}
```

### 2.5 异常的捕获

异常捕获处理的方法通常有：

- `try-catch`
- `try-catch-finally`
- `try-finally`
- `try-with-resource`

> **try-catch**

在一个 `try-catch` 语句块中可以捕获多个异常类型，并对不同类型的异常做出不同的处理

```java
private static void readFile(String filePath) {
    try {
        // code
    } catch (FileNotFoundException e) {
        // handle FileNotFoundException
    } catch (IOException e){
        // handle IOException
    }
}
```

同一个 `catch` 也可以捕获多种类型异常，用 `|` 隔开

```java
private static void readFile(String filePath) {
    try {
        // code
    } catch (FileNotFoundException | UnknownHostException e) {
        // handle FileNotFoundException or UnknownHostException
    } catch (IOException e){
        // handle IOException
    }
}
```

> **try-catch-finally**

- 常规语法

```java
try {                        
    //执行程序代码，可能会出现异常                 
} catch(Exception e) {   
    //捕获异常并处理   
} finally {
    //必执行的代码
}
```

- 执行顺序
  
  - **当try没有捕获到异常时**：try语句块中的语句逐一被执行，程序将跳过catch语句块，执行finally语句块和其后的语句；
  - **当try捕获到异常，catch语句块里没有处理此异常的情况**：当try语句块里的某条语句出现异常时，而没有处理此异常的catch语句块时，此异常将会抛给JVM处理，finally语句块里的语句还是会被执行，但finally语句块后的语句不会被执行；
  - **当try捕获到异常，catch语句块里有处理此异常的情况**：在try语句块中是按照顺序来执行的，当执行到某一条语句出现异常时，程序将跳到catch语句块，并与catch语句块逐一匹配，找到与之对应的处理程序，其他的catch语句块将不会被执行，而try语句块中，出现异常之后的语句也不会被执行，catch语句块执行完后，执行finally语句块里的语句，最后执行finally语句块后的语句；

- 案例
  
```java
private static void readFile(String filePath) throws MyException {
    File file = new File(filePath);
    String result;
    BufferedReader reader = null;
    try {
        reader = new BufferedReader(new FileReader(file));
        while((result = reader.readLine())!=null) {
            System.out.println(result);
        }
    } catch (IOException e) {
        System.out.println("readFile method catch block.");
        MyException ex = new MyException("read file failed.");
        ex.initCause(e);
        throw ex;
    } finally {
        System.out.println("readFile method finally block.");
        if (null != reader) {
            try {
                reader.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
```

> **try-finally**

try块中引起异常，异常代码之后的语句不再执行，直接执行finally语句。

try块没有引发异常，则执行完try块就执行finally语句。**try-finally可用在不需要捕获异常的代码，可以保证资源在使用后被关闭**。例如IO流中执行完相应操作后，关闭相应资源；使用Lock对象保证线程同步，通过finally可以保证锁会被释放；数据库连接代码时，关闭连接操作等等。

```java
//以Lock加锁为例，演示try-finally
ReentrantLock lock = new ReentrantLock();
try {
    //需要加锁的代码
} finally {
    lock.unlock(); //保证锁一定被释放
}
```

`finally` 遇到如下情况下不会执行：

- 在前面的代码中用了`System.exit()`退出程序。
- `finally`语句块中发生了异常。
- 程序所在的线程死亡。
- 关闭CPU。

> **try-with-resouce**

上面例子中，`finally` 中的 `close` 方法也可能抛出 `IOException`, 从而覆盖了原始异常。`JAVA 7` 提供了更优雅的方式来实现资源的自动释放，**自动释放的资源需要是实现了 `AutoCloseable` 接口的类**。

- 代码实现

```java
private  static void tryWithResourceTest(){
    try (Scanner scanner = new Scanner(new FileInputStream("c:/abc"),"UTF-8")){
        // code
    } catch (IOException e){
        // handle exception
    }
}
```

- Scanner 代码

```java
public final class Scanner implements Iterator<String>, Closeable {
  // ...
}
public interface Closeable extends AutoCloseable {
    public void close() throws IOException;
}
```

`try` 代码块退出时，会自动调用 `scanner.close` 方法，**和把 `scanner.close` 方法放在 `finally` 代码块中不同的是，若 `scanner.close` 抛出异常，则会被抑制，抛出的仍然为原始异常**。被抑制的异常会由 `addSusppressed` 方法添加到原来的异常，如果想要获取被抑制的异常列表，可以调用 `getSuppressed` 方法来获取。

### 2.6 常用的异常

> **RuntimeException**

- `java.lang.ArrayIndexOutOfBoundsException` 数组索引越界异常。当对数组的索引值为负数或大于等于数组大小时抛出。
- `java.lang.ArithmeticException` 算术条件异常。譬如：整数除零等。
- `java.lang.NullPointerException` 空指针异常。当应用试图在要求使用对象的地方使用了null时，抛出该异常。譬如：调用null对象的实例方法、访问null对象的属性、计算null对象的长度、使用throw语句抛出null等等
- `java.lang.ClassNotFoundException` 找不到类异常。当应用试图根据字符串形式的类名构造类，而在遍历CLASSPAH之后找不到对应名称的class文件时，抛出该异常。
- `java.lang.NegativeArraySizeException` 数组长度为负异常
- `java.lang.ArrayStoreException` 数组中包含不兼容的值抛出的异常
- `java.lang.SecurityException` 安全性异常
- `java.lang.IllegalArgumentException` 非法参数异常

> **IOException**

- `IOException`：操作输入流和输出流时可能出现的异常。
- `EOFException` 文件已结束异常
- `FileNotFoundException` 文件未找到异常

> **其他**

- `ClassCastException` 类型转换异常类
- `ArrayStoreException` 数组中包含不兼容的值抛出的异常
- `SQLException` 操作数据库异常类
- `NoSuchFieldException` 字段未找到异常
- `NoSuchMethodException` 方法未找到抛出的异常
- `NumberFormatException` 字符串转换为数字抛出的异常
- `StringIndexOutOfBoundsException` 字符串索引超出范围抛出的异常
- `IllegalAccessException` 不允许访问某类异常
- `InstantiationException` 当应用程序试图使用`Class`类中的`newInstance()`方法创建一个类的实例，而指定的类对象无法被实例化时，抛出该异常

### 2.7 总结

- try、catch和finally都不能单独使用，只能是try-catch、try-finally或者try-catch-finally。
- try语句块监控代码，出现异常就停止执行下面的代码，然后将异常移交给catch语句块来处理。
- finally语句块中的代码一定会被执行，常用于回收资源 。
- throws：声明一个异常，告知方法调用者。
- throw ：抛出一个异常，至于该异常被捕获还是继续抛出都与它无关。

Java编程思想一书中，对异常的总结。

- 在恰当的级别处理问题。（在知道该如何处理的情况下了捕获异常。）
- 解决问题并且重新调用产生异常的方法。
- 进行少许修补，然后绕过异常发生的地方继续执行。
- 用别的数据进行计算，以代替方法预计会返回的值。
- 把当前运行环境下能做的事尽量做完，然后把相同的异常重抛到更高层。
- 把当前运行环境下能做的事尽量做完，然后把不同的异常抛到更高层。
- 终止程序。进行简化（如果你的异常模式使问题变得太复杂，那么用起来会非常痛苦）。
- 让类库和程序更安全。

****

## 三、异常实践

> **提示**
> 在 Java 中处理异常并不是一个简单的事情。不仅仅初学者很难理解，即使一些有经验的开发者也需要花费很多时间来思考如何处理异常，包括需要处理哪些异常，怎样处理等等。这也是绝大多数开发团队都会制定一些规则来规范进行异常处理的原因。

异常不仅仅是一个**错误控制机制**，也是一个**通信媒介**。因此，为了和同事更好的合作，一个团队必须要制定出一个**最佳实践和规则**，只有这样，团队成员才能理解这些通用概念，同时在工作中使用它。

### 3.1 只针对不正常的情况才使用异常

> 异常只应该被用于不正常的条件，它们永远不应该被用于正常的控制流。《阿里手册》中：【强制】Java 类库中定义的可以**通过预检查方式规避的`RuntimeException`异常不应该通过`catch` 的方式来处理**，比如：`NullPointerException，IndexOutOfBoundsException`等等。

举例：**在解析字符串形式的数字时，可能存在数字格式错误**，不得通过`catch Exception`来实现

- 代码1

```java
if (obj != null) {
  //...
}
```

- 代码2

```java
try { 
  obj.method(); 
} catch (NullPointerException e) {
  //...
}
```

主要原因有三点：

- 异常机制的设计初衷是用于不正常的情况，所以很少会有JVM试图实现对异常机制的性能进行优化。所以，创建、抛出和捕获异常的开销是很昂贵的。
- 把代码放在`try-catch`中返回阻止了JVM实现本来可能要执行的某些特定的优化。
- **对数组进行遍历的标准模式并不会导致冗余的检查**，有些现代的JVM实现会将它们优化掉。

### 3.2 在 finally 块中清理资源或者使用 try-with-resource 语句

> **错误示例**

```java
public void doNotCloseResourceInTry() {
    FileInputStream inputStream = null;
    try {
        File file = new File("./tmp.txt");
        inputStream = new FileInputStream(file);
        // use the inputStream to read a file
        // do NOT do this
        inputStream.close();
    } catch (FileNotFoundException e) {
        log.error(e);
    } catch (IOException e) {
        log.error(e);
    }
}
```

上述代码问题在于：没有异常抛出的时候，这段代码才可以正常工作。try 代码块内代码会正常执行，并且资源可以正常关闭。但是，当异常抛出时，这意味着代码可能不会执行到 try 代码块的最后部分。结果就是，资源无法被正常关闭。

因此应该把**清理工作的代码放到 finally 里去，或者使用 try-with-resource 特性**。

- 方法一：使用finally 代码块

```java
public void closeResourceInFinally() {
    FileInputStream inputStream = null;
    try {
        File file = new File("./tmp.txt");
        inputStream = new FileInputStream(file);
        // use the inputStream to read a file
    } catch (FileNotFoundException e) {
        log.error(e);
    } finally {
        if (inputStream != null) {
            try {
                inputStream.close();
            } catch (IOException e) {
                log.error(e);
            }
        }
    }
}
```

- 方法二：Java 7 的 `try-with-resource` 语法

如果你的资源实现了 `AutoCloseable` 接口，可以使用这个语法。大多数的 `Java` 标准资源都继承了这个接口。当你在 try 子句中打开资源，**资源会在 try 代码块执行后或异常处理后自动关闭**。

```java
public void automaticallyCloseResource() {
    File file = new File("./tmp.txt");
    try (FileInputStream inputStream = new FileInputStream(file);) {
        // use the inputStream to read a file
    } catch (FileNotFoundException e) {
        log.error(e);
    } catch (IOException e) {
        log.error(e);
    }
}
```

### 3.3 尽量使用标准异常

**代码复用是值得提倡的，这是一条通用规则，异常也不例外**。

复用现有异常有如下好处：

- 使得API更加易于学习和使用，因为其与程序员原来已经熟悉的习惯用法是一致的。
- 对于用到这些API的程序而言，它们的可读性更好，因为它们不会充斥着程序员不熟悉的异常。
- **异常类越少，意味着内存占用越小，并且转载这些类的时间开销也越小**。

Java 标准异常中有几个是经常被使用的异常，如下表格：

| 异常  | 使用场合  |
|---|---|
| IllegalArgumentException  | 参数值不合适  |
| IllegalStateException  | 参数状态不合适  |
| NullPointerExceptioin  | 在null被禁止的状况下参数值为null  |
| IndexOutOfBoundException  | 下标越界  |
| ConcurrentModificationException  |  在禁止并发修改的情况下，对象检测到并发修改 |
| UnsupportedOperationException  | 对象不支持客户请求的方法  |

注意：

- 在许可的条件下，其它的异常也可以被重用
- 选择重用哪一种异常并没有必须遵循的规则

****

## 四、深入理解异常
