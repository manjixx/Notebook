# 七、对象性能模式

## 7.1 概述

面向对象很好地解决了“抽象”的问题，但是必不可免地要付出一定的代价。对于通常情况来讲，面向对象的成本大都可以忽略不计。但是某些情况，面向对象所带来的成本必须谨慎处理。

典型模式：

- Singleton
- Flyweight

## 7.2 Singleton 单例模式

### 7.1.1 动机（Motivation）

在软件系统中，经常有这样一些特殊的类，必须保证它们在系统中只存在一个实例，才能确保它们的逻辑正确性、以及良好的效率。
如何绕过常规的构造器，提供一种机制来保证一个类只有一个实例？
这应该是类设计者的责任，而不是使用者的责任。

### 7.2.2 代码示例

```c++
//Singleton.cpp
class Singleton {
private:
    //必须将类的构造函数设为私有
    Singleton();
    Singleton(const Singleton& other);
public:
    static Singleton* getInstance();
    static Singleton* m_instance;
};

Singleton* Singleton::m_instance = nullptr;

//线程非安全版本
Singleton* Singleton::getInstance() {
    if (m_instance == nullptr) {
        m_instance = new Singleton()；
    }
    return m_instance;
}


//线程安全版本，但锁的代价太高：m_instance不为空的时候，对于都是**读操作的时候加锁是浪费**
Singleton* Singleton::getInstance() {
    Lock lock; //函数结束的时候释放锁
    if (m_instace == nullptr) {
        m_instance = new Singleton();
    }
    return m_instance;
}


//双检查锁，但由于内存读写reorder不安全
//所有的编译器都可能会出现reorder
Singleton* Singleton::getInstance() {
    if (m_instance == nullptr) { //减小了m_instance不为空时都是读取操作时候的加锁代价
        Lock lock;
        if (m_instance == nullptr) { //避免两个线程同时在m_instance为空时进来
            //常见顺序：1. 分配内存 2.调用构造器 3.内存地址返回
            //如果编译器reorder：1.分配内存 2.返回内存地址给m_instance 3.调用构造器。
            //如果threadA在还没有调用构造器的时候，threadB进来了，发现m_instance不为空，直接返回对象，此时的m_instance是不可用的，只是分配了一个原生内存，并没有执行构造器，对象的状态不对。double-check lock欺骗了threadB，threadB拿到的指针所指向的对象只有对象地址，而没有执行构造器，这就是双检查锁可能出现的问题。
            m_instance = new Singleton();
        }
    }
    return m_instance;
}


//C++ 11版本之后的跨平台实现 (volatile)
std::atomic<Singleton*> Singleton::m_instance;
std::mutex Singleton::m_mutex;

Singleton* Singleton::getInstance() {
    Singleton* tmp = m_instance.load(std::memory_order_relaxed);
    std::atomic_thread_fence(std::memory_order_acquire);//获取内存fence
    if (tmp == nullptr) {
        std::lock_guard<std::mutex> lock(m_mutex);
        tmp = m_instance.load(std::memory_order_relaxed);
        if (tmp == nullptr) {
            tmp = new Singleton; //保证了tmp不会出现reorder
            std::atomic_thread_fence(std::memory_order_release);//释放内存fence
            m_instance.store(tmp, std::memory_order_relaxed);
        }
    }
    return tmp;
}
```

### 7.2.3 模式定义

保证一个类仅有一个实例，并提供一个该实例的全局访问点。 ——《设计模式》GoF

### 7.2.4 结构

![](https://img-blog.csdnimg.cn/img_convert/2faa035ca3a90527e2b61477e75678e8.png)

### 7.2.5 要点总结

- `Singleton`模式中的实例构造器可以设置为`protected`以允许子类派生。
- `Singleton`模式一般不要支持拷贝构造函数和Clone接口，因为这有可能导致多个对象实例，与`Singleton`模式的初衷违背。
- 如何实现多线程环境下安全的`Singleton`？注意对双检查锁的正确实现。

## 7.3 Flyweight 享元模式

### 7.3.1 动机（Motivation）

在软件系统采用纯粹对象方案的问题在于大量细粒度的对象会很快充斥在系统中，从而带来很高的运行时代价——主要指内存需求方面的代价。
如何在避免大量细粒度对象问题的同时，让外部客户程序依然能够透明地使用面向对象的方式来进行操作？

### 7.3.2 代码示例

```c++
//flyweight.cpp
class Font {
private:
    //unique object key
    string key;
    
    //object state
    //...
public:
    Font(const string& key) {
        //...
    }
};

class FontFactory {
private:
    map<string, Font*> fontPool;
public:
    Font* GetFont(const string& key) {
        map<string, Font*>::iterator item = fontPool.find(key);
        
        if (item != fontPool.end()) {
            return fontPool[key];
        } else {
            Font* font = new Font(key);
            fontPool[key] = font;
            return font;
        }
    }
    
    void clear() {
        //...
    }
};
```

共享的方式：有就使用，没有就添加。

### 7.3.3 模式定义

> 运用共享技术有效地支持大量细粒度的对象。 ——《设计模式》GoF

### 7.3.4 结构

![](https://img-blog.csdnimg.cn/img_convert/1c970cfbbc94128ae1965a55820c0566.png)

### 7.3.5 要点总结

- 面向对象很好地解决了抽象性的问题，但是作为一个运行在机器中的程序实体，我们需要考虑对象的代价问题。Flyweight主要解决面向对象的代价问题，一般不触及面向对象的抽象性问题。
- Flyweight采用对象共享的做法来降低系统中对象的个数，从而降低细粒度对象给系统带来的内存压力。在具体实现方面，要注意对象状态的处理。
- 对象的数量太大从而导致对象内存开销加大——什么样的数量才算大？这需要我们仔细地根据具体应用情况进行评估，而不能凭空臆断。
