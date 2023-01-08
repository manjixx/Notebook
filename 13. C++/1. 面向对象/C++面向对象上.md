# C++面向对象上

## 一、C++编程简介

> **基础**

- 曾学过某种`procedural language`(C语言)
  - 变量(`variables`)
  - 类型(`types`):`int, float, char, struct …`
  - 作用域(`scope`)
  - 循环(`loops`):`while, for`
  - 流程控制：`if-else, switch-case`
- 知道一个程序需要编译、连结才能被执行
- 知道如何编译和连结（如何建立一个可运行程序）

> **目标**

- 培养正规的、大气的编程习惯
- 以良好的方式编写`C++ class`(`Object Based`-基于对象)
  - `class without pointer members – Complex`
  - `class with pointer members – String`
- 学习Classes之间的关系(`Objected Oriented`-面向对象)
  - 继承（`inheritance`）
  - 复合（`composition`）
  - 委托（`delegation`）

> **示例代码**

- class without pointer members
  - complex.h
  - complex-test.cpp

- class with pointer members
  - string.h
  - string-test.cpp

- 综合
  - oop-demo.h
  - oop-test.cpp

> **C++的历史**

- B语言（1969）
- C语言（1972）
- C++语言（1983）： (new C -> C with Class ->C++)
- Java语言
- C#语言

> **C++演化**

- C++ 98(1.0)
- C++ 03(TR1, Technical Report 1)
- C++ 11(2.0)
- C++ 14
- C++:C++语言、C++标准库

> **Bibliography(书目志)**

- 《C++ Primer》
- 《The C++ PROGRAMMING LANGUAGE》
- 《Effective C++》
- 《THE C++ STANDARD LIBRARY》
- 《STL源码剖析》

## 二、头文件与类的声明

> **C vs C++ —— 数据和函数**

- c++: class,struct

