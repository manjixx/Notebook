# 五、单一职责模式

在软件组件的设计中，**如果责任划分的不清晰**，使用继承得到的结果往往是随着需求的变化，子类急剧膨胀，同时充斥着重复代码，这时候的关键是划清责任。

典型模式：责任的问题上表现的极其突出特征非常明显

- Decorator
- Bridge
  
## 5.1 Decorator 装饰模式

### 5.1.1 动机（Motivation）

在某些情况下我们可能会 **“过度地使用继承来扩展对象的功能”**，由于继承为类型引入的静态特质，使得这种扩展方式缺乏灵活性；并且随着子类的增多（扩展功能的增多），各种子类的组合（扩展功能的组合）会导致更多子类的膨胀。

如何使“对象功能的扩展”能够根据需要来动态地实现？同时避免“扩展功能的增多”带来的子类膨胀问题？从而使得任何“功能扩展变化”所导致的影响将为最低？

### 5.1.2 模式定义

> 动态（组合）地给一个对象增加一些额外的职责。就增加功能而言，Decorator模式比生成子类（继承）更为灵活（消除重复代码 & 减少子类个数）。​ ——《设计模式》GoF

### 5.1.3 代码示例

> **初始代码**

```c++
//decorator1.cpp
//业务操作
class Stream{
public：
    virtual char Read(int number)=0;
    virtual void Seek(int position)=0;
    virtual void Write(char data)=0;
    
    virtual ~Stream(){}
};

//主体类
class FileStream: public Stream{
public:
    virtual char Read(int number){
        //读文件流
    }
    virtual void Seek(int position){
        //定位文件流
    }
    virtual void Write(char data){
        //写文件流
    }

};

class NetworkStream :public Stream{
public:
    virtual char Read(int number){
        //读网络流
    }
    virtual void Seek(int position){
        //定位网络流
    }
    virtual void Write(char data){
        //写网络流
    }
    
};

class MemoryStream :public Stream{
public:
    virtual char Read(int number){
        //读内存流
    }
    virtual void Seek(int position){
        //定位内存流
    }
    virtual void Write(char data){
        //写内存流
    }
    
};

//扩展操作
class CryptoFileStream :public FileStream{
public:
    virtual char Read(int number){
        //额外的加密操作...
        FileStream::Read(number);//读文件流  静态特质，确定了只能调FileStream
        
    }
    virtual void Seek(int position){
        //额外的加密操作...
        FileStream::Seek(position);//定位文件流
        //额外的加密操作...
    }
    virtual void Write(byte data){
        //额外的加密操作...
        FileStream::Write(data);//写文件流
        //额外的加密操作...
    }
};

class CryptoNetworkStream : :public NetworkStream{
public:
    virtual char Read(int number){
        
        //额外的加密操作...
        NetworkStream::Read(number);//读网络流 静态特质，确定了只能调NetworkStream
    }
    virtual void Seek(int position){
        //额外的加密操作...
        NetworkStream::Seek(position);//定位网络流
        //额外的加密操作...
    }
    virtual void Write(byte data){
        //额外的加密操作...
        NetworkStream::Write(data);//写网络流
        //额外的加密操作...
    }
};

class CryptoMemoryStream : public MemoryStream{
public:
    virtual char Read(int number){
        
        //额外的加密操作...
        MemoryStream::Read(number);//读内存流
    }
    virtual void Seek(int position){
        //额外的加密操作...
        MemoryStream::Seek(position);//定位内存流
        //额外的加密操作...
    }
    virtual void Write(byte data){
        //额外的加密操作...
        MemoryStream::Write(data);//写内存流
        //额外的加密操作...
    }
};

class BufferedFileStream : public FileStream{
    //...
};

class BufferedNetworkStream : public NetworkStream{
    //...
};

class BufferedMemoryStream : public MemoryStream{
    //...
}


class CryptoBufferedFileStream :public FileStream{
public:
    virtual char Read(int number){
        
        //额外的加密操作...
        //额外的缓冲操作...
        FileStream::Read(number);//读文件流
    }
    virtual void Seek(int position){
        //额外的加密操作...
        //额外的缓冲操作...
        FileStream::Seek(position);//定位文件流
        //额外的加密操作...
        //额外的缓冲操作...
    }
    virtual void Write(byte data){
        //额外的加密操作...
        //额外的缓冲操作...
        FileStream::Write(data);//写文件流
        //额外的加密操作...
        //额外的缓冲操作...
    }
};


void Process(){
    //编译时装配
    CryptoFileStream *fs1 = new CryptoFileStream();
    BufferedFileStream *fs2 = new BufferedFileStream();
    CryptoBufferedFileStream *fs3 =new CryptoBufferedFileStream();
}
```

