# 十一、“行为变化”模式

## 11.1 概述

在组件的构建过程中，组件行为的变化经常导致组件本身剧烈的变化。“行为变化”模式将组件的行为和组件本身进行解耦，从而支持组件行为的变化，实现两者之间的松耦合。

典型模式
- Command
- Visitor

## 11.2 Command 命令模式

### 11.2.1 动机

在软件构建过程中，“行为请求者”与“行为实现者”通常呈现一种“紧耦合”。但在某些场合——比如需要对行为进行“记录、撤销/重（undo/redo)、事务”等处理，这种无法抵御变化的紧耦合是不合适的。
在这种情况下，如何将“行为请求者”与“行为实现者”解耦？将一组行为抽象为对象，可以实现二者之间的松耦合。

### 11.2.2 模式定义

> 将一个请求（行为）封装为一个对象，从而使你可用不同的请求对客户进行参数化；对请求排队或记录请求日志，以及支持可撤销的操作。——《设计模式》GoF

### 11.2.3 代码示例

```c
//Command.cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;


class Command
{
public:
    virtual void execute() = 0;
};

class ConcreteCommand1 : public Command
{
    string arg;
public:
    ConcreteCommand1(const string & a) : arg(a) {}
    void execute() override
    {
        cout<< "#1 process..."<<arg<<endl;
    }
};

class ConcreteCommand2 : public Command
{
    string arg;
public:
    ConcreteCommand2(const string & a) : arg(a) {}
    void execute() override
    {
        cout<< "#2 process..."<<arg<<endl;
    }
};
        
        
class MacroCommand : public Command
{
    vector<Command*> commands;
public:
    void addCommand(Command *c) { commands.push_back(c); }
    void execute() override
    {
        for (auto &c : commands)
        {
            c->execute();
        }
    }
};
        
        
int main()
{

    ConcreteCommand1 command1(receiver, "Arg ###");
    ConcreteCommand2 command2(receiver, "Arg $$$");
    
    MacroCommand macro;
    macro.addCommand(&command1);
    macro.addCommand(&command2);
    
    macro.execute();

}
```

### 11.2.4 结构

![](https://img-blog.csdnimg.cn/img_convert/4caf73c25999ef81b22cef74ecdd15c6.png)

`Command` 稳定
`ConcreteCommand` 变化

### 11.2.5 要点总结

- Command模式的根本目的在于将“行为请求者”与“行为实现者”解耦，在面向对象语言中，常见的实现手段是“将行为抽象为对象”。
- 实现Command接口的具体命令对象ConcreteCommand有时候根据需要可能会保存一些额外的状态信息。通过使用Composite模式，可以将多个“命令”封装为一个“复合命令”MacroCommand。
- Command模式与C++中的函数对象有些类似。但两者定义行为接口的规范有所区别：- Command以面向对象中的“接口-实现”来定义行为接口规范，更严格，但有性能损失；C++函数对象以函数签名来定义行为接口规范，更灵活，性能更高。

## 11.3 Visitor访问器

### 11.3.1 动机

在软件构建过程中，由于需求的改变，某些类层次结构【注：从基类到子类】中常常需要增加新的行为（方法），如果直接在基类中做这样的更改，将会给子类带来很繁重的变更负担，甚至破坏原有设计。
如何在不更改类层次结构的前提下，在运行时根据需要透明地为类层次结构上的各个类动态添加新的操作，从而避免上述问题？

### 11.3.2 模式定义

> 表示一个作用于某对象结构中的各元素的操作。使得可以在不改变（稳定）各元素的类的前提下定义（扩展）作用于这些元素的新操作（变化）。 ——《设计模式》GoF

### 11.3.3 代码示例

```c
//visitor1.cpp
#include <iostream>
using namespace std;

class Visitor;


class Element
{
public:
    virtual void Func1() = 0;
    
    virtual void Func2(int data)=0; //若有新需求时，更改基类，则子类也会随着改变，负担很重
    virtual void Func3(int data)=0;
    //...
    
    virtual ~Element(){}
};

class ElementA : public Element
{
public:
    void Func1() override{
        //...
    }
    
    void Func2(int data) override{
        //...
    }
    
};

class ElementB : public Element
{
public:
    void Func1() override{
        //***
    }
    
    void Func2(int data) override {
        //***
    }
};
```

使用Visitor模式：

```C
//visitor2.cpp
#include <iostream>
using namespace std;

class Visitor;

class Element
{
public:
    virtual void accept(Visitor& visitor) = 0; //第一次多态辨析

    virtual ~Element(){}
};

class ElementA : public Element
{
public:
    void accept(Visitor &visitor) override {
        visitor.visitElementA(*this);
    }
};

class ElementB : public Element
{
public:
    void accept(Visitor &visitor) override {
        visitor.visitElementB(*this); //第二次多态辨析
    }

};


class Visitor{
public:
    virtual void visitElementA(ElementA& element) = 0;
    virtual void visitElementB(ElementB& element) = 0;
    
    virtual ~Visitor(){}
};

//上面是已经设计好的，不更改
//==================================

//扩展1
class Visitor1 : public Visitor{
public:
    void visitElementA(ElementA& element) override{
        cout << "Visitor1 is processing ElementA" << endl;
    }
        
    void visitElementB(ElementB& element) override{
        cout << "Visitor1 is processing ElementB" << endl;
    }
};
     
//扩展2
class Visitor2 : public Visitor{
public:
    void visitElementA(ElementA& element) override{
        cout << "Visitor2 is processing ElementA" << endl;
    }
    
    void visitElementB(ElementB& element) override{
        cout << "Visitor2 is processing ElementB" << endl;
    }
};
        
        
int main()
{
    Visitor2 visitor;
    ElementB elementB;
    elementB.accept(visitor);// double dispatch
    
    ElementA elementA;
    elementA.accept(visitor);

    return 0;
}
```

### 11.3.4 结构

![](https://img-blog.csdnimg.cn/img_convert/9eaf95414bf2e8c707822549dacb48fb.png)

- Visitor、Element、ConcreteElementA和 ConcreteElementB 必须是稳定的，使用Visitor模式的前提是必须知道Element有几个子类，对应的设计几个访问函数，Vistor稳定的前提是Element的所有子类都确定，这是这个模式非常大的缺点；如果Element类层次结构无法稳定，则Visitor模式不适用了；
- ConcreteVisito1 和 ConcreteVisitor2 是可以变化的。

### 11.3.5 要点总结

- Visitor模式通过所谓双重分发（double dispatch）来是按在不更改（不添加新的操作-编译时）Element类层次结构的前提下，在运行时透明地为类层次结构上的各个类动态添加新的操作（支持变化）。
- 所谓双重分发即Visitor模式中间包括了两个多态分发（注意其中的多态机制）：第一个为accept方法的多态辨析；第二个为VisitElementX方法的多态辨析。
- Visitor模式的最大缺点在于扩展类层次结构（增添新的Element子类），会导致Visitor类的改变。因此Visitor模式适用于“Element类层次结构稳定，而其中的操作却经常面临频繁改动”