![](https://github.com/hubojing/BlogImages/blob/9d26e12a3e8f9bb1b75015884287637c9af86692/C++%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E4%BE%AF%E6%8D%B7%EF%BC%89%E7%AC%94%E8%AE%B0%E2%80%94%E2%80%94C%20vs%20C++.png?raw=true)

- C++ 关于数据和函数
  - class without pointer 
  - class with pointer

![](https://github.com/hubojing/BlogImages/blob/master/C++%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E4%BE%AF%E6%8D%B7%EF%BC%89%E7%AC%94%E8%AE%B0%E2%80%94%E2%80%94C++,%E5%85%B3%E4%BA%8E%E6%95%B0%E6%8D%AE%E5%92%8C%E5%87%BD%E6%95%B0.png?raw=true)

```c++
complex c1(2,1);
complex c2;
complex* pc = new complex(0,1);
```

```c++
string s1("Hello");
string s2("World");
string* ps = new string;
```

> **Object Based(基于对象) vs Object Oriented(面向对象)**

- 基于对象(`Object Based`) ：面向的是单一`class`的设计
- 面向对象（`Object Oriented`)：面对的是多重`classes`的设计，`classes`和`classes`之间的关系。

- Classes的两个经典分类：
  - Class without pointer member(s)
complex
  - Class with pointer member(s)
string

> **`C++ programs`代码基本形式**

![](https://github.com/hubojing/BlogImages/blob/master/C++%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E4%BE%AF%E6%8D%B7%EF%BC%89%E7%AC%94%E8%AE%B0%E2%80%94%E2%80%94C++%E4%BB%A3%E7%A0%81%E5%9F%BA%E6%9C%AC%E5%BD%A2%E5%BC%8F.png?raw=true)

- 延伸文件名（`extension file name`）不一定是`.h`或`.cpp`，也可能是`.hpp`或其他或甚至无延伸名。
- 引用标准库使用`<>`，引用自己写的头文件使用`" "`

> **Output, C++ vs. C**

- C++

```c++
#include <iostream> // c++输出标准库
using namespace std;

int main()
{
    int i = 7;
    cout<< "i=" << i << endl;

    return 0;
}
```

- C

```c
include <stdio.h> // c语言输出标准库

int main()
{
    int i = 7;
    printf("i=%d \n", i);

    return 0;
}
```

> **Header(头文件)中的防卫式声明**

**guard(防卫式声明)代码如下：**

```h
/*complex.h */

#ifndef __COMPLEX__
#define __COMPLEX__

...

#endif
```

【注】如果xxx未经定义，则对其进行编译，否则不进行相应定义。

```c
/** complex-test.h */
#include <iostream>
#include "complex.h" // 上文自己定义的头文件
using namespace std;

int main()
{
    complex c1(2,1);
    complex c2;
    cout << c1 << endl;
    cout << c2 << endl;

    c2 = c1 + 5;
    c2 = 7 + c1;
    c2 = c1 + c2;
    c2 += c1;
    c2 += 3;
    c2 = -c1;

    cout << (c1 == c2) << endl;
    cout << (c1 != c2) << endl;
    cout << conj(c1) << endl;
    return 0;
}
```

> **Header(头文件)的布局**

```c++
#ifndef __COMPLEX__
#define __COMPLEX__

#include<cmath>

/*
0:forward declarations(前置声明)
*/
class ostream;
class complex;

complex&
    __doapl (complex* ths, const complex& r);

/*
1:class declarations(类-声明)
*/
class complex
{
    ...
};

/*
2:class definiton(类-定义)
*/

complex::function ...

#endif
```

> **class的声明(declaration)**

```c++
class complex   //class head
{
//class body
public:
    complex (double r = 0, double i = 0)
    : re (r), im(i)
    {}
    complex& operator += (const complex&);
    double real () const {return re;}
    double imag () const {reutn im;}//有些函数在此直接定义，另一些在body之外定义
private:
    double re, im;  // data

    friend complex& __doapl (complex*, const complex&);
};
```

使用：

```c++
{
    complex c1(2,1);
    complex c2;
    ...
}
```

> **`class template`(模板)简介**

抽出数据

```c++
template<typename T>
class complex
{
public:
    complex (T r = 0, T i = 0)
    : re (r), im(i)
    {}
    complex& operator += (const complex&);
    T real () const {return re;}
    T imag () const {reutn im;}//有些函数在此直接定义，另一些在body之外定义
private:
    T re, im;

    friend complex& __doapl (complex*, const complex&);
};
```

使用：类型绑定

```c++
{
    complex<double> c1(2.5,1.5);
    complex<int> c2(2,6);
    ...
}
```

## 三、构造函数

> **inline(内联)函数**

函数若在`class body`内定义完成，便成为`inline`候选人

`inline`只是程序员对编译器的建议而已，是否真正编译为`inline`函数取决于编译器。

```c++
class complex
{
public:
    complex (double r = 0, double i = 0)
    : re (r), im(i)
    {}//函数若在class body内定义完成，便成为inline候选人
    complex& operator += (const complex&);
    double real () const {return re;}//可以inline
    double imag () const {reutn im;}//可以inline
private:
    double re, im;

    friend complex& __doapl (complex*, const complex&);
};
```

使用：

```c++
inline double
imag(const complex& x)
{
    return x.imag ();
}
```

【注】函数太复杂，就不能inline。

> **access level(访问级别)**

- public
- private
- protected

```c++
class complex
{
public:
    complex (double r = 0, double i = 0)
    : re (r), im(i)
    {}
    complex& operator += (const complex&);
    double real () const {return re;}
    double imag () const {reutn im;}
private:
    double re, im;

    friend complex& __doapl (complex*, const complex&);
};
```

**错误使用：**

```c++
{
    complex c1(2,1);
    cout << c1.re;
    cout << c1.im;
}
```

**正确使用：**

```c++
{
    complex c1(2,1);
    cout << c1.real();
    cout << c1.imag();
}
```

> **constructor(ctor,构造函数)**

- 构造函数名称一定与类名称相同
- 构造函数可以拥有参数，构造函数的参数可以有默认值，（其他函数也可以有默认值）
- 没有返回值类型

```c++
class complex
{
public:
    complex (double r = 0, double i = 0)//default argument(默认实参)
    : re (r), im(i)//initialization list(初值列，初始列)
    { }
    complex& operator += (const complex&);
    double real () const {return re;}
    double imag () const {reutn im;}
private:  re, im;

    friend complex& __doapl (complex*, const complex&);
};
```

【注】构造函数没有返回值类型。`initialization list`(初值列，初始列)形式初始列的三行等价于

```c++
complex (double r = 0, double i = 0)
{
    re = r; im = i;
}
```

但建议用初始列方式写，该种方式效率相对高一点 。初始化+赋值。初始列就是初始化的阶段。

**使用：**

```c++
{
    complex c1(2,1);
    complex c2;//没有指明，用默认值
    complex* p = new complex(4);    // 使用动态的方式
}
```

【注】**不带指针的类多半不用写析构函数**。

> **ctor(构造函数)可以有很多个 - overloading(重载)**

```c++
class complex
{
public:
    /**构造函数1 */
    complex (double r = 0, double i = 0)
    : re (r), im(i)
    { }
    /**构造函数2 ❌*/
    complex () : re(0), im(0) { } 

    complex& operator += (const complex&);
    double real () const {return re;}
    double imag () const {reutn im;}
private:
    double re, im;

    friend complex& __doapl (complex*, const complex&);
};


void real(double r){ re = r;}

```

重载表面名字相同，其实在编译器内名字不同。real函数编译后的实际名称可能如下所示：

```
?real@Complex@@QBENXZ
?real@Complex@@QAENABN@Z
```

**构造函数重载：** 构造函数2不能这样重载。

```c++
{
    Complex c1;
    Complex c2();//写法不同，意思相同
}
```

## 四、参数传递与返回值

> **constructor(ctor,构造函数)被放在private区**

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——ctor被放在private区.png?raw=true)

以下无法使用：

```c++
complex c1(2,1);
complex c2;
```

那么是不是说ctor不应该放在private区呢？也不是。

**构造函数放在private区域，Singleton(单例)设计模式：**

```c++
class A
{
public:
    static A& getInstance();
    setup() {...}
private:
    A();
    A(const A& rhs);
    ...
};

A& A::getInstance()
{
    static A a;
    return a;
}
```

**使用：**

```c++
A::getInstance().setup();
```

> **const member functions(常量成员函数)**

```c++
class complex
{
public:
    complex (double r = 0, double i = 0)
    : re (r), im(i)
    { }
    complex& operator += (const complex&);
    double real () const {return re;}
    double imag () const {reutn im;}
private:
    double re, im;

    friend complex& __doapl (complex*, const complex&);
};
```

**正确使用：**

```c++
{
    complex c1(2,1);
    cout << c1.real();
    cout << c1.imag();
}
```

【注】数据不需要改变就加const。

？！

```c++
{
    const complex c1(2,1);  // 这个值是不能改变的哦
    cout << c1.real();      // 万一real函数没写const，就可能改data。就会产生矛盾
    cout << c2.imag();
}
```

> **参数传递：pass by value vs. pass by reference (to const)**

```c++
class complex
{
public:
    complex (double r = 0, double i = 0)
    : re (r), im(i)
    { }
    complex& operator += (const complex&);// pass by reference 传引用速度很快哦，并且不能改我，我加了const哦。如果你改我，编译器就会报错
    double real () const {return re;}
    double imag () const {reutn im;}
private:
    double re, im;

    friend complex& __doapl (complex*, const complex&);
};
```

没有const:

```c++
ostream&
operator << (ostream& os, const complex& x)
{
    return os << '(' << real (x) << ','
              << imag (x) << ')';
}
```

- `pass by value`压到栈里。大的遵循守则，尽量不要`pass by value`。
- 在C里用指针。C++ `pass by reference`，尽量`pass by reference`。
- 如果不希望对方改数据，加const。

**使用：**

```c++
{
    complex c1(2,1);
    complex c2;

    c2 += c1;
    cout << c2;
}
```

> **返回值传递：return by value vs. return by reference(to const)**

返回值的传递也尽量使用`return by reference`

```c++
class complex
{
public:
    complex (double r = 0, double i = 0)
    : re (r), im(i)
    { }
    /*return by reference */
    complex& operator += (const complex&);
    /*return by value */
    double real () const {return re;}
    double imag () const {reutn im;}
private:
    double re, im;

    friend complex& __doapl (complex*, const complex&);
};
```

> **friend(友元)**

**friend打破封装，我们不希望外界获得`data`，但希望指定群体可以取得`data`**

```c++
class complex
{
public:
    complex (double r = 0, double i = 0)
    : re (r), im(i)
    { }
    complex& operator += (const complex&);
    double real () const {return re;}
    double imag () const {reutn im;}
private:
    double re, im;

    friend complex& __doapl (complex*, const complex&);
};
```

使用：

```c++
inline complex& __doapl (complex* ths, const complex& r)
{
    this->re += r.re;
    this->im += r.im;//自由取得friend的private成员
    return *ths;
}
```

> **相同class的各个objects互为friends(友元)**

```c++
class complex
{
public:
    complex (double r = 0; double i = 0)
    : re (r), im (i)
    { }

    /** 
    这个怎么可以直接拿咧~
    相同class的各个objects互为friends(友元)
    */
    int func(const complex& param)
    { return param.re + param.im; }

private:
    double re, im;
};
```

使用：

```c++
{
    complex c1(2,1);
    complex c2;

    c2.func(c1);
}
```

> **`class body`外的各种定义(`definitions`)**

- data 尽量使用private
- 参数值尽量使用`pass by reference`
- 返回值尽量使用`return by reference`
- 构造函数尽量使用`initialization list`

什么情况下可以`pass by reference`

什么情况下不可以`return by reference`:

- 函数内的操作需要放到一个新的对象内，因为此时新对象为local变量，因此此时无法 `return by reference`
-  

```c++
/** 

do assignment plus

*/

inline complex&
__doapl (complex* ths, const complex& r)
{
    ths->re += r.re;    // 第一参数将会被改动
    ths->im += r.im;    // 第二参数不会被改动
    return *ths;
}

inline complex&
complex::operator += (const complex& r)
{
    return __doapl (this, r);
}
```

## 五、操作符重载与临时对象

C++里操作符本质上是一种函数

> **operator overloading(操作符重载-1，成员函数) this**

所有成员函数都带一个隐藏的参数，即字符本身用`this`表示

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——操作符重载之成员函数.png?raw=true)

