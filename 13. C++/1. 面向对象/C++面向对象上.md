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
private:
    double re, im;

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

operator overloading(操作符重载-1，成员函数) this
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-nG0pg0uM-1634388013107)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——操作符重载之成员函数.png?raw=true)]

return by reference语法分析
传递者无需知道接受者是以reference形式接收。
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-M8KAu1oQ-1634388013110)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——返回引用语法分析.png?raw=true)]

【注】return *ths; 接收端是complex&，不矛盾。

class body外的各种定义(definitions)
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

使用：

{
    complex c1(2,1);

    cout << imag(c1);
    cout << real(c1);
}

operator overloading(操作符重载-2，非成员函数)(无this)
为了应对client的三种可能用法，这儿对应开发三个函数。
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-9UXGdUtC-1634388013114)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——操作符重载之非成员函数.png?raw=true)]

temp object(临时对象) typename();
上图complex这些函数绝不可return by reference,因为它们返回的必定是个local object。

## 七、三大函数：拷贝构造，拷贝复制，析构

Class without pointer member(s)
complex
Class with pointer member(s)
string
String class
string-test.cpp

int main()
{
    String s1(),
    String s2("hello");

    String s3(s1);
    cout << s3 << endl;
    s3 = s2;
    cout << s3 << endl;
}

string.h

#ifndef __MYSTRING__
define __MYSTRING__

class String
{
    ...
};

String::function(...)   ...
Global-function(...)    ...

#endif

Big Three, 三个特殊函数
Big Three：拷贝构造、拷贝赋值、析构函数
【注】拷贝构造、拷贝赋值，在带有指针的情况下，不能用编译器自带的那一套，需要自己编写。

class String
{
public:
    String(const char* cstr = 0);
    String(const String& str);//拷贝构造
    String& operator=(const String& s);//操作符重载（拷贝赋值）
    ~String();//析构函数
    char* get_c_str() const { return m_data};//inline
private:
    char* m_data;
};
1

【注】类似于动态分配的方式，用指针指向字符串，而不要用数组。

ctor和dtor(构造函数和析构函数)
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
    delete[] m_data;
}


使用：

{
    String s1();
    String s2("hello");

    String* p = new String("hello");
    delete p;
}

【注】离开作用域（一对大括号）时，s1,s2自然而然调用析构函数，p手动调用析构函数。

class with pointer members 必须有 copy ctor 和 copy op=
copy ctor(拷贝构造)
copy op=(拷贝赋值)

e.g.
a有一个data，指向Hello\0
b有一个data，指向World\0

如果使用 default copy ctor 或 default op= 就会形成以下局面
b = a;
导致b的指针也指向Hello\0

而World\0造成memory leak（内存泄漏）
这种叫做浅拷贝

cpoy ctor(拷贝构造函数)
深拷贝

inline String::String(const String& str)
{
    m_data = new char[strlen(str.m_data)+1];
    strcpy(m_data, str.m_data);
}

使用：

{
    String s1("hello");
    String s2(s1);
//  String s2 = s1;
}

copy assignment operator(拷贝赋值函数)
【注】类比：原来有一个装水和油的瓶子。现在要赋值，步骤：

倒掉油（杀掉自己）
将瓶子改造成水瓶一样大（重新创造自己）
将水从水瓶倒入新瓶（拷贝过来）
inline String& String::operator=(const String&)
{
    if(this == &str)//检测自我赋值(self assignment)
        return *this;
    
    delete[] m_data;//杀掉自己
    m_data = new char[strlen(str.m_data) + 1];//重新创造自己
    strcpy(m_data, str.m_data);//拷贝过来
    return *this;  
}

使用：

{
    String s1("hello");
    String s2(s1);
    s2 = s1;
}


一定要在 operator= 中检查是否 self assignment
【注】这样做不仅是为了提高效率，不做还会影响正确性。

比如， this和rhs的指针指向同一片内存Hello\0
前述operator=的第一件事情就是delete，造成this和rhs指向？？？
然后，当企图存取（访问）rhs，产生不确定行为(undefined behavior)

