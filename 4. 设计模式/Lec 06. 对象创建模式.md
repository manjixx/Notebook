# 六、对象创建模式

## 6.1 概述

通过“对象创建”模式**绕开new**，来**避免**对象创建（new）过程中所导致的**紧耦合**（依赖具体类），从而支持对象创建的稳定。它是接口抽象之后的第一步工作。

典型模式

- Factory Method
- Abstract Factory
- Prototype
- Builder

## 6.2 Factory Method 工厂方法

### 6.2.1 动机（Motivation）

在软件系统中，经常面临着创建对象的工作；由于需求的变化，需要**创建的对象的具体类型经常变化**。

如何应对这种变化？如何绕过常规的对象创建方法(new)，提供一种“封装机制”来避免客户程序和这种“具体对象创建工作”的紧耦合？

### 6.2.2 代码示例

```c++
class BinarySplitter 
{
public:
    void split() {
        //...
    }
};
```

```c++
//MainForm.cpp
class MainForm : public Form
{
    TextBox* txtFilePath;
    TextBox* txtFileNumber;
    ProgressBar* progressBar;

public:
    void Button1_Click(){
        string filePath = txtFilePath->getText();
        int number = atoi(txtFileNumber->getText().c_str());
        FileSplitter splitter(filePath, number, progressBar);
        splitter.split();
    }
};
```

未来可能的需求：文本分割，图片分割，那就要新增：

```c++
class ISplitter {
public:
    virtual void split() = 0;
    virtual ~ISplitter() { }
}

class BinarySplitter : public ISplitter
{
    virtual void split() {
        //...
    }
};

//新增
class TxtSplitter : public ISplitter
{
    virtual void split() {
        //...
    }
};

class PictureSplitter : public ISplitter
{
    virtual void split() {
        //...
    }
};

class VideoSplitter : public ISplitter
{
    virtual void split() {
        //...
    }
};
```

**面向接口编程最简单的表现就是变量要申明为接口基类**，

```c++
//MainForm1.cpp
class MainForm : public Form
{
    TextBox* txtFilePath;
    TextBox* txtFileNumber;

public:
    void Button1_Click(){
        string filePath = txtFilePath->getText();
        int number = atoi(txtFileNumber->getText().c_str());
        // 违背了依赖倒置原则，应该去依赖抽象，只要代码中有细节依赖存在就违背依赖倒置原则，即编译时仍然需要细节存在时才能编译，如何解决呢？
        //ISplitter* splitter= 是抽象依赖
        //new BinarySplitter(filePath, number) 是细节依赖
        ISplitter* splitter = new BinarySplitter(filePath, number); //依赖具体类
        splitter.split();
    }
};
```

”对象创建“ 模式就是要绕开这个new 带来的问题，这是面向接口编程必然要面临的需求，上述代码中`ISplitter* splitter = new BinarySplitter(filePath, number);`等号左右两边都变成依赖抽象。可以考虑通过一个方法返回对象。

```c++
//SplitterFactory1.cpp
//抽象类
class ISplitter {
public:
    virtual void split() = 0;
    virtual ~ISplitter() { }
}

//工厂基类
class SplitterFactory {
public:
    ISplitter* createSplitter() {
        return new BinaryFiltter();
    }
};
```

```c++
//MainForm2.cpp
class MainForm : public Form
{
    TextBox* txtFilePath;
    TextBox* txtFileNumber;

public:
    void Button1_Click(){
        string filePath = txtFilePath->getText();
        int number = atoi(txtFileNumber->getText().c_str());
        SplitterFactory factory;
        ISplitter* splitter = factory.createSplitter(); 
        splitter.split();
    }
};
```

因为SplitterFactory编译时依赖了BinarySplitter，而MainForm编译时依赖了SplitterFactory，所以相当于MainForm编译时依赖了BinarySplitter，所以还是没有解决问题。那应该怎么办呢？

虚函数是运行时依赖，所以修改SplitterFactory.cpp:

```c++
//SplitterFactory.cpp
class SplitterFactory {
public:
    virtual ISplitter* createSplitter() = 0;
    virtual ~SplitterFactory() { }
};

class ISplitter {
public:
    virtual void split() = 0;
    virtual ~ISplitter() { }
}
```

```c++
//MainForm3.cpp
class MainForm : public Form
{
    TextBox* txtFilePath;
    TextBox* txtFileNumber;

public:
    void Button1_Click(){
        string filePath = txtFilePath->getText();
        int number = atoi(txtFileNumber->getText().c_str());
        
        SplitterFactory* factory;
        ISplitter* splitter = factory->createSplitter();  //多态
        
        splitter.split();
    }
};
```

未来的对象实际是什么类型依赖于factory，那么factory的实际类型是什么呢：

```c++
//FileSplitter2.cpp
//具体类
class BinarySplitter : public ISplitter
{
    virtual void split() {
        //...
    }
};

class TxtSplitter : public ISplitter
{
    virtual void split() {
        //...
    }
};

class PictureSplitter : public ISplitter
{
    virtual void split() {
        //...
    }
};

class VideoSplitter : public ISplitter
{
    virtual void split() {
        //...
    }
};

//具体工厂
class BinarySplitterFactory : public SplitterFactory {
public:
    virtual ISplitter* createSplitter() {
        return new BinarySplitter();
    }
};

class TxtSplitterFactory : public SplitterFactory {
public:
    virtual ISplitter* createSplitter() {
        return new TxtSplitter();
    }
};

class PictureSplitterFactory : public SplitterFactory {
public:
    virtual ISplitter* createSplitter() {
        return new PictureSplitter();
    }
};

class VideoSplitterFactory : public SplitterFactory {
public:
    virtual ISplitter* createSplitter() {
        return new VideoSplitter();
    }
};
```

```c++
//MainForm3.cpp
class MainForm : public Form
{
    SplitterFactory* factory; //工厂
public:
    MainForm(SplitterFactory* factory) {
        this->factory = factory;
    }
    
    void Button1_Click(){
        ISplitter* splitter = factory->createSplitter();  //多态new
        splitter.split();
    }
};
```

可以发现，通过这种改善，MainForm 只依赖 SplitterFactory 和 ISplitter 这两个抽象，而没有依赖具体类。不是消灭变化，而是将变化赶到一个局部的地方。

### 6.2.3 模式定义

>定义一个用于创建对象的接口，**让子类决定实例化哪一个类**。Factory Method使得一个**类的实例化延迟**（目的：解耦，手段：虚函数）到子类。——《设计模式》GoF

注："解耦"是解new和后面具体的类的耦合。

### 6.2.4 结构