> **`return by reference`语法分析**

传递者无需知道接收者是以reference形式接收。

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——返回引用语法分析.png?raw=true)

右下角框框里的代码使得我们设计类的时返回值可以是`void`，右方框里的连加表达式则使得返回值不能是`void`。？

【注】`return *ths`; 接收端是`complex&`，不矛盾。

> **class body外的各种定义(definitions)**

```c++
inline double
imag(const complex& x)
{
    return x.imag ();
}

inline double
real(const complex& x)
{
    return x.real ();
}
```

**使用：**

```c++
{
    complex c1(2,1);

    cout << imag(c1);
    cout << real(c1);
}
```

> **operator overloading(操作符重载-2，非成员函数)(无this)**

为了应对`client`的三种可能用法，对应开发三个函数。

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——操作符重载之非成员函数.png?raw=true)

上图`complex`这些函数绝不可`return by reference`,因为它们返回的必定是个`local object`。

> **temp object(临时对象): typename()**

```c++
inline complex
operator + (const complex& x, const complex& y){
    return complex(real(x) + real(y),imag(x) + imag(y));// 临时对象
}

inline complex
operator + (const complex& x, const complex& y){
    return complex(real(x) + y,imag(x));
}
inline complex
operator + (const complex& x, const complex& y){
    return complex(x + real(y), imag(y));
}
```

```c++
int(7); // 临时对象

complex c1(2,1);
complex c2;
complex();
complex(4,5);
cout << complex(2); 
```

> **`class body`之外的各种定义(definitions)**

这个函数绝对不能`retrun by reference`，因为其返回的必定是`local object` 。

```c++
inline complex
operator + (const complex& x){
    return x;
}

inline complex
operator - (const complex& x){
    return complex(-real(x), -imag(x));
}
```

```c++
complex c1(2,1)
complex c2;
cout << -c1;
cout << +c1
```

