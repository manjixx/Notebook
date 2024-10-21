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

### 2.4 异常的自定义

### 2.5 异常的捕获

### 2.6 常用的异常

### 2.7 总结

****

## 三、异常实践

****

## 四、深入理解异常