![](https://img-blog.csdnimg.cn/img_convert/710fe7b612b2b87a332021f6ba33afd4.png)

- Product -> ISplitter (稳定)
- ConcreteProduct -> XXSplitter （变化）
- Creator -> SplitterFactory （稳定）
- ConcreteCreator -> XXSplitterFactory （变化）

### 6.2.5 要点总结

- Factory Method模式用于隔离类对象的使用者和具体类型之间的耦合关系。面对一个经常变化的具体类型，紧耦合关系(new)会导致软件的脆弱。
- Factory Method模式通过**面向对象【注：多态】的手法**，将所要创建的具体对象工作**延迟**到子类，从而实现一种**扩展**（而非更改）的策略，较好地解决了这种紧耦合关系。【注：“延迟” 对应到代码中就是 MainForm 类中，一开始只要有需求变化，就要修改对应的代码，而改善后MainForm中不会因为需求的变化而进行更改，只需要加子类和子类的工厂即可，然后将具体的类传给MainForm。】
- Factory Method模式解决“单个对象”的需求变化。缺点在于要求创建方法/参数相同。

***

## 6.3 Abstract Factory 抽象工厂

### 6.3.1 动机（Motivation）

在软件系统中，经常面临着 **“一系列相互依赖的对象”**的创建工作；同时，由于需求的变化，往往存在更多系列对象的创建工作。

如何应对这种变化？如何绕过常规的对象创建方法(new)，提供一种“封装机制”来避免客户程序和这种“多系列具体对象创建工作”的紧耦合？

### 6.3.2 代码示例

```c++
//EmployeeDAO1.cpp
class EmployeeDAO {
public:
    vector<EmployeeDO> GetEmployees() {
        SqlConnection* connection = new SqlConnection();
        connection->ConnectionString = "...";
        
        SqlCommand* command = new SqlCommand();
        command->CommandText = "...";
        command->SetConnection(connection);
        
        SqlDataReader* reader = command->ExecuteReader();
        while (reader->Read()) {
            
        }
    }
};
//缺点: 类与SqlServer绑定了
```

修改为面向接口编程，如果使用工厂方法：

```c++
//EmployeeDAO2.cpp
//数据库访问有关的基类
class IDBConnection {};
class IDBConnectionFactory {
public:
    virtual IDBConnection* createDBConnection() = 0;
};

class IDBCommand {};
class IDBCommandFactory {
public:
    virtual IDBCommand* createDBCommand() = 0;
};

class IDataReader {};
class IDataReaderFactory {
public:
    virtual IDataReader* createDataReader() = 0;
};

//支持SQL Server
class SqlConnection: public IDBConnection {};
class SqlConnectionFactory: public IDBConnectionFactory {};

class SqlCommand: public IDBCommand {};
class SqlCommandFactory: public IDBCommandFactory {};

class SqlDataReader: public IDataReader {};    
class SqlDataReaderFactory: public IDataReaderFactory {};

//支持 Oracle
class OracleConnection: public IDBConnection {};
class OracleConnectionFactory: public IDBConnectionFactory {};

class OracleCommand: public IDBCommand {};
class OracleCommandFactory: public IDBCommandFactory {};

class OracleDataReader: public IDataReader {};   
class OracleDataReadeFactory: public IDataReaderFactory {};

class EmployeeDAO { 
    //在构造器中初始化 这三个必须是一个系列的，如果是sql的就是sql系列的
    IDBConnectionFactory* dbConnectionFactory;
    IDBCommandFactory* dbCommandFactory;
    IDataReaderFactory* dataReaderFactory;
public:
    vector<EmployeeDO> GetEmployees() {
        IDBConnection* connection = dbConnectionFactory->createDBConnection();
        connection->ConnectionString("...");
        
        IDBCommand* command = dbCommandFactory->createDBCommand();
        command->CommandText("...");
        command->SetConnection(connection); //关联性
        
        IDataReader* reader = command->ExecuteReader();
        while (reader->Read()) {
            
        }
    }
};
```

三个工厂指针变量必须是一个系列的，因为 command 和 connection 是有关联性的。如果传了一个 Sql 的 connection，而传了一个 Oracle 的 Command 就乱套了。所以这时候，使用抽象工厂：

```c++
//EmployeeDAO3.cpp
//数据库访问有关的基类
class IDBConnection {};
class IDBCommand {};
class IDataReader {};

class IDBFactory {
public:
    //因为三个有相关性，所以考虑把它们放到一个工厂里
    virtual IDBConnection* createDBConnection() = 0;
    virtual IDBCommand* createDBCommand() = 0;
    virtual IDataReader* createDataReader() = 0;
};

//支持SQL Server
class SqlConnection: public IDBConnection {};
class SqlCommand: public IDBCommand {};
class SqlDataReader: public IDataReader {};    

class SqlDBFactory: public IDBFactory {
    virtual IDBConnection* createDBConnection() {}
    virtual IDBCommand* createDBCommand() {}
    virtual IDataReader* createDataReader() {}
};

//支持 Oracle
class OracleConnection: public IDBConnection {};
class OracleCommand: public IDBCommand {};
class OracleDataReader: public IDataReader {};   

class OracleDBFactory: public IDBFactory {
    virtual IDBConnection* createDBConnection() {}
    virtual IDBCommand* createDBCommand() {}
    virtual IDataReader* createDataReader() {}
};

class EmployeeDAO { 
    IDBFactory* dbFactory;
public:
    vector<EmployeeDO> GetEmployees() {
        IDBConnection* connection = dbFactory->createDBConnection();
        connection->ConnectionString("...");
        
        IDBCommand* command = dbFactory->createDBCommand();
        command->CommandText("...");
        command->SetConnection(connection); //关联性
        
        IDataReader* reader = command->ExecuteReader(); //关联性
        while (reader->Read()) {
            
        }
    }
};
```

## 6.3.3 模式定义

> 提供一个接口，让该接口负责创建一系列“相关或者相互依赖的对象”，无需指定它们具体的类。——《设计模式》GoF

### 6.3.4 结构

![](https://img-blog.csdnimg.cn/img_convert/ab4b5c8e20c21d4faba2e488adce7918.png)

- AbstractFactory -> IDBFactory (稳定)
- AbstractProductA -> IDBConnection （稳定）
- AbstractProductB -> IDBCommand / IDataReader （稳定）
- ConcreteFactoryX -> SqlDBFactory / OracleDBFactory (变化)

### 6.3.5 要点总结

- 如果没有应对 **“多系列对象构建”**的需求变化，则没有必要使用Abstract Factory模式，这时候使用简单的工厂完全可以。
- “系列对象”指的是在某一特定系列下的对象之间有相互依赖、或作用的关系。不同系列的对象之间不能相互依赖。
- Abstract Factory模式主要在于应对 **“新系列”的需求**变动。其缺点在于**难以应对“新对象”的需求**变动。

## 6.4 Prototype 原型模式

### 6.4.1 动机（Motivation）

在软件系统中，经常面临着“某些结构复杂的对象”的创建工作；由于需求的变化，这些对象经常面临着剧烈的变化，但是它们却拥有比较稳定一致的接口。

如何应对这种变化？如何向“客户程序（使用这些对象的程序）” 隔离出 “这些易变对象” ，从而使得 “依赖这些易变对象的客户程序” 不随着需求改变而改变？

### 6.4.2 代码示例

工厂方法中的ISplitterFactory.cpp：

```C++
//ISplitterFactory.cpp
//抽象类
class ISplitter {
public:
    virtual void split() = 0;
    virtual ~ISplitter() { }
};

//工厂基类
class SplitterFactory {
public:
    ISplitter* createSplitter() {
        return new BinaryFiltter();
    }
    
    virtual ~SplitterFactory() {}
};
```

原型模式将这两个类进行了合并：

```c++
//ISplitterFactory.cpp
class ISplitter {
public:
    virtual void split() = 0;
    virtual ISplitter* clone() = 0; //通过克隆自己来创建指针
    virtual ~ISplitter() { }
};
```

```c++
//FileSplitter.cpp
//具体类
class BinarySplitter : public ISplitter
{
     virtual ISplitter* clone() {
         return new BinarySplitter(*this); //克隆自己，通过拷贝构造
     }
};

class TxtSplitter : public ISplitter
{
    virtual ISplitter* clone() {
         return new TxtSplitter(*this); //克隆自己，通过拷贝构造
     }
};

class PictureSplitter : public ISplitter
{
    virtual ISplitter* clone() {
         return new PictureSplitter(*this); //克隆自己，通过拷贝构造
     }
};
```

```c++
class VideoSplitter : public ISplitter
{
    virtual ISplitter* clone() {
         return new VideoSplitter(*this); //克隆自己，通过拷贝构造进行深克隆
     }
};
```

```c++
//MainForm.cpp
class MainForm : public Form
{
    ISplitter* prototype; //原型对象
public:
    MainForm(ISplitter* prototype) {
        this->prototype = prototype;
    }
    
    void Button1_Click(){
        ISplitter* splitter = prototype->clone(); //克隆原型
        splitter->split();
    }
};
```

### 6.4.3 模式定义

> 使用原型实例指定创建对象的种类，然后通过拷贝这些原型来创建新的对象。 ——《设计模式》 GoF

### 6.4.4 结构

![](https://img-blog.csdnimg.cn/img_convert/c2bce3c8d754c9aa6682ad0a387632c5.png)

- Prototype -> ISplitter
- ConcretePrototypeX -> XXSplitter
- Client -> MainForm

### 6.4.5 要点总结

- Prototype模式同样用于隔离类对象的使用者和具体类型（易变类）之间的耦合关系，它同样要求这些“易变类”拥有“稳定的接口”。
- Prototype模式对于“如何创建易变类的实体对象”采用“原型克隆”的方法来做，它使得我们可以非常灵活地动态创建“拥有某些稳定接口”的新对象——所需工作仅仅是注册一个新类的对象（即原型），然后在任何需要的地方Clone。
- Prototype模式中的Clone方法可以利用某些框架中的序列化来实现深拷贝。

## 6.5 Builder 构建器

### 6.5.1 动机 (Motivation)

在软件系统中，有时候面临着“一个复杂对象”的创建工作，其通常由各个部分的子对象用一定的算法构成；由于需求的变化，这个复杂对象的各个部分经常面临着剧烈的变化，但是将它们组合在一起的算法却相对稳定。

如何应对这种变化？如何提供一种“封装机制”来隔离出“复杂对象的各个部分”的变化，从而保持系统中的“稳定构建算法”不随着需求改变而改变？

### 6.5.2 模式定义

> 将一个复杂对象的构建与其表示相分离，使得同样的构建过程(稳定)可以创建不同的表示(变化)。——《设计模式》GoF

### 6.5.3 代码示例

```c++
//builder.cpp
class House {
public:
    void Init() {
        this->BuilderPart1();
        
        for (int i = 0; i < 4; i++) {
            this->BuildPart2();
        }
        
        bool flag = this->BuildPart3();
        
        if (flag) { this->BuildPart4(); }
        
        this->BuildPart5();
    }
protected:
    virtual void BuildPart1() = 0;
    virtual void BuildPart2() = 0;
    virtual void BuildPart3() = 0;
    virtual void BuildPart4() = 0;
    virtual void BuildPart5() = 0;
};
```

说明：构造房子的流程不变，但是每个子步骤是变化的。此处不能将构造的流程直接放到构造函数里面：

```c++
//builder.cpp
class House {
public:
   //这种方式不可！！！不能放在构造函数里面
   House() {
        this->BuilderPart1(); //静态绑定
        
        for (int i = 0; i < 4; i++) {
            this->BuildPart2();
        }
        
        bool flag = this->BuildPart3();
        
        if (flag) { this->BuildPart4(); }
        
        this->BuildPart5();
    }
protected:
    virtual void BuildPart1() = 0;
    virtual void BuildPart2() = 0;
    virtual void BuildPart3() = 0;
    virtual void BuildPart4() = 0;
    virtual void BuildPart5() = 0;
};
```

因为C++中在构造函数里不可以调用子类的虚函数，因为是静态绑定。原因是子类的构造函数是先调用父类的构造函数，如果在父类的构造函数里调用子类的虚函数的override版本，就会导致子类的构造函数还没完成，但是子类的虚函数被调用了。

```c++
//builder.cpp
class House {
public:
    void Init() {
        this->BuilderPart1();
        
        for (int i = 0; i < 4; i++) {
            this->BuildPart2();
        }
        
        bool flag = this->BuildPart3();
        
        if (flag) { this->BuildPart4(); }
        
        this->BuildPart5();
    }
    virtual ~House() { }
protected:
    virtual void BuildPart1() = 0;
    virtual void BuildPart2() = 0;
    virtual void BuildPart3() = 0;
    virtual void BuildPart4() = 0;
    virtual void BuildPart5() = 0;
};

class StoneHouse : public House {
protected:
    virtual void BuildPart1() {}
    virtual void BuildPart2() {}
    virtual void BuildPart3() {}
    virtual void BuildPart4() {}
    virtual void BuildPart5() {}
};

int main() {
    House* pHouse = new StoneHouse()；
    pHouse->Init();
    
    return 0;
}
```

一个类中的东西太多不太好，就要进行分离，需要将House构建过程进行提取单独封装为一个类：

```c++
class House {
    //...
};

class HouseBuilder {
public:
    void Init() {
        this->BuilderPart1();
        
        for (int i = 0; i < 4; i++) {
            this->BuildPart2();
        }
        
        bool flag = this->BuildPart3();
        
        if (flag) { this->BuildPart4(); }
        
        this->BuildPart5();
    }
    
    House* GetResult() {
        return pHouse;
    }
    
    virtual ~HouseBuilder() { }
protected:
    House* pHouse;
    virtual void BuildPart1() = 0;
    virtual void BuildPart2() = 0;
    virtual void BuildPart3() = 0;
    virtual void BuildPart4() = 0;
    virtual void BuildPart5() = 0;
};

class StoneHouse : public House {
protected:
    virtual void BuildPart1() {
        //pHouse->Part1 = ...;
    }
    virtual void BuildPart2() {}
    virtual void BuildPart3() {}
    virtual void BuildPart4() {}
    virtual void BuildPart5() {}
};

int main() {
    House* pHouse = new StoneHouse()；
    pHouse->Init();
    
    return 0;
}
```

再将构建流程进行拆分：

```c++
//对象的表示
class House {
    //...
};

//对象的构建
class HouseBuilder {
public:
    House* GetResult() {
        return pHouse;
    }
    
    virtual ~HouseBuilder() { }
protected:
    House* pHouse;
    virtual void BuildPart1() = 0;
    virtual void BuildPart2() = 0;
    virtual void BuildPart3() = 0;
    virtual void BuildPart4() = 0;
    virtual void BuildPart5() = 0;
};

class StoneHouse : public House {
protected:
    virtual void BuildPart1() {
        //pHouse->Part1 = ...;
    }
    virtual void BuildPart2() {}
    virtual void BuildPart3() {}
    virtual void BuildPart4() {}
    virtual void BuildPart5() {}
};

class StoneHouseBuilder : public HouseBuilder {
    
};

class HouseDirector {
public:
    HouseBuilder* pHouseBuilder;
    
    HouseDirector(HouseBuilder* pHouseBuilder) {
    	this->pHouseBuilder = pHouseBuilder;    
    }
    
    House* Construct() {
        pHouseBuilder->BuilderPart1();
        
        for (int i = 0; i < 4; i++) {
            pHouseBuilder->BuildPart2();
        }
        
        bool flag = pHouseBuilder->BuildPart3();
        
        if (flag) { pHouseBuilder->BuildPart4(); }
        
        pHouseBuilder->BuildPart5();
        
        return pHouseBuilder->GetResult();
    }
};
```

### 6.5.4 结构

![](https://img-blog.csdnimg.cn/img_convert/64dec30b2d62415f051e527319c51ff7.png)

- Director -> HouseDirector (稳定)
- Builder -> HouseBuilder (稳定)
- ConcreteBuilder -> StoneHouseBuilder （变化）

### 6.5.5 要点总结

- Builder 模式主要用于“分步骤构建一个复杂的对象”。在这其中“分步骤”是一个稳定的算法，而复杂对象的各个部分则经常变化。
- 变化点在哪里，封装哪里—— Builder模式主要在于应对“复杂对象各个部分”的频繁需求变动。其缺点在于难以应对“分步骤构建算法”的需求变动。
- 在Builder模式中，要注意不同语言中构造器内调用虚函数的差别（C++ vs. C#) 。
