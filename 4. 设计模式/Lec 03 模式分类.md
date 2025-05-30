# 三、模式的分类

## 3.1 GOF-23 模式分类

- 从**目的**来看：
  - 创建型（Creational）模式：将对象的部分创建工作延迟到子类或者其他对象，从而应对需求变化为**对象创建**时具体类型实现引来的冲击。
  - 结构型（Structural）模式：通过类继承或者对象组合获得更灵活的结构，从而应对需求变化为对象的结构带来的冲击。
  - 行为型（Behavioral）模式：通过类继承或者对象组合来划分类与对象间的职责，从而应对需求变化为多个交互的对象带来的冲击。
  
- 从**范围**来看：
  - **类模式**处理类与子类的静态关系。【注：偏重于继承方案】
  - **对象模式**处理对象间的动态关系。【注：偏重于组合方案】

## 3.2 从封装变化角度对模式分类

- 组件协作：
  - Template Method
  - Observer / Event
  - Strategy

- 单一职责：
  - Decorator
  - Bridge

- 对象创建:
  - Factory Method
  - Abstract Factory
  - Prototype
  - Builder

- 对象性能：
  - Singleton
  - Flyweight

- 接口隔离:
  - Façade
  - Proxy
  - Mediator
  - Adapter

- 状态变化：
  - Memento
  - State

- 数据结构：
  - Composite
  - Iterator
  - Chain of Resposibility
  
- 行为变化：
  - Command
  - Visitor

- 领域问题：
  - Interpreter

## 3.3 重构获得模式 Refactoring to Patterns

- 面向对象设计模式是“好的面向对象设计”，所谓“好的面向对象设计”指是那些可以满足“应对变化，提高复用”的设计。
  
- 现代软件设计的特征是“需求的频繁变化”。设计模式的要点是“**寻找变化点**，然后在变化点处应用设计模式，从而来更好地应对需求的变化”。”**什么时候、什么地点应用设计模式”比“理解设计模式结构本身**”更为重要。
  
- **设计模式的应用不宜先入为主**，一上来就使用设计模式是对设计模式的最大误用。没有一步到位的设计模式。敏捷软件开发实践提倡的“Refactoring to Patterns”是目前普遍公认的最好的使用设计模式的方法。

## 3.4 推荐图书

《重构-改善既有代码设计》
《重构与模式》

## 3.5 重构关键技法

从不同角度看待同一个问题

- 静态 -> 动态
- 早绑定 -> 晚绑定
- 继承 -> 组合
- 编译时依赖 -> 运行时依赖
- 紧耦合 -> 松耦合
