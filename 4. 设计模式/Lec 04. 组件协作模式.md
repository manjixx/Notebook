# 四、“组件”协作模式

- 现代软件专业分工之后的第一个结果是“**框架与应用程序的划分**”，“组件协作”模式**通过晚期绑定**，来实现框架与应用程序之间的松耦合，是二者之间协作时常用的模式。

- 典型模式
  - Template Method
  - Strategy
  - Observer / Event

## 4.1 Template Method 模版方法

### 4.1.1 动机(Motivation)

- 在软件构建过程中，对于某一项任务，它常常有**稳定的**整体操作结构，但各个子步骤却有很多**改变的**需求，或者由于固有的原因（比如框架与应用之间的关系）而无法和任务的整体结构同时实现。

- 如何在**确定稳定操作结构**的前提下，来灵活应对各个**子步骤的变化**或者晚期实现需求？

### 4.1.2 结构化软件设计流程

- template1_lib.cpp **程序库开发人员**

```c++
//程序库开发人员
class Library{
public:
    void Step1() { 
        //... 
    }
    
    void Step3() { 
        //... 
    }
    
    void Step5() { 
        //... 
    }
};
```

- template1_app.cpp **应用程序开发人员**
  
```c++
// 应用程序开发人员
class Application {
public:
    bool Step2() {
        //...
    }
    
    void Step4() {
        //...
    }
};

int main() {
    Library lib();
    Application app();
    
    lib.Step1();
    
    if (app.Step2()) {
        lib.Step3();
    }
    
    for (int i = 0; i < 4; i++) {
        app.Step4();
    }
    
    lib.Step5();
    
    return 0;
}
```

Library开发人员: 开发1、3、5三个步骤
Application开发人员:

- 开发2、4两个步骤
- 程序主流程

### 4.1.3 面向对象软件设计流程

```c++
//template2_lib.cpp
//程序库开发人员
class Library {
public:
    //稳定 template method
    void Run() {
        Step1();
        
        if (Step2()) { //支持变化==> 虚函数的多态调用
            Step3();
        }
        
        for (int i = 0; i < 4; i++) {
            Step4(); //支持变化==> 虚函数的多态调用
        }
        
        Step5();
    }
    //基类中的析构函数要写成虚函数，否则delete的时候的调用不到子类的析构函数
    virtual ~Library() { }
    
protected:
    void Step1() { //稳定
        //...
    }
    
    void Step3() { //稳定
        //...
    }
    
    void Step5() { //稳定
        //...
    }
    
    virtual bool Step2() = 0; //变化
    virtual bool Step4() = 0; //变化
};
```

```c++
//template2_app.cpp
//应用开发人员
class Application : public Library {
protected:
    virtual bool Step2() {
        //... 子类重写实现
    }
    
    virtual bool Step4() {
        //... 子类重写实现
    }
};

//规范的
int main() {
    Library* pLib = new Application(); //pLib是个多态指针
    pLib->Run();
    
    delete pLib; 
}
```

Library开发人员:

- 开发1、3、5三个步骤
- 程序主流程

Application开发人员:

- 开发2、4两个步骤

### 4.1.4 早绑定与晚绑定

两种调用关系:

- 早绑定:
  - Library <--早绑定-- Application
  - 结构化软件设计的流程是一种早绑定的写法，Library写的比Application早，实现比较晚的调用实现比较早的程序就叫做早绑定

- 晚绑定:
  - Library --晚绑定--> Application
  - 面向对象软件设计的流程是一种晚绑定的写法，Library反过来调用Application，实现的比较早的调用实现比较晚的就叫做晚绑定；

### 4.1.5 模式定义

> 定义一个操作中的算法的**骨架**(稳定)，而将一些**步骤延迟(变化)**到子类中。Template Method使得子类可以**不改变(复用)**一个算法的结构即**可重定义(override 重写)** 该算法的某些特定步骤。                    ——《设计模式》GoF

- 此处的“骨架”对应于上面的第二种写法中的Run
- “延迟到子类”的意思就是定义虚函数让子类去实现或重写，就是支持子类来变化。
- 第二种写法中的模板方法就是Run，它是**相对稳定**的，但是它其中又包含了变化（Step2和Step4）。
- 如果极端地讨论，**全部是稳定的**或者**全部是变化的**都不适合使用设计模式。

设计模式应用的核心就是分辨出变化和稳定。

### 4.1.6 结构