output函数

#include <iostream.h>
ostream& operator<<(ostream& os, const String& str)
{
    os << str.get_c_str();
    return os;
}


使用：

{
    String s1("hello");
    cout << s1;
}

## 八、堆，栈与内存管理

所谓stack(栈)，所谓heap(堆)
Stack，是存在于某作用域(scope)的一块内存空间(memory space)。例如当你调用函数，函数本身即会形成一个stack用来放置它所接收的参数，以及返回地址。
在函数本体(function body)内声明的任何变量，其所使用的内存块都取自上述stack。

Heap，或谓system heap，是指由操作系统提供的一块global内存空间，程序可动态分配(dynamic allocated)从某中获得若干区块(blocks)。

class Complex{...};
...
{
    Complex c1(1, 2);
    Complex* p = new Complex(3);
}


c1所占用的空间来自stack
Complex(3)是个临时对象，其所占用的空间乃是以new自heap动态分配而得，并由p指向。

stack objects 的生命期
class Complex{...};
...
{
    Complex c1(1, 2);
}


c1便是所谓stack object，其生命在作用域(scope)结束之后结束。
这种作用域内的object，又称为auto object，因为它会被“自动”清理。

stack local objects 的生命期
class Complex{...};
...
{
    static Complex c2(1, 2);
}


c2便是所谓的static object，其生命在作用域(scope)结束之后仍然存在，直到整个程序结束。

global objects 的生命期
class Complex{...};
...
Complex c3(1, 2);

int main()
{
    ...
}


c3便是所谓global object，其生命在整个程序结束之后才结束。也可以把它视为一种static object，其作用域是“整个程序”。

heap objects 的生命期
class Complex{...};
...
{
    Complex* p = new Complex;
    ...
    delete p;
}


p所指的便是heap object，其生命在它被deleted之后结束。

class Complex{...};
...
{
    Complex* p = new Complex;
}


以上为内存泄漏(memory leak)，因为当作用域结束，p所指的heap object仍然存在，但指针p的生命却结束了，作用域之外再也看不到p（也就没机会delete p）。

new:先分配memory,再调用ctor
Complex* pc = new Complex(1, 2);
1
编译器转化为

Complex *pc;

void* mem = operator new(sizeof(Complex));//分配内存
pc = static_cast<Complex*>(mem);//转型
pc->Complex::Complex(1, 2);//构造函数


operator new是一个函数，其内部调用malloc(n)
构造函数的全名是

Complex::Complex(pc, 1 ,2);

pc即隐藏的参数this。

delete: 先调用dtor,再释放memory
Complex* ps = new Complex(1, 2);
...
delete ps;

编译器转化为

Complex::~Complex(ps);//析构函数
operator delete(ps);//释放内存

delete函数内部调用free(ps)

析构函数先删除内容，delete删除指针

动态分配所得的内存块(memory block),in VC
Complex大小为8b，调试模式下会增加灰色的内存块（32+4），并且收尾各有一个cookie（4*2）（用于回收）
vc每一块都是16的倍数，所以需要一些填补物(pad)

release下没有灰色部分

String大小为4b
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-RcR4ev1M-1634388013117)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——动态分配所得的内存块.png?raw=true)]

动态分配所得的array
vc用一个整数记录数组个数，所以+4
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-ZidxhGQN-1634388013119)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——动态分配所得的array.png?raw=true)]