## 六、复习Complex类的实现

参考库文件`complex.h`和`complex__test.class`

## 七、三大函数：拷贝构造，拷贝复制，析构

- Class without pointer member(s)：complex
- Class with pointer member(s)：string

> **String class**

如果编写类的时候没有写拷贝构造与拷贝赋值函数，那么编译器会自动提供。

complex类因为没有指针，使用编译器提供的拷贝构造与拷贝赋值函数即可完成实部与虚部的复制；
String类因为使用指针，使用编译器提供的拷贝构造与拷贝赋值函数只会拷贝指针，而无法拷贝String。

如果类中带指针，因此一定要自己写拷贝构造与拷贝赋值函数。

- string-test.cpp

```c++
int main()
{
    String s1(),
    String s2("hello");

    String s3(s1);  // 拷贝构造 clone s1
    cout << s3 << endl;

    s3 = s2;    // 拷贝赋值
    cout << s3 << endl;
}
```

- string.h

```c++
#ifndef __MYSTRING__
define __MYSTRING__

class String
{
    ...
};

String::function(...)   ...
Global-function(...)    ...

#endif
```

> **Big Three, 三个特殊函数**

Big Three：拷贝构造、拷贝赋值、析构函数
【注】拷贝构造、拷贝赋值，在带有指针的情况下，不能用编译器自带的那一套，需要自己编写。

因为String长度无法确定，所以data处应该设计为指针。

```c++
class String
{
public:
    String(const char* cstr = 0);       //构造函数
    String(const String& str);          //拷贝构造
    String& operator=(const String& s); //操作符重载（拷贝赋值）
    ~String();                          //析构函数，对象死亡时回调用该函数
    char* get_c_str() const { return m_data};//inline，注意这里的const
private:
    char* m_data;
};
```

【注】类似于动态分配的方式，用指针指向字符串，而不要用数组。

> **ctor和dtor(构造函数 和 析构函数)**

```c++
inline String::String(const char* cstr = 0)
{
    if(cstr)
    {
        m_data = new char[strlen(cstr)+1];
        strcpy(m_data, cstr);
    }
    else
    {//未指定初值
        m_data = new char[1];
        *m_data = '\0';
    }
}

inline String::~String()
{
    delete[] m_data;    // 如果没有delet将导致内存泄漏
}
```

使用：

```c++
{
    /**
    离开作用域（一对大括号）时，s1,s2自然而然调用析构函数，p手动调用析构函数。
     */
    String s1();
    String s2("hello");
    // 动态创建
    String* p = new String("hello");
    delete p;
}
```

> **copy ctor(拷贝构造) 和 copy op=(拷贝赋值)**

copy ctor(拷贝构造)
copy op=(拷贝赋值)

- **e.g.浅拷贝**
    a为一个指针data，指向`Hello\0`
    b为一个指针data，指向`World\0`

    如果使用 `default copy ctor` 或 `default op=` 就会形成以下局面`b = a;`
    导致b的指针也指向`Hello\0`

    而`World\0`造成`memory leak（内存泄漏）`

> **cpoy ctor(拷贝构造函数)**

**深拷贝：**

```c++
/**2-2 */
inline String::String(const String& str)    // 传进来的值不会被更改因此需要加 const
{
    m_data = new char[strlen(str.m_data)+1];    // 直接取另一个object的private data，兄弟间互为friend。
    strcpy(m_data, str.m_data);
}
```

使用：

```c++
{
    String s1("hello");
    String s2(s1);
//  String s2 = s1;
}
```

> **copy assignment operator(拷贝赋值函数)**

【注】类比：原来有一个装水和油的瓶子。现在要赋值，步骤：

- 倒掉油（杀掉自己）
- 将瓶子改造成水瓶一样大（重新创造自己）
- 将水从水瓶倒入新瓶（拷贝过来）

```c++
inline String& String::operator=(const String&)
{
    if(this == &str)//检测自我赋值(self assignment)
        return *this;
    
    delete[] m_data;//杀掉自己
    m_data = new char[strlen(str.m_data) + 1];//重新创造自己
    strcpy(m_data, str.m_data);//拷贝过来
    return *this;  
}
```

使用：

```c++
{
    String s1("hello");
    String s2(s1);
    s2 = s1;
}
```

一定要在 `operator=` 中检查是否是**自我赋值**`self assignment`

- 【注】这样做不仅是为了提高效率，不做还会影响正确性。比如， `this`和`rhs`的指针指向同一片内存`Hello\0`。前述`operator=`的第一件事情就是`delete`，造成`this`和`rhs`指向`？？？`。然后，当企图存取（访问）`rhs`，产生不确定行为(`undefined behavior`)

> **output函数**

不能写成成员函数，一定要是全局函数。

```c++
#include <iostream.h>
ostream& operator<<(ostream& os, const String& str)
{
    os << str.get_c_str();
    return os;
}
```

使用：

```c++
{
    String s1("hello");
    cout << s1;
}
```

## 八、堆，栈与内存管理

> **stack(栈) 和heap(堆)**

**Stack**，是存在于某作用域(`scope`)的一块内存空间(`memory space`)。例如当你调用函数，函数本身即会形成一个stack用来放置它所接收的参数，以及返回地址。**在函数本体(`function body`)内声明的任何变量，其所使用的内存块都取自上述`stack`。**

**Heap**，或谓`system heap`，是指由操作系统提供的一块`global`内存空间，程序可动态分配(`dynamic allocated`)从某中获得若干区块(`blocks`)。