涉及到的结构：

![](https://img-blog.csdnimg.cn/img_convert/cdcc2f1ca38c45e53b45f9e874b18fd8.png)

类的规模为：${1 + n + n × m ! / 2 }$

这份代码存在冗余，加密操作都是相同的，代码大量的重复。

> **重构**

```c++
//decorator2.cpp
//业务操作
class Stream{

public：
    virtual char Read(int number)=0;
    virtual void Seek(int position)=0;
    virtual void Write(char data)=0;
    
    virtual ~Stream(){}
};

//主体类
class FileStream: public Stream{
public:
    virtual char Read(int number){
        //读文件流
    }
    virtual void Seek(int position){
        //定位文件流
    }
    virtual void Write(char data){
        //写文件流
    }

};

class NetworkStream :public Stream{
public:
    virtual char Read(int number){
        //读网络流
    }
    virtual void Seek(int position){
        //定位网络流
    }
    virtual void Write(char data){
        //写网络流
    }
    
};

class MemoryStream :public Stream{
public:
    virtual char Read(int number){
        //读内存流
    }
    virtual void Seek(int position){
        //定位内存流
    }
    virtual void Write(char data){
        //写内存流
    }
    
};

//扩展操作，继承自Stream，是为了符合虚函数的接口规范

class CryptoStream: public Stream {
    
    Stream* stream;//...new FileStream() / new NetworkStream() /...

public:
    CryptoStream(Stream* stm) : stream(stm){
    
    }
    
    virtual char Read(int number){
       
        //额外的加密操作...
        stream->Read(number);//读文件流   动态特质，在运行时确定stream的具体类型
    }
    virtual void Seek(int position){
        //额外的加密操作...
        stream::Seek(position);//定位文件流
        //额外的加密操作...
    }
    virtual void Write(byte data){
        //额外的加密操作...
        stream::Write(data);//写文件流
        //额外的加密操作...
    }
};


class BufferedStream : public Stream{
    
    Stream* stream;//...
    
public:
    BufferedStream(Stream* stm) : stream(stm){
        
    }
    //...
};


void Process(){
    //运行时通过组合的方式装配
    FileStream* s1=new FileStream();
    CryptoStream* s2=new CryptoStream(s1); 
    BufferedStream* s3=new BufferedStream(s1);
    BufferedStream* s4=new BufferedStream(s2);
}
```

修改后的优点：将“继承”改成“对象组合"，使用多态，在运行时确定具体类型，“编译时装配"变成了"运行时装配”。

> **将相同字段提到一个新的基类DecoratorStream 中**：

```c++
//decorator3.cpp
//业务操作
class Stream{
public：
    virtual char Read(int number)=0;
    virtual void Seek(int position)=0;
    virtual void Write(char data)=0;
    
    virtual ~Stream(){}
};

//主体类
class FileStream: public Stream{
public:
    virtual char Read(int number){
        //读文件流
    }
    virtual void Seek(int position){
        //定位文件流
    }
    virtual void Write(char data){
        //写文件流
    }

};

class NetworkStream :public Stream{
public:
    virtual char Read(int number){
        //读网络流
    }
    virtual void Seek(int position){
        //定位网络流
    }
    virtual void Write(char data){
        //写网络流
    }
    
};

class MemoryStream :public Stream{
public:
    virtual char Read(int number){
        //读内存流
    }
    virtual void Seek(int position){
        //定位内存流
    }
    virtual void Write(char data){
        //写内存流
    }
    
};

//扩展操作
class DecoratorStream: public Stream{
protected:
    Stream* stream;//...
    
    DecoratorStream(Stream* stm) : stream(stm){
    
    }
};

class CryptoStream: public DecoratorStream {
public:
    CryptoStream(Stream* stm): DecoratorStream(stm) {
    
    }

    virtual char Read(int number){
       
        //额外的加密操作...
        stream->Read(number);//读文件流
    }
    
    virtual void Seek(int position){
        //额外的加密操作...
        stream::Seek(position);//定位文件流
        //额外的加密操作...
    }
    
    virtual void Write(byte data){
        //额外的加密操作...
        stream::Write(data);//写文件流
        //额外的加密操作...
    }
};


class BufferedStream : public DecoratorStream{
public:
    BufferedStream(Stream* stm):DecoratorStream(stm){
        
    }
    //...
};


void Process(){
    //运行时装配
    FileStream* s1=new FileStream();
    
    CryptoStream* s2=new CryptoStream(s1);
    
    BufferedStream* s3=new BufferedStream(s1);
    
    BufferedStream* s4=new BufferedStream(s2);
}
```

此时类关系：

![](https://img-blog.csdnimg.cn/img_convert/2ce9566ab12e8b777a6f14c2b83bdaca.png)

类的规模：1 + n + 1 + m

### 5.1.4 结构（Structure)

![](https://img-blog.csdnimg.cn/img_convert/dbc33bdd17ae4eb24c3a2d9a2a91bc59.png)

- Component -> Stream (稳定)
- Decorator -> DecoratorStream （稳定）
- ConcreteComponent -> FileStream/NetworkStream/… （变化）
- ConcreteDecoratorX-> CryptoStream / BufferedStream (变化)

### 5.1.5 要点总结

- 通过采用组合而非继承的手法，Decorator模式实现了在**运行时动态扩展对象功能的能力**，而且可以根据需要扩展多个功能。避免了使用继承带来的“灵活性差”和“多子类衍生问题”。
- Decorator类在接口上表现为**is-a** Component的继承关系，即Decorator类继承了Component类所具有的接口。但在实现上又表现为**has-a** Component的组合关系，即Decorator类又使用了另外一个Component类。【注：DecoratorStream 类继承自 Stream，同时又有一个Stream类型的字段，一般这种**既继承又组合的方式**通常都是装饰模式。例子中的继承是为了完善接口的规范，组合是为了支持实现具体的类】
- Decorator模式的目的并非解决“多子类衍生的多继承”问题，Decorator模式**应用的要点**在于解决“主体类在多个方向上的扩展功能”——是为“装饰”的含义。

## 5.2 Bridge 桥模式

### 5.2.1 动机（Motivation）

由于某些类型的固有的实现逻辑，使得它们具有两个变化的维度，乃至多个纬度的变化。

如何应对这种“多维度的变化”？如何利用面向对象技术来使得类型可以轻松地沿着两个乃至多个方向变化，而不引入额外的复杂度？

### 5.2.2 代码示例

> **原始代码**

```c++
//bridge1.cpp
class Messager{
public:
    virtual void Login(string username, string password)=0;
    virtual void SendMessage(string message)=0;
    virtual void SendPicture(Image image)=0;

    virtual void PlaySound()=0;
    virtual void DrawShape()=0;
    virtual void WriteText()=0;
    virtual void Connect()=0;
    
    virtual ~Messager(){}
};


//平台实现 n
//类的数目：1 + n + m * n
class PCMessagerBase : public Messager{
public:
    virtual void PlaySound(){
        //**********
    }
    
    virtual void DrawShape(){
        //**********
    }
    
    virtual void WriteText(){
        //**********
    }
    
    virtual void Connect(){
        //**********
    }
};

class MobileMessagerBase : public Messager{
public:
    virtual void PlaySound(){
        //==========
    }
    
    virtual void DrawShape(){
        //==========
    }
    
    virtual void WriteText(){
        //==========
    }
    
    virtual void Connect(){
        //==========
    }
};

 
//业务抽象 m
class PCMessagerLite : public PCMessagerBase {
public:
    virtual void Login(string username, string password){
        
        PCMessagerBase::Connect();
        //........
    }
    virtual void SendMessage(string message){
        
        PCMessagerBase::WriteText();
        //........
    }
    virtual void SendPicture(Image image){
        
        PCMessagerBase::DrawShape();
        //........
    }
};


class PCMessagerPerfect : public PCMessagerBase {
public:
    
    virtual void Login(string username, string password){
        
        PCMessagerBase::PlaySound();
        //********
        PCMessagerBase::Connect();
        //........
    }
    virtual void SendMessage(string message){
        
        PCMessagerBase::PlaySound();
        //********
        PCMessagerBase::WriteText();
        //........
    }
    virtual void SendPicture(Image image){
        
        PCMessagerBase::PlaySound();
        //********
        PCMessagerBase::DrawShape();
        //........
    }
};


class MobileMessagerLite : public MobileMessagerBase {
public:
    
    virtual void Login(string username, string password){
        
        MobileMessagerBase::Connect();
        //........
    }
    
    virtual void SendMessage(string message){
        
        MobileMessagerBase::WriteText();
        //........
    }
    
    virtual void SendPicture(Image image){
        
        MobileMessagerBase::DrawShape();
        //........
    }
};


class MobileMessagerPerfect : public MobileMessagerBase {
public:
    
    virtual void Login(string username, string password){
        
        MobileMessagerBase::PlaySound();
        //********
        MobileMessagerBase::Connect();
        //........
    }
    virtual void SendMessage(string message){
        
        MobileMessagerBase::PlaySound();
        //********
        MobileMessagerBase::WriteText();
        //........
    }
    virtual void SendPicture(Image image){
        
        MobileMessagerBase::PlaySound();
        //********
        MobileMessagerBase::DrawShape();
        //........
    }
};

void Process(){
    //编译时装配
    Messager *m = new MobileMessagerPerfect();
}
```

> **基于装饰模式的经验，将业务的继承修改为组合，进行如下的修改：**

```c++
class Messager{
public:
    //存在着多个变化的维度：平台实现 + 业务抽象
    virtual void Login(string username, string password)=0;
    virtual void SendMessage(string message)=0;
    virtual void SendPicture(Image image)=0;

    virtual void PlaySound()=0;
    virtual void DrawShape()=0;
    virtual void WriteText()=0;
    virtual void Connect()=0;
    
    virtual ~Messager(){}
};

//平台实现 n
//类的数目：1 + n + m * n
//主要到这个类里只实现了Messager这个类的部分接口
class PCMessagerBase : public Messager{
public:
    virtual void PlaySound(){
        //**********
    }
    
    virtual void DrawShape(){
        //**********
    }
    
    virtual void WriteText(){
        //**********
    }
    
    virtual void Connect(){
        //**********
    }
};

class MobileMessagerBase : public Messager{
public:
    virtual void PlaySound(){
        //==========
    }
    
    virtual void DrawShape(){
        //==========
    }
    
    virtual void WriteText(){
        //==========
    }
    
    virtual void Connect(){
        //==========
    }
};


//业务抽象 
//主要到这个类里只需要实现了Messager这个类的部分接口，如果继承Messager是不合适的
class MessagerLite {
    Messager* messager; //指针才具有多态性
public:
    virtual void Login(string username, string password){
        
        messager->Connect();
        //........
    }
    virtual void SendMessage(string message){
        
        messager->WriteText();
        //........
    }
    virtual void SendPicture(Image image){
        
        messager->DrawShape();
        //........
    }
};


class MessagerPerfect {
    Messager* messager;
public:
    
    virtual void Login(string username, string password){
        messager->PlaySound();
        //********
        messager->Connect();
        //........
    }
    
    virtual void SendMessage(string message){
        
        messager->PlaySound();
        //********
        messager->WriteText();
        //........
    }
    
    virtual void SendPicture(Image image){
        
        messager->PlaySound();
        //********
        messager->DrawShape();
        //........
    }
};

void Process(){
    //编译时装配
    Messager *m = new MobileMessagerPerfect();
}
```

> **因为PCMessageBase类和MessagerLite、MessagerPerfect类都各自只实现了Messager的部分接口，说明Messager中的两部分的接口不应该放到一起，应该进行拆分：**

```c++
//bridge2.cpp
class Messager{
protected:
     MessagerImp* messagerImp;//...
public:
    Messager(MessagerImpl* mimp) : messagerImpl(mimp) { }
    virtual void Login(string username, string password)=0;
    virtual void SendMessage(string message)=0;
    virtual void SendPicture(Image image)=0;
    
    virtual ~Messager(){}
};

class MessagerImp{
public:
    virtual void PlaySound()=0;
    virtual void DrawShape()=0;
    virtual void WriteText()=0;
    virtual void Connect()=0;
    
    virtual ~MessagerImp(){}
};


//平台实现 n
class PCMessagerImp : public MessagerImp{
public:
    
    virtual void PlaySound(){
        //**********
    }
    virtual void DrawShape(){
        //**********
    }
    virtual void WriteText(){
        //**********
    }
    virtual void Connect(){
        //**********
    }
};

class MobileMessagerImp : public MessagerImp{
public:
    
    virtual void PlaySound(){
        //==========
    }
    virtual void DrawShape(){
        //==========
    }
    virtual void WriteText(){
        //==========
    }
    virtual void Connect(){
        //==========
    }
};

//业务抽象 m
//类的数目：1+n+m
class MessagerLite : public Messager {
public:
    MessagerLite(MessagerImp* mimp) : Messager(mimp) { 
        
    }
    virtual void Login(string username, string password){
        
        messagerImp->Connect(); //messagerImpl字段在父类中声明了
        //........
    }
    virtual void SendMessage(string message){
        
        messagerImp->WriteText();
        //........
    }
    virtual void SendPicture(Image image){
        
        messagerImp->DrawShape();
        //........
    }
};


class MessagerPerfect  :public Messager {
public: 
    MessagerPerfect(MessagerImp* mimp) : Messager(mimp) { 
        
    }
    virtual void Login(string username, string password){
        
        messagerImp->PlaySound();
        //********
        messagerImp->Connect();
        //........
    }
    virtual void SendMessage(string message){
        
        messagerImp->PlaySound();
        //********
        messagerImp->WriteText();
        //........
    }
    virtual void SendPicture(Image image){
        
        messagerImp->PlaySound();
        //********
        messagerImp->DrawShape();
        //........
    }
};

void Process(){
    //运行时装配
    MessagerImp* mImp = new PCMessagerImp();
    Messager *m = new Messager(mImp);
}
```

### 5.2.3 模式定义

> 将抽象部分(**业务功能**)与实现部分(**平台实现**)分离，使它们都**可以独立地变化**。——《设计模式》GoF

### 5.2.4 结构（Structure）

![](https://img-blog.csdnimg.cn/img_convert/41cbdd2904d6ea9ef6725bf75204add7.png)

- Abstraction -> Messgaer (稳定) 【imp对应到代码中就是 Messager 中有一个MessagerImpl类型的指针变量】

- Implementor -> MessagerImpl （稳定）

- RefinedAbstraction -> MessagerLite / MessagerPerfect (变化)

- ConcreteImplementorX -> XXMessagerImpl (变化)

两个方向独立变化，而不是杂糅在一起。

### 5.2.5 要点总结

- Bridge模式使用“**对象间的组合关系**”解耦了抽象和实现之间固有的绑定关系，使得抽象和实现可以沿着各自的维度来变化。所谓抽象和实现沿着各自纬度的变化，即“子类化”它们。
  
- Bridge模式**有时候类似于多继承方案**，但是多继承方案往往违背**单一职责原则**（即一个类只有一个变化的原因），复用性比较差。Bridge模式是比多继承方案更好的解决方法。
  
- Bridge模式的应用一般在 **“两个非常强的变化维度”**，有时一个类也有多于两个的变化维度，这时可以使用Bridge的扩展模式。
