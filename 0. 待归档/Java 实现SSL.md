# JSSE 

## 一、JSSE 实现 SSL/TLS 安全协议

### 一、简介

SSL/TLS协议是安全的通信模式，对于底层协议如果需要每个开发者自己实现，显然会带来不必要的麻烦。为了解决该问题，Java 为广大开发者提供了 Java 安全套接字扩展——JSSE。

在用 JSSE 实现SSL通信过程中主要会遇到以下类和接口，由于过程中涉及到加解密、密钥生成等运算的框架和实现，所以也会间接用到 JCE 包的一些类。如图为JSSE接口的主要类图：

![](https://docs.oracle.com/javase/8/docs/technotes/guides/security/jsse/images/jsse-classes-and-interfaces.png)

- **通信核心类 —— SSLSocket 和 SSLServerSocket**，对应的就是 Socket 与 ServerSocket，只是表示实现了 SSL 协议的 Socket，ServerSocket，同时它们也是Socket与ServerSocket的子类。SSLSocket主要负责**设置加密套件、管理SSL会话、处理握手结束时间、设置客户端模式或服务器模式**。
- **客户端与服务器端Socket工厂——SSLSocketFactory 和 SSLServerSocketFactory**，在设计模式中工厂模式是专门用于生产出需要的实例，这里也是把SSLSocket、SSLServerSocket对象创建的工作交给这两个工厂类。
- **SSL 会话——SSLSession**，安全通信握手过程需要一个会话，为了提高通信的效率，SSL 协议允许多个 SSLSocket 共享同一个 SSL 会话，在同一个会话中，只有第一个打开的SSLSocket 需要进行 SSL 握手，负责生成密钥及交换密钥，其余 SSLSocket 都共享密钥信息。
- **SSL 上下文——SSLContext**，它是对整个 SSL/TLS 协议的封装，表示了安全套接字协议的实现。主要负责设置安全通信过程中的各种信息，例如跟证书相关的信息。并且负责构建SSLSocketFactory、SSLServerSocketFactory 和 SSLEngine 等工厂类。
- **SSL 非阻塞引擎——SSLEngine**，假如要进行 NIO 通信，那么将使用这个类，它让通过过程支持非阻塞的安全通信。
- **密钥管理器——KeyManager**，此接口负责选择用于证实自己身份的安全证书，发给通信另一方。KeyManager 对象由 KeyManagerFactory 工厂类生成。
- **信任管理器——TrustManager**，此接口负责判断决定是否信任对方的安全证书，TrustManager对象由TrustManagerFactory工厂类生成。
- **密钥证书存储设施——KeyStore**，这个对象用于存放安全证书，安全证书一般以文件形式存放，KeyStore 负责将证书加载到内存。

通过上述类即可实现 SSL 协议的安全通信，注意使用 SSL/TLS 进行安全通信时，客户端和服务器端必须要支持 SSL/TLS 协议，否则无法进行通信。而且客户端和服务器端都可能要设置用于**证实自己身份的安全证书，并且还要设置信任对方的哪些安全证书**。

身份认证：

- 客户端模式，一般情况客户端要对服务器端的身份进行验证，但是无需向服务器证实自己的身份，这样不用向对方证实自己身份的通信端我们就说它处于客户模式，否则称它处于服务器模式。
- `SSLSocket的setUseClientMode(Boolean mode)`方法可以设置客户端模式或服务器模式。

### 二、证书简介

#### 2.1 证书来源

一般而言作为服务器端必须要有证书以证明这个服务器的身份，并且证书应该描述此服务器所有者的一些基本信息，例如公司名称、联系人名等。证书由所有人以密码形式签名，基本不可伪造，证书获取的途径有两个：

- 一是从权威机构购买证书，权威机构担保它发出的证书的真实性，而且这个权威机构被大家所信任，进而你可以相信这个证书的有效性；
- 自己用JDK提供的工具keytool创建一个自我签名的证书，这种情况下一般是我只想要保证数据的安全性与完整性，避免数据在传送的过程中被窃听或篡改，此时身份的认证已不重要，重点已经在端与端传输的秘密性上，证书的作用只体现在加解密签名。
  
另外，关于证书的一些概念在这里陈述，一个证书是一个实体的数字签名，这个实体可以是一个人、一个组织、一个程序、一个公司、一个银行，同时证书还包含这个实体的公共钥匙，此公共钥匙是这个实体的数字关联，让所有想同这个实体发生信任关系的其他实体用来检验签名。而这个实体的数字签名是实体信息用实体的私钥加密后的数据，这条数据可以用这个实体的公共钥匙解密，进而鉴别实体的身份。这里用到的核心算法是非对称加密算法。

#### 2.2 证书格式

SSL协议通信涉及密钥储存的文件格式比较多，很容易搞混，例如`xxx.cer、xxx.pfx、xxx.jks、xxx.keystore、xxx.truststore`等格式文件。如下图所示：

![](https://p1-jj.byteimg.com/tos-cn-i-t2oaga2asx/leancloud-assets/86dee010cbfa3f10b0fe~tplv-t2oaga2asx-jj-mark:3024:0:0:0:q75.png)

- `.cer`格式文件俗称证书，但这个证书中没有私钥，只包含了公钥；
- `.pfx`格式文件也称为证书，它一般供浏览器使用，而且它不仅包含了公钥，还包含了私钥，当然这个私钥是加密的，不输入密码是解不了密的；
- `.jks`格式文件表示 java 密钥存储器（javakey store），它可以同时容纳N个公钥跟私钥，是一个密钥库；
- `.keystore`格式文件其实跟`.jks`基本是一样的，只是不同公司叫法不太一样，默认生成的证书存储库格式；
- `.truststore`格式文件表示信任证书存储库，它仅仅包含了通信对方的公钥，当然你可以直接把通信对方的`jks`作为信任库（就算如此你也只能知道通信对方的公钥，要知道密钥都是加密的，你无从获取，只要算法不被破解）

### 三、生成证书

按照理论上，一共需要准备四个文件，两个`keystore`文件和两个`truststore`文件，通信双方分别拥有一个`keystore`和一个`truststore`：

- `keystore`用于存放自己的密钥和公钥;
- `truststore`用于存放所有需要信任方的公钥。

这里为了方便直接使用`jks`(即`keystore`)替代 `truststore`（免去证书导来导去），因为对方的 `keystore` 包含了自己需要的信任公钥。

本例中使用`jdk`自带的工具分别生成服务器端证书，通过如下命令并输入姓名、组织单位名称、组织名称、城市、省份、国家信息即可生成证书密码为 `myserver` 的证书，此证书存放在密码也为`123456`的`myserver.jks`证书存储库中。

如果继续创建证书将继续往`myserver.jks`证书存储库中添加证书。

**keytool 用法:**

```bash
# 1.生成
keytool -genkey -alias yushan(别名) -keypass yushan(别名密码) -keyalg RSA(算法) -keysize 1024(密钥长度) -validity 365(有效期，天单位) -keystore e:\yushan.keystore(指定生成证书的位置和证书名称) -storepass 123456(获取keystore信息的密码)；

# 2. 证书库导出到 crt 证书文件
keytool -export -alias yushan -keystore e:\yushan.keystore -file e:\yushan.crt(指定导出的证书位置及证书名称) -storepass 123456

# 3. 导入（从证书文件导入到keystore或jks文件）

# 准备一个导入的证书：
keytool -genkey -alias shuany -keypass shuany -keyalg RSA -keysize 1024 -validity 365 -keystore  e:\shuany.keystore -storepass 123456 -dname "CN=shuany, OU=xx, O=xx, L=xx, ST=xx, C=xx";
keytool -export -alias shuany -keystore e:\shuany.keystore -file e:\shuany.crt -storepass 123456
 
# 将shuany.crt 加入到yushan.keystore中

keytool -import -alias shuany(指定导入证书的别名，如果不指定默认为mykey,别名唯一，否则导入出错) -file e:\shuany.crt -keystore e:\yushan.keystore -storepass 123456 keytool -list  -v -keystore e:\keytool\yushan.keystore -storepass 123456
```

## 四、实现SSL

### 4.1 服务端简单实现

```java
public static void main(String[] args) throws Exception {
 
    //密钥管理器
    KeyStore serverKeyStore = KeyStore.getInstance("JKS");  //证书库格式
    serverKeyStore.load(new FileInputStream("e:\\myserver.jks"), "123456".toCharArray());   //加载密钥库

    KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");   //证书格式
    kmf.init(serverKeyStore, "123456".toCharArray());   //加载密钥储存器

    //信任管理器
    KeyStore clientKeyStore = KeyStore.getInstance("JKS");
    clientKeyStore.load(new FileInputStream("e:\\myclient.jks"), "123456".toCharArray());

    TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
    tmf.init(clientKeyStore);

    //SSL上下文设置
    SSLContext sslContext = SSLContext.getInstance("SSL");
    sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

    //SSLServerSocket
    SSLServerSocketFactory serverFactory = sslContext.getServerSocketFactory();
    SSLServerSocket svrSocket = (SSLServerSocket) serverFactory.createServerSocket(34567);
    //svrSocket.setNeedClientAuth(true);//客户端模式，服务端需要验证客户端身份

    String[] supported = svrSocket.getEnabledCipherSuites();//加密套件
    svrSocket.setEnabledCipherSuites(supported);

    //接收消息
    System.out.println("端口已打开，准备接受信息");

    SSLSocket cntSocket = (SSLSocket) svrSocket.accept();//开始接收
    InputStream in=cntSocket.getInputStream();//输入流
    int a=in.read(new byte[102]);
    //循环检查是否有消息到达
    System.out.println("来自于客户端:" + a);
}
```

实现顺序：

- 先得到一个 `SSLContext`实例，对`SSLContext`实例进行初始化
- 密钥管理器及信任管理器作为参数传入
- 证书管理器及信任管理器按照指定的密钥存储器路径和密码进行加载
- 设置支持的加密套件
- 最后让 SSLServerSocket 开始监听客户端发送过来的消息。

注意服务器端有行代码`svrSocket.setNeedClientAuth(true);`它是非常重要的一个设置方法，用于设置是否验证客户端的身份。
假如将其它注释掉或设置为`false`，此时客户端将不再需要自己的密钥管理器，即服务器不需要通过`client.jks`对客户端的身份进行验证，把密钥管理器直接设置为null也可以跟服务器端进行通信。

### 4.2 客户端实现

```java
public static void main(String[] args) throws Exception {
 
        //密钥管理器
        KeyStore clientKeyStore = KeyStore.getInstance("JKS");
        clientKeyStore.load(new FileInputStream("e:\\myclient.jks"), "123456".toCharArray());
 
        KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
        kmf.init(clientKeyStore, "123456".toCharArray());
 
 
        //信任管理器
        KeyStore serverKeyStore = KeyStore.getInstance("JKS");
        serverKeyStore.load(new FileInputStream("e:\\myserver.jks"), "123456".toCharArray());
 
 
        TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
        tmf.init(serverKeyStore);
 
        //SSL上下文
        SSLContext sslContext = SSLContext.getInstance("SSL");
        sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
 
 
        SSLSocketFactory sslcntFactory =(SSLSocketFactory) sslContext.getSocketFactory();
        SSLSocket sslSocket= (SSLSocket) sslcntFactory.createSocket("127.0.0.1", 34567);
 
        String[] supported = sslSocket.getSupportedCipherSuites();
        sslSocket.setEnabledCipherSuites(supported);
 
        //发送
        OutputStream out=sslSocket.getOutputStream();
        out.write("hello".getBytes());
 
    }
```

客户端的前面操作基本跟服务器端的一样，先创建一个SSLContext实例，再用密钥管理器及信任管理器对SSLContext进行初始化，当然这里密钥存储的路径是指向客户端的client.jks。接着设置加密套件，最后使用SSLSocket进行通信。

### 4.3 信任管理器

最后谈谈信任管理器，它的职责是觉得是否信任远端的证书，那么它凭借什么去判断呢？如果不显式设置信任存储器的文件路径，将遵循如下规则：

- 如果系统属性`javax.net.ssl.truststore`指定了`truststore`文件，那么信任管理器将去`jre`路径下的`lib/security`目录寻找这个文件作为信任存储器；

- 如果没设置 1 中的系统属性，则去寻找一个`%java_home%/lib/security/jssecacerts`文件作为信任存储器；

- 如果`jssecacerts`不存在而`cacerts`存在，则`cacerts`作为信任存储器。


## 站在巨人的肩上

[Java SSL实现使用详解](https://blog.csdn.net/a82514921/article/details/104590197)