```c++
class Complex{...};
...
{
    Complex c1(1, 2);       // c1所占用的空间来自stack
    // Complex(3)是个临时对象，其所占用的空间乃是以new自heap动态分配而得，并由p指向。
    Complex* p = new Complex(3);
}
```

> **`stack objects` 的生命期**

```c++
class Complex{...};
...
{
    Complex c1(1, 2);
}
```

c1便是所谓`stack object`，其生命在作用域(`scope`)结束之后结束。
这种作用域内的`object`，又称为`auto object`，因为它会被“自动”清理。

> **`staic local objects` 的生命期**

```c++
class Complex{...};
...
{
    static Complex c2(1, 2);
}
```

`c2`便是所谓的`static object`，其生命在作用域(`scope`)结束之后仍然存在，直到整个程序结束。

> **`global objects` 的生命期**

```c++
class Complex{...};
...
Complex c3(1, 2);

int main()
{
    ...
}
```

`c3`便是所谓`global object`，其**生命在整个程序结束之后才结束**。也可以把它视为一种`static object`，其作用域是“整个程序”。

> **`heap objects` 的生命期**

```c++
class Complex{...};
...
{
    Complex* p = new Complex;
    ...
    delete p;
}
```

`p`所指的便是`heap object`，其生命在它被`deleted`之后结束。

```cpp
class Complex{...};
...
{
    Complex* p = new Complex;
}
```

以上为内存泄漏(`memory leak`)，因为当作用域结束，`p`所指的`heap object`仍然存在，但指针`p`的生命却结束了，作用域之外再也看不到`p`（也就没机会`delete p`）。

> **new:先分配memory,再调用ctor**

```c++
Complex* pc = new Complex(1, 2);
```

上述代码被编译器转化为：

```c++
Complex *pc;

void* mem = operator new(sizeof(Complex));  //1.分配内存
pc = static_cast<Complex*>(mem);            //2.转型
pc->Complex::Complex(1, 2);                 //3.构造函数
```

**第一步**：`operator new`是一个函数，其内部调用`malloc(n)`

**第二步**： 指针类型转换

**第三步**： 调用构造函数，构造函数的全名如下

```c++
pc -> Complex::Complex(pc, 1 ,2); // pc即隐藏的参数this。
```

> **delete: 先调用dtor,再释放memory**

- Copmlex类

```cpp
Complex* ps = new Complex(1, 2);
...
delete ps;
```

上述代码被编译器转化为

```cpp
Complex::~Complex(ps);  //1. 析构函数
operator delete(ps);    //2. 释放内存
```

- String 类

```cpp
String* ps = new String("Hello");
...
delete ps;
```

上述代码被编译器转换为

```cpp
String::~String(ps);      // 1.析构函数
operator delete(ps);      // 2.释放内存
```

**第一步：** 调用析构函数

对于`Complex`类，调用的是编译器提供的析构函数，未进行任何操作

而对于`String`类，需要自己实现析构函数，我们自己编写的析构函数进行了如下操作

```cpp
Class String
{
public:
    ~String(){
        delete[] m_data;
    }
    ...
private:
    char* m_data;
};
```

**第二步：** 释放内存，`delete`函数内部调用`free(ps)`

析构函数负责先删除内容，`delete`删除指针

> **动态分配所得的内存块(`memory block`),in VC**

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——动态分配所得的内存块.png?raw=true)

- `Complex`
  - **非调试模式下（左2列）**：`Complex`大小为`8`，首尾各有一个`cookie`**（4*2）**（用于告诉回收时内存大小），共计 **16**。release下没有灰色部分。
  
  - **调试模式下（左1列）**：调试模式下会增加灰色的内存块 **（32+4）**，并且收尾各有一个`cookie` **（4*2）**（用于告诉回收时内存大小），**共计 52**。由于vc编译器下内存分配都是16的倍数，所以需要一些填补物(pad)，**填充之后共计 64。**

- `String`
  - **非调试模式下（右1列）**：`String`大小为`4`，首尾各有一个`cookie`**（4*2）**（用于告诉回收时内存大小），共计 **12**。由于vc编译器下内存分配都是16的倍数，所以需要一些填补物(pad)，**填充之后共计 16。**
  
  - **调试模式下（右2列）**：调试模式下会增加灰色的内存块 **（32+4）**，并且收尾各有一个`cookie`**（4*2）**（用于告诉回收时内存大小），**共计 48**。

> **动态分配所得的`array`,`array new`**

vc编译器用一个整数记录数组个数，所以最后`+4`

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——动态分配所得的array.png?raw=true)

> **`array new`一定要搭配`array delete`**