array new一定要搭配array delete
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-Af7BeT5l-1634388013121)(https://raw.githubusercontent.com/hubojing/BlogImages/master/C%2B%2B%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E4%BE%AF%E6%8D%B7%EF%BC%89%E7%AC%94%E8%AE%B0%E2%80%94%E2%80%94array%20new%E4%B8%80%E5%AE%9A%E8%A6%81%E6%90%AD%E9%85%8Darray%20delete.png)]
【注】看清内存泄漏的地方。

## 十、扩展补充：类模板，函数模板及其他

static
静态函数和一般成员函数的区别：静态函数没有this pointer
静态函数只能处理静态数据

如设计银行户头的类

class Account
{
public:
    static double m_rate;//静态数据
    static void set_rate(const double& x){m_rate = x;}//静态函数
};
double Account::m_rate = 8.0;

int main()
{
    Account::set_rate(5.0);

    Account a;
    a.set_rate(7.0);
}

调用static函数的方式有二：
（1）通过object调用
（2）通过class name调用

把ctor放在private区
Singleton

class A
{
public:
    static A& getInstance{return a;};//取得唯一的自己
    setup(){...}
private:
    A();//任何人不能创建它
    A(const A& rhs);
    static A a;//已经创建了一份
    ...
};


使用：

A::getInstance().setup();
1
如果不用a，但a仍然存在，为避免资源浪费，更好的写法是：
Meyers Singleton

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


使用：

A::getInstance().setup();
1
cout
class _IO_ostream_withassign:public ostream{
    ...
};
extern _IO_ostream_withassign cout;


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


class template,类模板
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


使用：

{
    complex<double> c1(2.5, 1.5);
    complex<int> c2(2, 6);
    ...
}


function template, 函数模板
stone r1(2,3),r(3,3),r3;
r3 = min(r1, r2);


编译器会对function template进行引数推导(argument deduction)

template<class T>
inline const T& min(const T& a, const T& b)
{
    return b < a ? b : a;
}

引数推导的结果，T为stone，于是调用stone::operator<

class stone
{
public:
    stone(int w, int h, int we):_w(w), _h(h), _weight(we)
    {}
    bool operator< (const strone& rhs) const
    {return _weight < rhs._weight;}
private:
    int _w, _h, _weight;
};

namespace
namespace std
{
    ...
}

using directive

#include<iostream.h>
using namespace std;

int main()
{
    cin << ...;
    cout << ...;

    return 0;
}

using declaration

#include<iostream.h>
using std::cout;

int main()
{
    std::cin<<...;
    cout<<...;

    return 0;
}

#include<iostream.h>

int main()
{
    std::cin<<...;
    std::cout<<...;

    return 0;
}

更多细节与深入
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

## 十一、组合与继承

Object Oriented Programming, Object Oriented Design OOP, OOD
Inheritance(继承)
Composition(复合)
Delegation(委托)
Compostion(复合)，表示has-a
Adapter

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


从内存角度看

template <class T>
class queue
{
protected:
    deque<T> c;
...
};
1

Sizeof: 40

template <class T>
class deque
{
protected:
    Itr<T> start;
    Itr<T> finish;
    T** map;
    unsigned int map_size;
};

Sizeof: 16 * 2 + 4 + 4

template <class T>
struct Itr
{
    T* cur;
    T* first;
    T* last;
    T** node;
...
};

Sizeof: 4*4

Composition(复合)关系下的构造和析构
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-FfzqBLZg-1634388013123)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——复合关系下的构造和析构.png?raw=true)]
构造由内而外
Container的构造函数首先调用Component的default构造函数，然后才执行自己。

Container::Container(...):Component(){...};

析构由外而内
Container的析构函数首先执行自己，然后才调用Component的析构函数。

Container:~Container(...){... ~Component()};

Delegation(委托). Composition by reference.
Handle/Body(pImpl)

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

//file String.cpp
#include "String.hpp"
namespace
{
class StringRep
{
friend class String;
    StringRep(const char* s);
    ~StringRep();
    int count;
    char* rep;
};
}

String::String(){...}
...


