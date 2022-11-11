# 八、接口隔离模式

## 8.1 概述

在组件构建过程中，某些接口之间直接的依赖常常会带来很多问题、甚至根本无法实现。采用添加一层间接（稳定）接口，来隔离本来互相紧密关联的接口是一种常见的解决方案。

典型模式

- Facade 【注：解决系统内和系统外】
- Proxy 【注：两个对象，由于安全/分布式/性能的原因不能直接依赖，必须隔离】
- Adapter 【注：解决老接口和新接口的不匹配问题】
- Mediator 【注：解耦系统内对象间的关联关系】

## 8.2 Facede 门面模式

### 8.2.1 系统间耦合的复杂度

![](https://img-blog.csdnimg.cn/img_convert/6d2df1515e931197ad262439afea4a40.png)

### 8.2.2 动机（Motivation)

上述 A 方案的问题在于组件的客户和组件中各种复杂的子系统有了过多的耦合，随着外部客户程序和各子系统的演化，这种过多的耦合面临很多变化的挑战。
如何简化外部客户系统和系统间的交互接口？如何将外部客户程序的演化和内部子系统的变化之间的依赖相互解耦？

### 8.2.3 模式定义

> 为子系统中的一组接口提供一个一致（稳定）的界面，Facade 模式定义了一个高层接口，这个接口使得这一子系统更加容易使用（复用）。——《设计模式》 GoF

### 8.2.4 结构

![](https://img-blog.csdnimg.cn/img_convert/0bf63e9c83cdee007f8973be3e0a44d5.png)

- Facade （稳定）
- 其他的可能会变化

### 8.2.5 要点总结

- 从客户程序的角度来看，Facade模式简化了整个组件系统的接口，对于组件内部与外部客户程序来说，达到了一种“解耦”的效果——内部子系统的任何变化不会影响到Facade接口的变化。
- Facade设计模式更注重从架构的层次去看整个系统，而不是单个类的层次。Facade很多时候更是一种架构设计模式。
- Facade设计模式并非一个集装箱，可以任意地放进任何多个对象。Facade模式中组件的内部应该是“相互耦合关系比较大的一系列组件”，而不是一个简单的功能集合。

## 8.3 Proxy 代理模式

### 8.3.1 动机（Motivation）

在面向对象系统中，有些对象由于某种原因（比如对象创建的开销很大，或者某些操作需要安全控制，或者需要进程外的访问等），直接访问会给使用者、或者系统结构带来很多麻烦。
如何在不失去透明操作（一致性）对象的同时来管理/控制这些对象特有的复杂性？增加一层间接层是软件开发中常见的解决方式。

### 8.3.2 模式定义

> 为其他对象提供一种代理以控制（隔离，使用接口）对这个对象的访问。 ——《设计模式》GoF

### 8.3.3 结构

![](https://img-blog.csdnimg.cn/img_convert/d752fda0d94573e75686a9ea100a9d9a.png)

### 8.2.4 代码示例

```c++
//client.cpp
class ISubject{
public:
    virtual void process();
};

class RealSubject: public ISubject{
public:
    virtual void process(){
        //....
    }
};

class ClientApp{
    
    ISubject* subject;
    
public:
    
    ClientApp(){
        subject=new RealSubject();
    }
    
    void DoTask(){
        //...
        subject->process();
        
        //....
    }
};
```

```c++
//proxy.cpp
class ISubject{
public:
    virtual void process();
};


//Proxy的设计
class SubjectProxy: public ISubject{
public:
    virtual void process(){
        //对RealSubject的一种间接访问
        //....
    }
};

class ClientApp{
    
    ISubject* subject;
    
public:
    
    ClientApp(){
        subject = new SubjectProxy(); //可以通过某种工厂模式进行创建
    }
    
    void DoTask(){
        //...
        subject->process();
        
        //....
    }
};
```

### 8.3.5 要点总结

- “增加一层间接层” 是软件系统中对许多复杂问题的一种常见解决方法。在面向对象系统中，直接使用某些对象会带来很多问题，作为间接层的proxy对象便是解决这一问题的常用手段。
- 具体proxy设计模式的实现方法、实现粒度都相差很大，有些可能对单个对象做细粒度的控制，如copy-on-write技术，有些可能对组件模块提供抽象代理层，在架构层次对对象做proxy。
- Proxy 并不一定要求保持接口完整的一致性，只要能够实现间接控制，有时候损及一些透明性是可以接受的。

## 8.4 Adapter 适配器模式

### 8.4.1 动机

在软件系统中，由于应用环境的变化，常常需要将“一些现存的对象” 放在新的环境中应用，但是新环境要求的接口时这些现存对象所不满足的。

如何应对这种“迁移的变化”？如何既能利用现有对象的良好实现，同时又能满足新的应用环境所要求的接口？

### 8.4.2 我们身边的Adapter

![](https://img-blog.csdnimg.cn/img_convert/c806bb7843ee166eb47b5a71826e0d3e.png)

### 8.4.3 模式定义

> 将一个类的接口转换成客户希望的另一个接口。Adapter模式使得原本由于接口不兼容而不能一起工作的那些类可以一起工作。 ——《设计模式》GoF

### 8.4.4 结构

![](https://img-blog.csdnimg.cn/img_convert/044aadad7a20e0abcc535525b949ccd8.png)

- Target 是希望的接口 （稳定）
- Adaptee 是以前的接口 （稳定）
- Adapter 具有和父类一样的接口规范，实现了Adapter向Target的转换 （变化）

### 8.4.5 代码示例

```c++
//Adapter.cpp
//目标接口（新接口）
class ITarget{
public:
    virtual void process() = 0;
};

//遗留接口（老接口）
class IAdaptee{
public:
    virtual void foo(int data) = 0;
    virtual int bar() = 0;
};

//遗留类型
class OldClass: public IAdaptee{
    //....
};

//GoF中适配器有两种：对象适配器和类适配器
//对象适配器：组合了一个对象
class Adapter: public ITarget{ //继承
protected:
    IAdaptee* pAdaptee;//组合
    
public:
    Adapter(IAdaptee* pAdaptee){
        this->pAdaptee = pAdaptee;
    }
    
    virtual void process(){
        int data = pAdaptee->bar();
        pAdaptee->foo(data);
        
    }
};


//类适配器
class Adapter: public ITarget, protected OldClass{ //多继承
                           
};

int main(){
    IAdaptee* pAdaptee = new OldClass();

    ITarget* pTarget=new Adapter(pAdaptee);
    pTarget->process();
    
    return 0; 
}
```

```c++
//STL中的Adapter模式的应用:将dequeue转换成stack/queue
class stack{
    deqeue container;
    
};

class queue{
    deqeue container;
    
};

```

### 8.4.6 要点总结

- Adapter模式主要应用于“希望复用一些现存的类，但是接口又与复用环境要求不一致的情况”，在遗留代码复用、类库迁移等方面非常有用。
- GoF 23 定义了两种 Adapter 模式的实现结构：对象适配器和类适配器。但类适配器采用“多继承”的实现方式，一般不推荐使用。对象适配器采用“对象组合”的方式，更符合松耦合精神。
- Adapter模式可以实现得非常灵活，不必拘泥于 GoF 23 中定义的两种结构。例如，完全可以将Adapter模式中的“现存现象”作为新的接口方法参数，来达到适配的目的。

## 8.5 Mediator 中介者模式

### 8.5.1 动机

在软件构建过程中，经常会出现多个对象互相关联交互的情况，对象之间常常会维持一种复杂的引用关系，如果遇到一些需求的更改，这种直接的引用关系将面临不断的变化。
在这种情况下，我们可使用一个“中介对象”来管理对象间的关联关系，避免相互交互的对象之间的紧耦合引用关系，从而更好地抵御变化。

### 8.5.2 模式定义

> 用一个中介对象来封装（封装变化）一系列的对象交互。中介者使各对象不需要显式地相互引用（编译时依赖->运行时依赖），从而使其耦合松散（管理变化），而且可以独立地改变它们之间的交互。 ——《设计模式》GoF

### 8.5.3 结构

![](https://img-blog.csdnimg.cn/img_convert/af74bf829afca8fe39b94c0e1522b24c.png)

- Mediator 和 Colleague 之间是双向依赖，而ConcreteColleague 之间没有依赖关系，通过这种方式达到了依赖的解耦

梳理结构中的关系：

![](https://img-blog.csdnimg.cn/img_convert/d63869c4db7c7538e745f03516b58975.png)

需要定义消息通知的规范/协议，比如1要和3通信，如何通过Mediator找到3，这就要通过消息通知的规范。

上图是将直接依赖关系 转化为 间接依赖关系，和Facade模式异曲同工，但是Facade解决的是系统内和系统外的耦合，而中介者模式解决的系统内各个组件之间的耦合。

### 8.5.4 要点总结

- 将多个对象间复杂的关联关系解耦，Mediator模式将多个对象间的控制逻辑进行集中管理【注：定义一套调用机制的协议】，变“多个对象互相关联”为“多个对象和一个中介者关联”，简化了系统的维护，抵御了可能的变化。
- 随着控制逻辑的复杂化，Mediator具体对象的实现可能相当复杂。这时候可以对Mediator对象进行分解处理。
- Facade模式是解耦系统间（单向）的对象关联关系；Mediator模式是解耦系统内各个对象之间（双向）的关联关系。