![](https://raw.githubusercontent.com/hubojing/BlogImages/master/C%2B%2B%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E4%BE%AF%E6%8D%B7%EF%BC%89%E7%AC%94%E8%AE%B0%E2%80%94%E2%80%94array%20new%E4%B8%80%E5%AE%9A%E8%A6%81%E6%90%AD%E9%85%8Darray%20delete.png)

【注】

- 看清内存泄漏的地方。
- `Complex`类由于是`class without point`，`array new` 可以跟`delete`搭配使用，但是以防万一，需要养成良好的编程习惯，**`array new`一定要搭配`array delete`**。

## 九、复习String类的实现过程

参考文件`String.h`和`String-test.class`

```cpp
#ifndef __MYSTRING__
define __MYSTRING__

class String
{
public:
    String(const char* cstr = 0);       //构造函数
    String(const String& str);          //拷贝构造
    String& operator=(const String& s); //操作符重载（拷贝赋值）
    ~String();                          //析构函数，对象死亡时回调用该函数
    char* get_c_str() const { return m_data};//inline，注意这里的const
private:
    char* m_data;
};

// 构造函数
inline String::String(const char* cstr = 0)
{
    if(cstr)
    {
        m_data = new char[strlen(cstr)+1];
        strcpy(m_data, cstr);
    }
    else
    {//未指定初值
        m_data = new char[1];
        *m_data = '\0';
    }
}

// 析构函数
inline String::~String()
{
    delete[] m_data;    // 如果没有delet将导致内存泄漏
}

// 拷贝构造函数
inline String::String(const String& str)    // 传进来的值不会被更改因此需要加 const
{
    m_data = new char[strlen(str.m_data)+1];    // 直接取另一个object的private data，兄弟间互为friend。
    strcpy(m_data, str.m_data);
}

// 拷贝赋值函数
inline String& String::operator=(const String&)
{
    if(this == &str)//检测自我赋值(self assignment)
        return *this;
    
    delete[] m_data;//杀掉自己
    m_data = new char[strlen(str.m_data) + 1];//重新创造自己
    strcpy(m_data, str.m_data);//拷贝过来
    return *this;  
}

// 输出函数 
#include <iostream.h>
ostream& operator<<(ostream& os, const String& str)
{
    os << str.get_c_str();
    return os;
}
#endif

```

【注】：

- type&：表示reference
- &object： 表示取地址，得到一个指针

## 十、扩展补充：类模板，函数模板及其他

> **static**

**静态函数：**

- 静态函数和一般成员函数的区别：静态函数没有this pointer
- 静态函数只能处理静态数据

如设计银行户头的类

```c++
class Account
{
public:
    static double m_rate;//静态数据
    static void set_rate(const double& x){m_rate = x;}//静态函数
};
double Account::m_rate = 8.0;

int main()
{
    Account::set_rate(5.0); // 通过class name调用static函数

    Account a;
    a.set_rate(7.0);    // 通过class name调用static函数
}
```

调用static函数的方式有二：

- （1）通过object调用
- （2）通过class name调用

> **把ctor放在private区**

**Singleton**

```c++
class A
{
public:
    static A& getInstance{return a;};// 对外界唯一的接口，取得唯一的自己
    setup(){...}
private:
    A();                //任何人不能创建它
    A(const A& rhs);
    static A a;         //已经创建了一份
    ...
};
```

使用：

```c++
A::getInstance().setup();
```

如果不用a，但a仍然存在，为避免资源浪费。

更好的写法如下。

**Meyers Singleton**

```c++
class A
{
public:
    static A& getInstance();
    setup() {...}
private:
    A();
    A(const A& rhs);
    ...
};

A& A::getInstance()
{
    static A a;
    return a;
}
```

使用：

```c++
A::getInstance().setup();
```

> **cout**

```c++

class _IO_ostream_withassign:public ostream{
    ...
};
extern _IO_ostream_withassign cout;
```

```cpp
class ostream:virtual public ios
{
public:
    ostream& operator<<(char c);
    ostream& operator<<(unsigned char c){return (*this)<<(char)c;}
    ostream& operator<<(signed char c){return (*this)<<(char)c;}
    ostream& operator<<(const char *s);
    ostream& operator<<(const unsigned char *s)
    {return (*this) << (const char*)s;}
    ostream& operator<<(const signed char *s)
    {reutrn (*this) << (const char*)s;}
    ostream& operator<<(const void *p);
    ostream& operator<<(int n);
    ostream& operator<<(unsigned int n);
    ostream& operator<<(long n);
    ostream& operator<<(unsigned long n);
    ...
};
```

> **class template,类模板**

类型不写死，用符号T告诉编译器，现在类型不确定后续添加。

```c++
template<typename T>
class complex
{
public:
    complex(T r = 0, T i = 0):re(r), im(i)
    {}
    complex& operator += (const complex)
    T real() const {return re;}
    T imag() const {return im;}
private:
    T re, im;

    friend complex& __doapl(complex*, const complex&);
};
```

使用：

```c++
{
    complex<double> c1(2.5, 1.5);
    complex<int> c2(2, 6);
    ...
}
```

> **function template, 函数模板**

```c++
stone r1(2,3),r(3,3),r3;
r3 = min(r1, r2);
```

编译器会对`function template`进行引数推导(`argument deduction`)

```c++
template <class T>       // T未定
inline const T& min(const T& a, const T& b)
{
    return b < a ? b : a;
}
```

引数推导的结果，`T`为`stone`，于是进行**操作符重载**，调用`stone::operator <`

```c++
class stone
{
public:
    stone(int w, int h, int we):_w(w), _h(h), _weight(we)
    {}
    // 操作符重载
    bool operator< (const strone& rhs) const
    {return _weight < rhs._weight;}
private:
    int _w, _h, _weight;
};
```

> **namespace**

```cpp
namespace std
{
    ...
}
```

```cpp
/** 
using directive 全开
*/

#include<iostream.h>
using namespace std;

int main()
{
    cin << ...;
    cout << ...;

    return 0;
}
```

```cpp

/*
    using declaration
    一行一行引入
*/
#include<iostream.h>
using std::cout;

int main()
{
    std::cin<<...;
    cout<<...;

    return 0;
}
```

```cpp
#include<iostream.h>

int main()
{
    std::cin<<...;
    std::cout<<...;

    return 0;
}
```

> **更多细节与深入**

```cpp
operator type() const;
*explicit complex(…):initialization list{}
pointer-like object
funtion-like object
Namespace
template specialization
Standard Library
variadic template(since C++11)
move ctor(since C++11)
Rvalue reference(since C++11)
auto(since C++11)
lambda(since C++11)
range-base for loop(since C++11)
unordered containers(since C++ 11)
…
```

## 十一、组合与继承

> **Object Oriented Programming, Object Oriented Design OOP, OOD**

`complex`类的实现-基于对象设计OOD

面向对象的设计OOP：

- Inheritance(继承)
- Composition(复合)
- Delegation(委托)

> **Compostion(复合)，表示`has-a`**

`queue`里边有一个`deque`,`has-a`的关系
二者生命周期是一致的

这里涉及到`Adapter`设计模式

```c++
template <class T, class Sequence = deque<T>>
class queue
{
    ...
protected:
    Sequence c;//底层容器
public:
    //以下完全利用c的操作函数完成
    bool empty() const {return c.empty();}
    size_type size() const {return c.size();}
    reference front() {return c.front();}
    reference back() {return c.back();}
    //deque是两端可进出，queue是末端进前端出（先进先出）
    void push(const value_type& x) {c.push_back(x);}
    void pop() {c.pop_front();}
};
```

从内存角度看

```c++
/**
    Sizeof: 40 
*/
template <class T>
class queue
{
protected:
    deque<T> c;
...
};
```

```c++
/**
    Sizeof: 16 * 2 + 4 + 4
 */
template <class T>
class deque
{
protected:
    Itr<T> start;
    Itr<T> finish;
    T** map;
    unsigned int map_size;
};
```

```cpp
/**
Sizeof: 4*4
 */

template <class T>
struct Itr
{
    T* cur;
    T* first;
    T* last;
    T** node;
...
};
```

**Composition(复合)关系下的构造和析构**

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——复合关系下的构造和析构.png?raw=true)