这种手法可称为编译防火墙
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-jdvEXkFA-1634388013129)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——引用计数.png?raw=true)]
n=3
共享同一个Hello，节省内存。
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-AquVjEl4-1634388013130)(https://raw.githubusercontent.com/hubojing/BlogImages/master/C%2B%2B%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E4%BE%AF%E6%8D%B7%EF%BC%89%E7%AC%94%E8%AE%B0%E2%80%94%E2%80%94%E5%A7%94%E6%89%98%20%E5%9B%BE.png)]

Inheritance(继承), 表示is-a
struct _List_node_base
{
    _List_node_base* _M_next;
    _List_node_base* _M_prev;
};

template<typename _Tp>
struct _List_node:public _List_node_base
{
    _Tp _M_data;
};

[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-HGNlGZxN-1634388013133)(https://raw.githubusercontent.com/hubojing/BlogImages/master/C%2B%2B%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%EF%BC%88%E4%BE%AF%E6%8D%B7%EF%BC%89%E7%AC%94%E8%AE%B0%E2%80%94%E2%80%94%E7%BB%A7%E6%89%BF%20%E5%9B%BE.png)]

Inheritance(继承)关系下的构造和析构
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-9vJeNqG4-1634388013135)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——继承关系下的构造和析构.png?raw=true)]

base class的dtor必须是virtual，否则会出现undefined behavior

构造由内而外
Derived的构造函数首先调用Base的default构造函数，然后才执行自己。

Derived::Derived(...):Base(){...};
1
析构由外而内
Derived的析构函数首先执行自己，然后才调用Base的析构函数。

Derived::~Derived(...){...~Base()};
1
Inheritance(继承) with virtual functions(虚函数)
non-virtual函数：不希望derived class重新定义(override,复写)它。
virtual函数：希望derived class重新定义(override，复写)它，它已有默认定义。
pure virtual函数：希望derived class一定要重新定义(override)它，对它没有默认定义。

【注】：纯虚函数其实可以有定义，只是本文不提及。

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

Template Method


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
        Serialize();
        cout << "close file..." << endl;
        cout << "update all views..." << endl;
    }

    virtual void Serialize()  {};
};


class CMyDoc : public CDocument
{
public:
    virtual void Serialize()
    {
        //只有应用程序本身才知道如何读取自己的文件（格式）
        cout << "CMyDoc::Serialize()" << endl;
    }
};

int main()
{
    CMyDoc myDoc;//假设对应[File/open]
    myDoc.OnFileOpen();
}

Inheritance + Composition关系下的构造和析构
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-kh9PcCZ7-1634388013137)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——继承+复合.png?raw=true)]

第一个问号：

第二个问号：构造函数调用顺序：Component, Base , Derived
析构函数则相反。

Delegation(委托) + Inheritance(继承)
Observer

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

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
class Observer
{
public:
    virtual void update(Subject* sub, int value) = 0;
};
1
2
3
4
5
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-elGo2yrc-1634388013140)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——委托+继承.png?raw=true)]

Composite
[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-wjsbbVAA-1634388013144)(https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——Composite.png?raw=true)]

class Primitive:public Component
{
public:
    Primitive(int val):Component(val) {}
};
1
2
3
4
5
class Component
{
    int value;
public:
    Component(int val) { value = val; }
    virtual void add(Component*) {}
};
1
2
3
4
5
6
7
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

**Prototype**
![Prototype](https://github.com/hubojing/BlogImages/blob/master/C++面向对象程序设计（侯捷）笔记——Prototype.png?raw=true)
出自Design Patterns Explained Simply

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

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
//Client calls this public static member function when it needs an instance 
Image *Image::findAndClone(imageType type)
{
    for(int i = 0; i < _nextSlot; i++)
    {
        if(_prototypes[i]->returnType())
        return _prototypes[i]->clone();
    }
}
1
2
3
4
5
6
7
8
9
子类

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
    the default ctor to be called, which registers the subclass's prototype
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
ypes[_nextSlot++] = image;
    }
private:
    //addPrototype() saves each registered prototype here
    static Image* _prototypes[10];
    static int _nextSlot;
};
Image *Image::prototypes[];//定义
int Image::_nextSlot;//定义

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
//Client calls this public static member function when it needs an instance 
Image *Image::findAndClone(imageType type)
{
    for(int i = 0; i < _nextSlot; i++)
    {
        if(_prototypes[i]->returnType())
        return _prototypes[i]->clone();
    }
}


子类

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
    the default ctor to be called, which registers the subclass's prototype
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