![](https://img-blog.csdnimg.cn/img_convert/c7420b923bd86761692d65c6c0b3bd54.png)

`AbstractClass`中的`TemplateMethod()`是稳定的，*PrimitiveOperationX()* 是变化的。设计模式的学习重点就是区分开“稳定”和“变化”的部分。

对应到之前的代码实现：

- `AbstractClass`就是`Library`类；
- `TemplateMethod()`就是`Run()`方法；
- `PrimitiveOperation1()` 对应于 `Step2()`方法； `PrimitiveOperation2()` 对应于 `Step4()` 方法；
- `ConcreteClass`就是`Application`类；

### 4.1.7 要点总结

- Template Method模式是一种**非常基础性**的设计模式，在面向对象系统中有着大量的应用。它用最简洁的机制（虚函数的多态性）为很多应用程序框架提供了灵活的**扩展点**【注：**扩展点就是继承+虚函数**】，是代码复用方面的基本实现结构。
- 除了可以灵活应对子步骤的变化外，==“不要调用我，让我来调用你”== 的反向控制结构是`Template Method`的典型应用
- 在具体实现方面，被`Template Method` 调用的虚方法可以具有实现，也可以没有任何实现（抽象方法、纯虚方法），但一般推荐将它们设置为 `protected` 方法。

## 4.2 Strategy 策略模式

与模版模式有异曲同工之妙

### 4.2.1 动机（Motivation）

在软件构建过程中，某些对象使用的算法可能多种多样，经常改变，如果将这些算法都编码到对象中，将会使对象变得异常复杂；而且有时候支持不使用的算法也是一个性能负担。
如何在运行时根据需要透明地更改对象的算法？将算法与对象本身解耦，从而避免上述问题？

### 4.2.2 模式定义

> 定义一系列算法，把它们一个个封装起来，并且使它们可**互相替换（变化）**。该模式使得算法可**独立于**使用它的客户程序(稳定)而变化（扩展，子类化）。 ——《设计模式》GoF

### 4.2.3 代码示例

```c++
//strategy1.cpp
enum TaxBase {
    CN_Tax,
    US_Tax,
    DE_Tax,
    FR_Tax       //更改
};
 
class SalesOrder{
    TaxBase tax;
public:
    double CalculateTax(){
        //...
        
        if (tax == CN_Tax){
            //CN***********
        }
        else if (tax == US_Tax){
            //US***********
        }
        else if (tax == DE_Tax){
            //DE***********
        }
        else if (tax == FR_Tax){  //更改
            //...
        }

        //....
     }
    
};
//说明：这种方式更改的时候违反了开放封闭原则，对扩展开放对更改封闭
```

```c++
//strategy2.cpp
class TaxStrategy{
public:
    virtual double Calculate(const Context& context)=0;
    virtual ~TaxStrategy(){}
};

//规范的写法是每个类放在不同的文件中

class CNTax : public TaxStrategy{
public:
    virtual double Calculate(const Context& context){
        //***********
    }
};

class USTax : public TaxStrategy{
public:
    virtual double Calculate(const Context& context){
        //***********
    }
};

class DETax : public TaxStrategy{
public:
    virtual double Calculate(const Context& context){
        //***********
    }
};


//扩展：正常应该是在一个新的文件中写，此处只是为了方便演示
//*********************************
class FRTax : public TaxStrategy{
public:
    virtual double Calculate(const Context& context){
        //.........
    }
};


class SalesOrder{
private:
    TaxStrategy* strategy; //抽象类，必须放一个指针，而且具有多态性

public:
    SalesOrder(StrategyFactory* strategyFactory){
        this->strategy = strategyFactory->NewStrategy();
    }
    ~SalesOrder(){
        delete this->strategy;
    }

    public double CalculateTax(){
        //...
        Context context();
        
        double val = 
            strategy->Calculate(context); //多态调用
        //...
    }
    
};

//说明：这种方式扩展的时候遵循了开放封闭原则
```

“复用”指的是**编译后二进制层级的复用性**，是编译单位的复用性，而不是简单的代码片段的复用。SalesOrder是稳定的，各种XXTax 是变化的。

### 4.2.4 结构

![](https://img-blog.csdnimg.cn/img_convert/34d40a3726b5ca3c3f3fffdc78128e64.png)

- `Context`和`Strategy`是稳定的，`ConcreteStrategyX`是变化的
- `Context`对应上述的`SalesOrder`，`Strategy`对应`TxStrategy`
- `ConcreteStrategyX` 对应 `xxTax`

### 4.2.5 要点总结

- Strategy及其子类为组件提供了一系列可重用的算法，从而可以使得类型在运行时方便地根据需要在各个算法之间进行切换。
- Strategy模式**提供了用条件判断语句以外的另一种选择**，消除条件判断语句，就是在解耦合。含有许多条件判断语句的代码通常都需要Strategy模式。  
  - 绝对稳定不变的情况可以用if-else，如性别、一周七天，而其他的可能变化条件判断的情况就要用Strategy模式。
  - 代码示例中的第一种写法的很多条件判断代码可能根本不会执行，但是却被迫装载到了CPU高级缓存中，占用了缓存位置，其他代码可能被挤出高级缓存，不得不装载到硬盘；而第二种写法则不会有这个问题，减轻了性能负担，但这不是Strategy模式的最大优势，**Strategy模式的最大优势是用扩展应对变化。**
  - 看到条件判断的情况，都要考虑能不能使用Strategy模式。
- 如果Strategy对象没有实例变量，那么各个上下文可以共享同一个Strategy对象，从而节省对象开销。【注：一般可以使用单例模式】

## 4.3 Observer 观察者模式

### 4.3.1 动机（Motivation）

- 在软件构建过程中，我们需要为某些对象建立一种 **“通知依赖关系”** ——一个对象（目标对象）的状态发生改变，所有的依赖对象（观察者对象）都将得到通知。如果这样的依赖关系过于紧密，将使软件不能很好地抵御变化。
- 使用面向对象技术，可以**将这种依赖关系弱化**，并**形成一种稳定的依赖关系**。从而实现软件体系结构的松耦合。

### 4.3.2 模式定义

> 定义对象间的一种**一对多（变化）的依赖关系**，以便**当一个对象(Subject)的状态**发生改变时，所有依赖于它的对象都得到通知并自动更新。           ​ ——《设计模式》GoF

### 4.3.3 代码示例
  
实现一个文件分割器

- 第一种方案：

```c++
//FileSplitter1.cpp
class FileSplitter
{
    string m_filePath;
    int m_fileNumber;
    ProgressBar* m_progressBar; //注：ProgressBar是实现细节，容易变化。 是个通知控件

public:
    FileSplitter(const string& filePath, int fileNumber, ProgressBar* progressBar) :
        m_filePath(filePath), 
        m_fileNumber(fileNumber),
        m_progressBar(progressBar){

    }

    void split(){

        //1.读取大文件

        //2.分批次向小文件中写入
        for (int i = 0; i < m_fileNumber; i++){
            //...
            float progressValue = m_fileNumber;
            progressValue = (i + 1) / progressValue;
            m_progressBar->setValue(progressValue); //更新进度条
        }
    }
};
```

```c++
//MainForm1.cpp
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

存在的问题：**违背了DIP原则**，如果A依赖于B——编译时“依赖”，即A编译的时候B要存在。此处犯了依赖依赖于细节。

- 重构使得遵循DIP原则：

```c++
//FileSplitter1.cpp
class IProgress{
public:
    virtual void DoProgress(float value)=0;
    virtual ~IProgress(){}
    };

class FileSplitter
{
    string m_filePath;
    int m_fileNumber;
    //ProgressBar* m_progressBar; //注：ProgressBar是实现细节，容易变化。 是个通知控件
    IProgress* m_iprogress;
public:
    FileSplitter(const string& filePath, int fileNumber, IProgress* iprogress;) :
        m_filePath(filePath), 
        m_fileNumber(fileNumber),
        m_iprogress(iprogress){
    }

    void split(){

        //1.读取大文件

        //2.分批次向小文件中写入
        for (int i = 0; i < m_fileNumber; i++){
            //...
            float progressValue = m_fileNumber;
            progressValue = (i + 1) / progressValue;
            m_iprogress->DoProgress(progressValue); //更新进度条
        }
    }
};
```

```c++
//MainForm2.cpp
class MainForm : public Form, public IProgress
{
    TextBox* txtFilePath;
    TextBox* txtFileNumber;
    ProgressBar* progressBar;

    public:
    void Button1_Click(){
        string filePath = txtFilePath->getText();
        int number = atoi(txtFileNumber->getText().c_str());
        FileSplitter splitter(filePath, number, this);
        splitter.split();
    }

    virtual void DoProgress(float value) {
        progressBar->setValue(value);
    }
};
```

- 进一步的小优化：

```c++
//FileSplitter1.cpp
class IProgress{
public:
    virtual void DoProgress(float value)=0;
    virtual ~IProgress(){}
    };

class FileSplitter
{
    string m_filePath;
    int m_fileNumber;
    //ProgressBar* m_progressBar; //注：ProgressBar是实现细节，容易变化。 是个通知控件
    IProgress* m_iprogress;
public:
    FileSplitter(const string& filePath, int fileNumber, IProgress* iprogress;) :
        m_filePath(filePath), 
        m_fileNumber(fileNumber),
        m_iprogress(iprogress){

    }

    void split(){

        //1.读取大文件

        //2.分批次向小文件中写入
        for (int i = 0; i < m_fileNumber; i++){
            //...
            float progressValue = m_fileNumber;
            progressValue = (i + 1) / progressValue;
            onProgress(progressValue); 
        }
    }
protected:
    virtual void onProgress(float value) {
        if (m_iprogress != nullptr) {
            m_iprogress->DoProgress(value);//更新进度条
        }
    }
};
```

- 目前的实现只能支持一个观察者，此处就是MainForm。修改使得支持多个观察者：

```c++
//FileSplitter2.cpp
class IProgress{
public:
    virtual void DoProgress(float value)=0;
    virtual ~IProgress(){}
};


class FileSplitter
{
    string m_filePath;
    int m_fileNumber;

    List<IProgress*>  m_iprogressList; // 抽象通知机制，支持多个观察者

public:
    FileSplitter(const string& filePath, int fileNumber) :
        m_filePath(filePath), 
        m_fileNumber(fileNumber){

    }


    void split(){

        //1.读取大文件

        //2.分批次向小文件中写入
        for (int i = 0; i < m_fileNumber; i++){
            //...

            float progressValue = m_fileNumber;
            progressValue = (i + 1) / progressValue;
            onProgress(progressValue);//发送通知
        }
    }

    void addIProgress(IProgress* iprogress){
        m_iprogressList.add(iprogress);
    }

    void removeIProgress(IProgress* iprogress){
        m_iprogressList.remove(iprogress);
    }


protected:
    virtual void onProgress(float value){
        List<IProgress*>::iterator itor = m_iprogressList.begin();
        while (itor != m_iprogressList.end() ){
            (*itor)->DoProgress(value); //更新进度条
            itor++;
        }
    }
};

```

```c++
//MainForm2.cpp
class MainForm : public Form, public IProgress
{
    TextBox* txtFilePath;
    TextBox* txtFileNumber;

    ProgressBar* progressBar;

public:
    void Button1_Click(){

        string filePath = txtFilePath->getText();
        int number = atoi(txtFileNumber->getText().c_str());

        ConsoleNotifier cn;

        FileSplitter splitter(filePath, number);

        splitter.addIProgress(this); //订阅通知
        splitter.addIProgress(&cn)； //订阅通知

        splitter.split();

        splitter.removeIProgress(this);

    }

    virtual void DoProgress(float value){
        progressBar->setValue(value);
    }
};

class ConsoleNotifier : public IProgress {
public:
    virtual void DoProgress(float value){
        cout << ".";
    }
};
```

### 4.3.3 结构

![](https://img-blog.csdnimg.cn/img_convert/d8bd97350f763a1985398e2b1d5bee49.png)

- Observer对应于IProgress
- Update()对应于DoProgress()
- Attach对应于addIProgress，Detach对应于removeIProgress，Notify对应于onProgress,GOF中建议将这三个方法提出来放到一个父类中，其他的Subject继承它，但是此处我们没有将它提出来，
- ConcreteSubject就是FileSplitter，ConcreteObserver对应于MainForm和ConsoleNotifier，具体的观察者。

稳定的：Subject、Observer

变化的：ConcreteSubject、ConcreteObserver

### 4.3.5 要点总结

观察者模式的核心是:抽象的通知 依赖关系

- 使用面向对象的抽象，Observer模式使得我们可以**独立地**改变目标与观察者，从而使二者之间的依赖关系达致松耦合。
- 目标发送通知时，无需指定观察者，通知（可以携带通知信息作为参数）会自动传播。
- 观察者自己决定是否需要订阅通知，目标对象对此一无所知。
- Observer模式是基于事件的UI框架中非常常用的设计模式，也是MVC模式的一个重要组成部分。