- 左边拥有右边

- **构造由内而外：** `Container`的构造函数首先调用`Component`的`default`构造函数，然后才执行自己。

```c++
Container::Container(...):Component(){...};
```

- **析构由外而内：** `Container`的析构函数首先执行自己，然后才调用`Component`的析构函数。

```c++
Container:~Container(...){... ~Component()};
```

> **Delegation(委托). Composition by reference.**

通过指针相连，二者生命周期不同步，StringRep* 先创建出来等其需要动作时，才去调用StringRep

这种手法可称为编译防火墙

Handle/Body(pImpl)

```c++
/**
Handle
*/
//file String.hpp
class StringRep;
class String
{
public:
    String();
    String(const char* s);
    String(const String& s);
    String &operator=(const String& s);
    ~String();
...
private:
    StringRep* rep;//pimpl
};
```

```cpp
/**
Body(pImpl)
*/
//file String.cpp
#include "String.hpp"
namespace{
class StringRep{
friend class String;
    StringRep(const char* s);
    ~StringRep();
    int count;
    char* rep;
};
}

String::String(){...}
...
 ```

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——引用计数.png?raw=true)

`n=3`共享同一个Hello，节省内存。涉及copy or write

![](https://raw.githubusercontent.com/hubojing/BlogImages/master/C%2B%2B%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E4%BE%AF%E6%8D%B7%EF%BC%89%E7%AC%94%E8%AE%B0%E2%80%94%E2%80%94%E5%A7%94%E6%89%98%20%E5%9B%BE.png)

> **Inheritance(继承), 表示is-a**

```c++
struct _List_node_base
{
    _List_node_base* _M_next;
    _List_node_base* _M_prev;
};

template<typename _Tp>
struct _List_node
    :public _List_node_base //继承
{
    _Tp _M_data;
};
 ```

`c++`里继承有：`public、private、protected`三种

父类的数据被子类完整继承。

![](https://raw.githubusercontent.com/hubojing/BlogImages/master/C%2B%2B%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E4%BE%AF%E6%8D%B7%EF%BC%89%E7%AC%94%E8%AE%B0%E2%80%94%E2%80%94%E7%BB%A7%E6%89%BF%20%E5%9B%BE.png)

> **Inheritance(继承)关系下的构造和析构**

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——继承关系下的构造和析构.png?raw=true)

`base class`的`dtor`必须是`virtual`，否则会出现`undefined behavior`

- **构造由内而外**：子类`Derived`的构造函数首先调用父类`Base`的`default`构造函数，然后才执行自己。

```cpp
Derived::Derived(...):Base(){...};
```

- **析构由外而内**：子类`Derived`的析构函数首先执行自己，然后才调用父类`Base`的析构函数。

```cpp
Derived::~Derived(...){...~Base()};
```

> **Inheritance(继承) with virtual functions(虚函数)**

继承搭配虚函数使用

- `non-virtual`函数：不希望子类`derived class`重新定义(`override`,复写)它。
- `virtual`函数：希望`derived class`重新定义(`override`，复写)它，它已有默认定义。
- `pure virtual`函数：希望`derived class`一定要重新定义(`override`)它，对它没有默认定义。

【注】：纯虚函数其实可以有定义，只是本文不提及。

```c++
class Shape
{
public:
    virtual void draw() const = 0;//pure virtual
    virtual void error(const std::string& msg);//impure virtual
    int objectID() const;//non-virtual
    ...
};

class Rectangle:public Shape {...};
class Ellipse:public Shape {...};
```

- **`Template Method`**

```c++
/**Application FrameWork */

#include <iostream>
using namespace std;

class CDocument
{
public:
    void OnFileOpen()
    {
        //这是个算法，每个cout输出代表一个实际动作
        cout << "dialog..." << endl;
        cout << "check file status..." << endl;
        cout << "open file..." << endl;
        // 关键动作延缓到子类中去实现，让子类实现该虚函数
        Serialize();
        cout << "close file..." << endl;
        cout << "update all views..." << endl;
    }

    virtual void Serialize()  {};
};
```

```cpp
/** Application */
class CMyDoc : public CDocument
{
public:
    virtual void Serialize()
    {
        //只有应用程序本身才知道如何读取自己的文件（格式）
        cout << "CMyDoc::Serialize()" << endl;
    }
};
```

```cpp
int main()
{
    CMyDoc myDoc;//假设对应[File/open]
    // 子类对象调用父类的函数
    myDoc.OnFileOpen();
    // CDoucument::OnFileOpen(&myDoc);
}
```

> **Inheritance + Composition关系下的构造和析构**

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——继承+复合.png?raw=true)

