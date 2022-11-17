# 九、“状态变化”模式

## 9.1 概述

在组件构建过程中，某些**对象的状态经常面临变化**，如何对这些变化进行有效的管理？同时又维持高层模块的稳定？“状态变化”模式为这一问题提供了一种解决方案。

典型模式

- State
- Memento

## 9.2 State 状态模式

### 9.2.1 动机（Motivation）

在软件构建过程中，某些对象的状态如果改变，其行为也会随之而发生变化，比如文档处于只读状态，其支持的行为和读写状态支持的行为就可能完全不同。

如何在运行时根据对象的状态来透明地更改对象的行为？而不会为对象操作和状态转化之间引入紧耦合？

### 9.2.2 代码示例

```c
//state1.cpp
enum NetworkState
{
    Network_Open,
    Network_Close,
    Network_Connect,
};

class NetworkProcessor{
    
    NetworkState state;
public:
    
    void Operation1(){ //根据state不同而操作不同
        if (state == Network_Open){

            //**********
            state = Network_Close;
        } else if (state == Network_Close){

            //..........
            state = Network_Connect;
        } else if (state == Network_Connect){

            //$$$$$$$$$$
            state = Network_Open;
        }
    }

    public void Operation2(){

        if (state == Network_Open){
            
            //**********
            state = Network_Connect;
        } else if (state == Network_Close){

            //.....
            state = Network_Open;
        } else if (state == Network_Connect){

            //$$$$$$$$$$
            state = Network_Close;
        }
    
    }

    public void Operation3(){

    }
};
```

枚举类型中如何添加了一种的状态，那么操作里面都要进行改变，**违反了开闭原则**。

将枚举类型转换为抽象基类，操作变成状态对象的行为：

```c
//state2.cpp
class NetworkState{

public:
    NetworkState* pNext;
    virtual void Operation1()=0;
    virtual void Operation2()=0;
    virtual void Operation3()=0;

    virtual ~NetworkState(){}
};


class OpenState :public NetworkState{
    
    static NetworkState* m_instance;
public:
    static NetworkState* getInstance(){
        if (m_instance == nullptr) {
            m_instance = new OpenState();
        }
        return m_instance;
    }

    void Operation1(){
        
        //**********
        pNext = CloseState::getInstance();
    }
    
    void Operation2(){
        
        //..........
        pNext = ConnectState::getInstance();
    }
    
    void Operation3(){
        
        //$$$$$$$$$$
        pNext = OpenState::getInstance();
    }
};

class CloseState:public NetworkState{ };
//...
//扩展
class WaitState: public NetworkState { };

class NetworkProcessor{
    
    NetworkState* pState;
    
public:
    
    NetworkProcessor(NetworkState* pState){
        
        this->pState = pState;
    }
    
    void Operation1(){
        //...
        pState->Operation1();
        pState = pState->pNext;
        //...
    }
    
    void Operation2(){
        //...
        pState->Operation2();
        pState = pState->pNext;
        //...
    }
    
    void Operation3(){
        //...
        pState->Operation3();
        pState = pState->pNext;
        //...
    }

};
```

当状态增加的时候，`NetworkProcesser`中不必发生改变，达到了稳定。

### 9.2.3 模式定义

> 允许一个对象在其内部状态改变时改变它的行为。从而使对象看起来似乎修改了其行为。 ——《设计模式》GoF

### 9.2.4 结构

![](https://img-blog.csdnimg.cn/img_convert/f9477f0195c300d3314f04bca5328ae4.png)

- Context -> NetworkProcesser （稳定）
- State -> NetworkState (稳定)
- ConcreteStateX -> xxState （变化）

### 9.2.5 要点总结

- State模式将所有与一个特定状态相关的行为都放入一个 State 的子类对象中，在对象状态切换时，切换相应的对象；但同时维持 State 的接口，这样实现了具体操作与状态转换之间的解耦。
- 为不同的状态引入不同的对象使得状态转换变得更加明确，而且可以保证不会出现状态不一致的情况，因为转换是原子性的——即要么彻底转换过来，要么不转换。
- 如果State对象没有实例变量，那么各个上下文可以共享同一个 State 对象【注：使用了Singleton模式】，从而节省对象开销。

## 9.3 Memento 备忘录

### 9.3.1 动机（Motivation）

在软件构建过程中，某些对象的状态在转换过程中，可能由于某种需要，要求程序能够回溯到对象之前处于某个点时的状态。如果使用一些公有接口来让其他对象得到对象的状态，便会暴露对象的细节实现。
如何实现对象状态的良好保存与恢复？但同时又不会因此而破坏对象本身的封装性。

### 9.3.2 模式定义

> 在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态。这样以后就可以将该对象恢复到原先保存的状态。 ——《设计模式》GoF

### 9.3.3 代码示例

```c
//memento.cpp
class Memento
{
    string state;
    //..
public:
    Memento(const string & s) : state(s) {}
    string getState() const { return state; }
    void setState(const string & s) { state = s; }
};

class Originator
{
    string state;
    //....
public:
    Originator() {}
    Memento createMomento() {
        Memento m(state);
        return m;
    }
    void setMomento(const Memento & m) {
        state = m.getState();
    }
};

int main()
{
    Originator orginator;
    
    //捕获对象状态，存储到备忘录
    Memento mem = orginator.createMomento();
    
    //... 改变orginator状态
    
    //从备忘录中恢复
    orginator.setMomento(memento);
}
```

### 9.3.4 结构

![](https://img-blog.csdnimg.cn/img_convert/0678690c5c9ee51b583c3254a9fb37ab.png)

### 9.3.5 要点总结

- 备忘录（Memento）存储原发器（Originator）对象的内部状态，在需要时恢复原发器状态。
- Memento模式的核心是信息隐藏，即Originator需要向外界隐藏信息，保持其封装性。但同时又需要将状态保存到外界（Memento）。
- 由于现代语言运行时（如C#、Java等）都具有相当的对象序列化支持，因此往往采用效率较高、又较容易正确实现的序列化方案来实现Memento模式。
