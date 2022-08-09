# 一、IO概念

## 1.1 定义

Java中I/O操作主要是指使用Java进行输入，输出操作. Java所有的I/O机制都是基于数据流进行输入输出，这些数据流表示了字符或者字节数据的流动序列。Java的I/O流提供了读写数据的标准方法。任何Java中表示数据源的对象都会提供以数据流的方式读写它的数据的方法。

## 1.2 类库

流IO库:java.io,大多数面向数据流的输入/输出类的主要软件包。

块IO库:java.nio,提供块传输。

流IO的好处是简单易用，缺点是效率较低。块IO效率很高，但编程比较复杂。

## 1.3 Java IO模型

Java的IO模型设计非常优秀，它使用Decorator模式，按功能划分Stream，可以动态装配这些Stream，以便获得需要的功能。

如果需要一个**具有缓冲的文件输入流**，则应当组合使用**FileInputStream**和**BufferedInputStream**。

# 二、数据流的基本概念

## 2.1 流的基本概念

通过“流”的形式允许java程序使用相同的方式来访问不同的输入/输出源。

stream是从起源（source）到接收的（sink）的有序数据。我们这里把输入/输出源对比成“水桶”，那么流就是“管道”，这个“管道”的粗细、单向性等属性也就是区分了不同“流”的特性。

 流是一个很形象的概念，当程序需要读取数据的时候，就会开启一个通向数据源的流，这个数据源可以是文件，内存，或是网络连接。类似的，当程序需要写入数据的时候，就会开启一个通向目的地的流。

## 2.2 使用范围

在Java类库中，IO部分的内容是很庞大的，因为它涉及的领域很广泛:**标准输入输出，文件的操作，网络上的数据流，字符串流，对象流，zip文件流**等等，java中将输入输出抽象称为流。
![]()

## 2.3 java中IO流分类

> **java中流汇总**