**第一个问号**：课堂作业

**第二个问号**：

- **构造函数调用顺序**：Component, Base , Derived
- **析构函数**则相反。

> **Delegation(委托) + Inheritance(继承)**

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——委托+继承.png?raw=true)

Observer-观察者模式

```c++
class Subject
{
    int m_value;
    vector<Observer*> m_views;
public:
    void attach(Observer* obs)
    {
        m_views.push_back(obs);
    }
    void set_val(int value)
    {
        m_value = value;
        notify();
    }
    void notify()
    {
        for(int i = 0; i < m_views.size(); ++i)
            m_views[i]->update(this, m_value);
    }
};
```

```c++
class Observer
{
public:
    virtual void update(Subject* sub, int value) = 0;
};
```

> **Composite** 委托+继承

![](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——Composite.png?raw=true)

```c++
class Primitive:public Component
{
public:
    Primitive(int val):Component(val) {}
};
```

```c++
class Component
{
    int value;
public:
    Component(int val) { value = val; }
    virtual void add(Component*) {}
};
```

```c++
class Composite:public Component
{
    vector<Component*>c;
public:
    Composite(int val):Component(val) {}

    void add(Component* elem)
    {
        c.push_back(elem);
    }
...
};
```

> **Prototype，委托+继承**

树状继承器，想要创建未来才会出现的子类。即预先设计框架，而子类未来才会派生。

解决方案，子类自己创建一个自己的对象，然后告诉父类有子类对象的存在。

![Prototype](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——Prototype.png?raw=true)

出自Design Patterns Explained Simply

**父类：**

```cpp
#include<iostream.h>
enum imageType
{
    LSAT, SPOT
};
class Image
{
public:
    virtual void draw() = 0;
    static Image *findAndClone(imageType);
protected:
    virtual imageType returnType() = 0;
    virtual Image* clone() = 0;
    //As each subclass of Image is declared, it registers its prototype
    static void addPrototype(Image *image)
    {
        _prototypes[_nextSlot++] = image;
    }
private:
    //addPrototype() saves each registered prototype here
    static Image* _prototypes[10];
    static int _nextSlot;
};
Image *Image::prototypes[];//定义
int Image::_nextSlot;//定义
```

```cpp
//Client calls this public static member function when it needs an instance 
Image *Image::findAndClone(imageType type)
{
    for(int i = 0; i < _nextSlot; i++)
    {
        if(_prototypes[i]->returnType())
        return _prototypes[i]->clone();
    }
}
```

**子类：**

```cpp
class LandSatImage:public Image
{
public:
    imageType returnType()
    {
        return LSAT;
    }
    void draw()
    {
        cout << "LandSatImage::draw" << _id << endl;
    }
    //When clone() is called, call the one-argument with a dummy arg
    Image *clone()
    {
        return new LandSatImage(1); 
    }
protected:
    //This is only called from clone()
    LandSatImage(int dummy)
    {
        _id = _count++;
    }
private:
    //Mechanism for initializing an Image subclass - this causes
    //the default ctor to be called, which registers the subclass's prototype
    static LandSatImage _landSatImage;
    //This is only called when the private static data member is inited
    LandSatImage()
    {
        addPrototype(this);
    }
    //Nominal "state" per instance mechanism
    int _id;
    static int _count;
};
//Register the subclass's prototype
LandSatImage LandSatImage::_landSatImage;
//Initialize the "state" per instance mechanism
int LandSatImage::_count = 1;
```

**子类：**

```cpp
class SpotImage:public Image
{
public:
    imageType returnType()
    {
        return SPOT;
    }
    void draw()
    {
        cout << "SpotImage::draw" << _id << endl;
    }
    //When clone() is called, call the one-argument with a dummy arg
    Image *clone()
    {
        return new SpotImage(1); 
    }
protected:
    //This is only called from clone()
    SpotImage(int dummy)
    {
        _id = _count++;
    }
private:
    //Mechanism for initializing an Image subclass - this causes
    //the default ctor to be called, which registers the subclass's prototype
    static SpotImage _spotImage;
    //This is only called when the private static data member is inited
    SpotImage()
    {
        addPrototype(this);
    }
    //Nominal "state" per instance mechanism
    int _id;
    static int _count;
};
```