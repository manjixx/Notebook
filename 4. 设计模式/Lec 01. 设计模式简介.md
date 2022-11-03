# 设计模式简介

## 课程目标

- 理解松耦合设计思想
- 掌握面向对象设计原则
- 掌握重构技法改善设计
- 掌握GOF核心设计模式

## 什么是设计模式

“每个模式描述了一个在我们周围不断重复发生以及该问题的解决方案的核心。这样，你就能一次又一次地使用该方案而不必做重复劳动。”

教材：《设计模式：可复用面向对象软件的基础》

## 从面向对象谈起

面向对象底层包含两层思维模型：

- 底层思维：向下，如何把握机器底层从微观理解对象构造
  - 语言构造
  - 编译转换
  - 内存模型
  - 运行时机制
- 抽象思维：向上，如何将我嗯周围的世界抽象为程序代码
  - 面向对象
  - 组件封装
  - 设计模式
  - 架构模式

## 深入理解面向对象

- 向下：深入理解三大面向对象机制
  - 封装，隐藏内部实现
  - 继承，复用现有代码
  - 多态，改写对象行为

- 向上：深刻把握面向对象机制所带来的抽象意义，理解如何使用这些机制来表达现实世界，掌握什么是“好的面向对象设计”

## 软件设计固有的复杂性

软件设计复杂的根本原因：**变化**。

## 如何解决复杂性

- 分解：人们面对复杂性有一个常见的做法：即分而治之，将大问题化解为多个小问题，将复杂问题分解为多个简单问题
- 抽象：更高层次来讲，人们处理复杂性有一个通用技术，即抽象。由于不能掌握全部的复杂对象，我们选择忽视它的非本质细节，而去处理泛化和理想化的对象模型。

## 1.9 结构化 VS. 面向对象

- 代码中注释了“改变/增加”的是有新需求的情况设计到要修改的代码。
- 分解的做法不容易复用，而抽象的设计方法的代码复用非常高，能够使用通用的方法统一处理。

> 分解：伪代码

```c++
//Shape1.h
class Point {
public:
    int x;
    int y;
};

class Line {
public:
    Point start;
    Point end;

    Line(const Point& start, const Point& end) {
        this->start = start;
        this->end = end;
    }
};

class Rect {
public:
    Point leftUp;
    int width;
    int height;

    Rect(const Point& leftUp, int width, int height) {
        this->leftUp = leftUp;
        this->width = width;
        this->height = height;
    }
};

//增加
class Circle{
 
 
};
```

```c++
//MainForm1.cpp
class MainForm : public Form {
private:
    Point p1;
    Point p2;
 
    vector<Line> lineVector;
    vector<Rect> rectVector;
    //改变
    vector<Circle> circleVector;
 
public:
    MainForm(){
        //...
    }
protected:
 
    virtual void OnMouseDown(const MouseEventArgs& e);
    virtual void OnMouseUp(const MouseEventArgs& e);
    virtual void OnPaint(const PaintEventArgs& e);
};
 
 
void MainForm::OnMouseDown(const MouseEventArgs& e){
    p1.x = e.X;
    p1.y = e.Y;
 
    //...
    Form::OnMouseDown(e);
}
 
void MainForm::OnMouseUp(const MouseEventArgs& e){
    p2.x = e.X;
    p2.y = e.Y;
 
    if (rdoLine.Checked){
        Line line(p1, p2);
        lineVector.push_back(line);
    }
    else if (rdoRect.Checked){
        int width = abs(p2.x - p1.x);
        int height = abs(p2.y - p1.y);
        Rect rect(p1, width, height);
        rectVector.push_back(rect);
    }
    //改变
    else if (...){
        //...
        circleVector.push_back(circle);
    }
 
    //...
    this->Refresh();
 
    Form::OnMouseUp(e);
}
 
void MainForm::OnPaint(const PaintEventArgs& e){
 
    //针对直线
    for (int i = 0; i < lineVector.size(); i++){
        e.Graphics.DrawLine(Pens.Red,
            lineVector[i].start.x, 
            lineVector[i].start.y,
            lineVector[i].end.x,
            lineVector[i].end.y);
    }
 
    //针对矩形
    for (int i = 0; i < rectVector.size(); i++){
        e.Graphics.DrawRectangle(Pens.Red,
            rectVector[i].leftUp,
            rectVector[i].width,
            rectVector[i].height);
    }
 
    //改变
    //针对圆形
    for (int i = 0; i < circleVector.size(); i++){
        e.Graphics.DrawCircle(Pens.Red,
            circleVector[i]);
    }
 
    //...
    Form::OnPaint(e);
}

```