![java中流汇总](https://segmentfault.com/img/remote/1460000023008392)

- 按照流的流向分，可以分为输入流和输出流；
- 按照操作单元划分，可以划分为字节流和字符流；
  ![按照操作方式的分类结构图](https://my-blog-to-use.oss-cn-beijing.aliyuncs.com/2019-6/IO-%E6%93%8D%E4%BD%9C%E6%96%B9%E5%BC%8F%E5%88%86%E7%B1%BB.png)
- 按照流的角色划分为节点流和处理流
  ![按照操作对象的分类结构图](https://my-blog-to-use.oss-cn-beijing.aliyuncs.com/2019-6/IO-%E6%93%8D%E4%BD%9C%E5%AF%B9%E8%B1%A1%E5%88%86%E7%B1%BB.png)


### 2.3.1 输入流和输出流

> **基本概念**

- 输入流（Input  Stream）：程序从输入流读取数据源。数据源包括外界(键盘、文件、网络…)，即是将数据源读入到程序的通信通道

- 输出流：程序向输出流写入数据。将程序中的数据输出到外界（显示器、打印机、文件、网络…）的通信通道。

![输入流与输出流](https://oss-emcsprod-public.modb.pro/wechatSpider/modb_20211217_2d878988-5eec-11ec-abfd-fa163eb4f6be.png)
Java Io 流共涉及 40 多个类，这些类看上去很杂乱，但实际上很有规则，而且彼此之间存在非常紧密的联系， Java I0 流的 40 多个类都是从如下 4 个抽象类基类中派生出来的。
  - InputStream/Reader: 所有的输入流的基类，前者是字节输入流，后者是字符输入流。
  - OutputStream/Writer: 所有输出流的基类，前者是字节输出流，后者是字符输出流。
  
> **输入字节流(InputStream)和输出字节流(OutputStream)**

- InputStream 是所有的输入字节流的父类，它是一个抽象类。
    - `ByteArrayInputStream`、`StringBufferInputStream`、`FileInputStream`是三种基本的介质流，它们分别从Byte 数组、StringBuffer、和本地文件中读取数据。
    - `PipedInputStream`是从与其它线程共用的管道中读取数据
    - `ObjectInputStream`和所有`FilterInputStream`的子类都是装饰流（装饰器模式的主角）。

- OutputStream 是所有的输出字节流的父类，它是一个抽象类。
  - `ByteArrayOutputStream`、`FileOutputStream`是两种基本的介质流，它们分别向Byte 数组、和本地文件中写入数据。
  - `PipedOutputStream`是向与其它线程共用的管道中写入数据。  
  - `ObjectOutputStream`和所有`FilterOutputStream`的子类都是装饰流。


### 2.3.2 字符流和字节流

> **既然有了字节流,为什么还要有字符流?**

该问题的本质是：不管是文件读写还是网络传输，信息最小的存储单元都是字节，那么io操作还要分为字节流和字符操作

字符流是由 Java 虚拟机将字节转换得到的，问题就出在这个过程还算是非常耗时，并且，如果我们不知道编码类型就很容易出现乱码问题。所以， I/O 流就干脆提供了一个直接操作字符的接口，方便我们平时对字符进行流操作。

因为数据编码的不同，而有了对字符进行高效操作的流对象。本质其实就是基于字节流读取时，去查了指定的码表。

> **字符流与字节流的区别**

- 读写单位不同：字节流以字节（8bit）为单位，字符流以字符为单位，根据码表映射字符，一次可能读多个字节。

- 处理对象不同：字节流能处理所有类型的数据（如图片、avi等），而字符流只能处理字符类型的数据。

- 字节流：一次读入或读出是8位二进制。

- 字符流：一次读入或读出是16位二进制。


只要是处理纯文本数据，就优先考虑使用字符流。 除此之外都使用字节流。

### 2.3.3 节点流与处理流

> **节点流**
- 直接与数据源相连，读入或读出。

![节点流](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwMTA1MTk0NDEyMjcx)

- 常用节点流:
  - **父　类** ：InputStream 、OutputStream、 Reader、 Writer
  - **文　件** ：FileInputStream 、 FileOutputStrean 、FileReader 、FileWriter 文件进行处理的节点流
  - **数　组** ：ByteArrayInputStream、 ByteArrayOutputStream、 CharArrayReader 、CharArrayWriter 对数组进行处理的节点流（对应的不再是文件，而是内存中的一个数组）
  - **字符串** ：StringReader、 StringWriter 对字符串进行处理的节点流
  - **管　道** ：PipedInputStream 、PipedOutputStream 、PipedReader 、PipedWriter 对管道进行处理的节点流


> **处理流**
- 对一个已经存在的流进行连接或封装，通过封装后的流来实现数据读/写功能。相当于在这个水管上面装了一些“控制阀门”，最终用户只要关心“阀门”具备的能力就行
![处理流](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTcwMTA1MTk0NTIyMzkw)

- **常用处理流**
  - **缓冲流**：BufferedInputStrean 、BufferedOutputStream、 BufferedReader、 BufferedWriter 增加缓冲功能，避免频繁读写硬盘。
  - **转换流**：InputStreamReader 、OutputStreamReader实现字节流和字符流之间的转换。
  - **数据流**： DataInputStream 、DataOutputStream 等-提供将基础数据类型写入到文件中，或者读取出来。


# 三、常见的IO流实践

## 4.1 访问操作文件

涉及FileInputStream/FileReader ，FileOutputStream/FileWriter四个类。

### 4.1.1 使用`FileInputStream`，从文件读取数据

```JAVA
import java.io.*;

public class TestFileInputStream{
    public static void main(String[] args){
        int b = 0;
        FileInputStream in = null;
        try{
            in = new FileInputStream("filepath");
        }catch(FileNotFoundException e){
            System.out.println("file not found");
            System.exit(- 1);
        }

        try{
            long num = 0;
            while((b = in.read()) != - 1){
                 System.out.println((char) b);
                 num++;
            }
            in.close();
			System.out.println();
			System.out.println("共读取了"+num+"个字节");
        }catch(IOException e){
			System.out.println("IO异常，读取失败");
			System.exit(-1);
        }
    }
}
```

### 4.1.2 使用`FileOutputStream`，往文件里写数据
```java
import java.io.*;
public class TextFileOutputStream {

	public static void main(String[] args) {
		int b=0;
		FileInputStream in = null;
		FileOutputStream out = null;
		try {
		in =new FileInputStream("inputfilepath");
		out=new FileOutputStream("outputfilepath");
		}catch(FileNotFoundException e){
			System.out.println("file is not found");
			System.exit(-1);
		}
		try {
			while ((b=in.read())!=-1) {
				out.write(b);
			}
			in.close();
			out.close();
		}catch(IOException e) {
			System.out.println("IO异常，读取失败");
			System.exit(-1);
		}
		System.out.println("文件复制完成");
	}
}
```

## 4.2 缓存流的使用

主要涉及 `BufferedInputStream/BufferedOutputStream`，`BufferedReader/BufferedWriter`

他们最基本的其实也是FileInputStream和FileOutputStream，在这个“流”的基础上，又加了缓存的功能流BufferedInputStream和BufferedOutputStream。

```java
import java.io.*;

public class TestBufferStream{
    public static void main(String[] args) throws IOException{
        BufferedInputStream bis = null;
        BufferedOutputStream bos = null;
        try{
            FileInputStream fis = new FileInputStream("InputFilePath");
            FileOutputStream fos = new FileOutputStream("OutputFilePath");
            bis = new BufferedInputStream(fis);
            bos = new BufferedOutputStream(fos);
            byte[] b = new byte[1024];
            int off = 0;
            while((off = bis.read(b)) > 0){
                bos.write(b, 0, off);
            }
            bis.close();
            bos.close();
        }catch(IOException e){
            e.printStackeTrace();
        }finally{
            bis.close();
            bos.close();
        }
    }
}
```
## 4.3 转换流的使用


`InputStreamReader`、`OutputStreamWriter`


字面意思理解，转化流就是用来转化的,其是将`InputStream`或`OutputStream`作为参数，实现从字节流到字符流的转换。

构造函数：
```JAVA
InputStreamReader(InputStream);        //通过构造函数初始化，使用的是本系统默认的编码表GBK。
InputStreamReader(InputStream,String charSet);   //通过该构造函数初始化，可以指定编码表。
OutputStreamWriter(OutputStream);      //通过该构造函数初始化，使用的是本系统默认的编码表GBK。
OutputStreamwriter(OutputStream,String charSet);   //通过该构造函数初始化，可以指定编码表。
```

读取键盘输入的每一行内容，并写入到文本中，直到遇到over行结束输入

readLine()方法在进行读取一行时，只有遇到回车(\r)或者换行符(\n)才会返回读取结果，这就是“读取一行的意思”

```JAVA
import java.io.*;

public class TransStreamTest{
    public static void main(String[] args) throws IOException{
        BufferedReader br = new BufferedReader(new InputStream(System.in()));
        BufferedWriter bw = new BufferedWriter(new FileWriter("outPutFilePath"));

        String line = null;

        while((line = br.readLine()) != null){
            if("over".contentEquals(line)){
                break;
            }
            bw.write(line);
            bw.newLine();
            bw.flush();
        }

        bw.close();
        br.close();
    }
}
```

## 4.4 对象流的使用

字节和字符流，包括封装在他们上面的处理流，那么我们想，在程序设计的过程中，我们都是用类和对象来描述定义，能不能直接把对象进行传输。


对象流其实就是一种特殊的处理流水，也是在基础的字节流上去作封装。【可以应用于游戏存盘】

下面程序使用一个对象流，把对象直接写到文件中

```java
import java.io.*;

pulbic class ObjectStreamTest{
    public static void main(String[] args) throws Exception{
        try{
            Person P = new Preson("Jeccica",26);
            FileOutputStream fos = new FileOutputStream("outPutFilePath");
            ObjectOutputStream oos = new ObjectOutputStream(fos);

            oos.writeObject(P);

            oos.flush();

            oos.close();
        }catch(FileNotFoundException e){
            e.printStackTrace();
        }catch(IOException e){
            e.printStackeTrace()
        }

        FileInputStream fis = new FileInputStream("inputFilePath");
        ObjectOutputStream ois = new ObjectInputStream(fis);
        Person P2 = (Person)ois.readObject();
        System.out.println(P2.name + "的年龄为" + P2.age);
    }
}

Class Person implements Serializable{
    String name = null;
    int age = 0;
    Person(String name,int age){
        this.name = name;
        this.age = age;
    }
}
```
## 4.5 字节数组流的使用

`ByteArrayInputStream/ByteArrayOutputStream`,通常结合数据流`DataInputStream/DataOutputStream`

我们分析了常见的节点流和常见的处理流等，经常而言我们都是针对文件的操作，然后带上缓冲的节点流进行处理，但有时候为了提升效率，我们发现频繁的读写文件并不是太好，那么于是出现了字节数组流，即存放在内存中，因此有称之为内存流；

其中字节数组流也一种节点流；

除了节点流外，我们也将学习另外一种处理流，即数据流。

数据处理流是用于针对数据类型传输处理的，是一种处理流，即是在节点流之上的增强处理，一般用于序列化和反序列化的时候用到。

```java
import java.io.*;

public class DataStream{
    public static void main(String[] args){
        // 创建字节数组流，同时会在内存中创建数组
        ByteArrayOutputStream baos = new ByteArrayOutputStream();

        // 对字节数组流外封装成数据处理流
        DataOutputStream dos = new DataOutputStream(baos);

        try{
            // 利用数据流里面的写法，写一个Double类型的随机数据
            dos.writeDouble(Math.random());
            dos.writeBoolean(true);
            // toByteArray()方法是创建一个新分配的字节数组。
            // 数组的大小和当前输出流的大小。这里指的是baos这个字节数组
            ByteArrayInputStream bias = new ByteArrayInputStream(baos.toByteArray());
            System.out.println(bias.available());
            DataInputStream dis = new DataInputStream(bias);
            System.out.println(dis.readDouble());
            System.out.println(dis.readBoolean());
            dos.close();
            dis.close();
        }cathc(IOException e){
            e.printStackeTrace();
        }
    }
}
```
# 四、常见IO流的问题

## 4.1 BIO、NIO与AIO的区别

> **BIO**
BIO(Blocking I/O):同步阻塞 I/O 模式，数据的读取写入必须阻塞在一个线程内等待其完成。

在活动连接数不是特别高（小于单机 1000）的情况下，这种模型是比较不错的，可以让每一个连接专注于自己的 I/O 并且编程模型简单，也不用过多考虑系统的过载、限流等问题。线程池本身就是一个天然的漏斗，可以缓冲一些系统处理不了的连接或请求。

但是，**当面对十万甚至百万级连接的时候**，传统的 BIO 模型是无能为力的。因此，我们需要一种更高效的 I/O 处理模型来应对更高的并发量。


> **NIO**
NIO(Non-blocking/New I/O): NIO 是一种同步非阻塞的 I/O 模型，在 Java 1.4 中引入了 NIO 框架，对应 java.nio 包，提供了 Channel , Selector，Buffer 等抽象。**NIO 中的 N 可以理解为 Non-blocking**，不单纯是 New。

**它支持面向缓冲的，基于通道的 I/O 操作方法。**

 NIO 提供了与传统 BIO 模型中的 Socket 和 ServerSocket 相对应的 SocketChannel 和 ServerSocketChannel 两种不同的套接字通道实现,两种通道都支持阻塞和非阻塞两种模式。
 
 阻塞模式使用就像传统中的支持一样，比较简单，但是性能和可靠性都不好；
 
 非阻塞模式正好与之相反。**对于低负载、低并发的应用程序**，可以使用同步阻塞 I/O 来提升开发速率和更好的维护性；**对于高负载、高并发的（网络）应用**，应使用 NIO 的非阻塞模式来开发

> **AIO**

AIO 也就是 NIO 2。在 Java 7 中引入了 NIO 的改进版 NIO 2,它是异步非阻塞的 IO 模型。

异步 IO 是基于事件和回调机制实现的，也就是应用操作之后会直接返回，不会堵塞在那里，当后台处理完成，操作系统会通知相应的线程进行后续的操作。

AIO 是异步 IO 的缩写，虽然 NIO 在网络操作中，提供了非阻塞的方法，但是 NIO 的 IO 行为还是同步的。对于 NIO 来说，我们的业务线程是在 IO 操作准备好时，得到通知，接着就由这个线程自行进行 IO 操作，IO 操作本身是同步的。查阅网上相关资料，我发现就目前来说 AIO 的应用还不是很广泛，Netty 之前也尝试使用过 AIO，不过又放弃了。