> **抽象：** 伪代码

```c++
//MainForm1.cpp
class MainForm : public Form {
private:
    Point p1;
    Point p2;
 
    vector<Line> lineVector;
    vector<Rect> rectVector;
    //改变
    vector<Circle> circleVector;
 
public:
    MainForm(){
        //...
    }
protected:
 
    virtual void OnMouseDown(const MouseEventArgs& e);
    virtual void OnMouseUp(const MouseEventArgs& e);
    virtual void OnPaint(const PaintEventArgs& e);
};
 
 
void MainForm::OnMouseDown(const MouseEventArgs& e){
    p1.x = e.X;
    p1.y = e.Y;
 
    //...
    Form::OnMouseDown(e);
}
 
void MainForm::OnMouseUp(const MouseEventArgs& e){
    p2.x = e.X;
    p2.y = e.Y;
 
    if (rdoLine.Checked){
        Line line(p1, p2);
        lineVector.push_back(line);
    }
    else if (rdoRect.Checked){
        int width = abs(p2.x - p1.x);
        int height = abs(p2.y - p1.y);
        Rect rect(p1, width, height);
        rectVector.push_back(rect);
    }
    //改变
    else if (...){
        //...
        circleVector.push_back(circle);
    }
 
    //...
    this->Refresh();
 
    Form::OnMouseUp(e);
}
 
void MainForm::OnPaint(const PaintEventArgs& e){
 
    //针对直线
    for (int i = 0; i < lineVector.size(); i++){
        e.Graphics.DrawLine(Pens.Red,
            lineVector[i].start.x, 
            lineVector[i].start.y,
            lineVector[i].end.x,
            lineVector[i].end.y);
    }
 
    //针对矩形
    for (int i = 0; i < rectVector.size(); i++){
        e.Graphics.DrawRectangle(Pens.Red,
            rectVector[i].leftUp,
            rectVector[i].width,
            rectVector[i].height);
    }
 
    //改变
    //针对圆形
    for (int i = 0; i < circleVector.size(); i++){
        e.Graphics.DrawCircle(Pens.Red,
            circleVector[i]);
    }
 
    //...
    Form::OnPaint(e);
}
```

```c++
//MainForm2.cpp
class MainForm : public Form {
private:
    Point p1;
    Point p2;
 
    //针对所有形状
    vector<Shape*> shapeVector; //此处必须要放Shape*指针，保证多态性
 
public:
    MainForm(){
        //...
    }
protected:
 
    virtual void OnMouseDown(const MouseEventArgs& e);
    virtual void OnMouseUp(const MouseEventArgs& e);
    virtual void OnPaint(const PaintEventArgs& e);
};
 
 
void MainForm::OnMouseDown(const MouseEventArgs& e){
    p1.x = e.X;
    p1.y = e.Y;
 
    //...
    Form::OnMouseDown(e);
}
 
void MainForm::OnMouseUp(const MouseEventArgs& e){
    p2.x = e.X;
    p2.y = e.Y;
 
    if (rdoLine.Checked){
        shapeVector.push_back(new Line(p1,p2));
    }
    else if (rdoRect.Checked){
        int width = abs(p2.x - p1.x);
        int height = abs(p2.y - p1.y);
        shapeVector.push_back(new Rect(p1, width, height));
    }
    //改变
    else if (...){
        //...
        shapeVector.push_back(circle);
    }
 
    //...
    this->Refresh();
 
    Form::OnMouseUp(e);
}
 
void MainForm::OnPaint(const PaintEventArgs& e){
 
    //针对所有形状
    for (int i = 0; i < shapeVector.size(); i++){
 
        shapeVector[i]->Draw(e.Graphics); //多态调用，各负其责
    }
 
    //...
    Form::OnPaint(e);
}
```

## 1.10 软件设计目标

什么是好的软件设计？软件设计的金科玉律：**复用！**
