# 一、栈与队列基础

## 1. 栈与队列原理

栈先进后出，队列先进先出

![栈与队列基础](https://img-blog.csdnimg.cn/20210104235346563.png)

## 2.Java中的栈与队列的实现

> Java中栈的容器

**官方解释**

Java中原本存在stack类，但是现在已经不推荐使用，一般将`Deque`这个接口当作栈来使用，它实现的是一个双端队列,Java中常见的能用作栈和队列的类有：**LinkedList、ArrayDeque**

![Deque接口方法](https://img-blog.csdnimg.cn/20210320194639532.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQwMjgzMTc=,size_16,color_FFFFFF,t_70)

Queue 也是 Java 集合框架中定义的一种接口，直接继承自 Collection 接口。除了基本的 Collection 接口规定测操作外，Queue 接口还定义一组针对队列的特殊操作。通常来说，Queue 是按照先进先出(FIFO)的方式来管理其中的元素的，但是优先队列是一个例外。

Deque 接口继承自 Queue接口，但 Deque 支持同时从两端添加或移除元素，因此又被成为双端队列。鉴于此，Deque 接口的实现可以被当作 FIFO队列使用，也可以当作LIFO队列（栈）来使用。官方也是推荐使用 Deque 的实现来替代 Stack。

ArrayDeque 是 Deque 接口的一种具体实现，是依赖于可变数组来实现的。ArrayDeque 没有容量限制，可根据需求自动进行扩容。ArrayDeque不支持值为 null 的元素。

**三种基本定义方式**
- 普通队列
```java
Queue queue = new LinkedList();
```
- 双端队列

```java
Deque deque = new LinkedList(); 
```

- 栈

```java
Deque deque = new LinkedList(); 
```
> Java中的Deque内部实现

deque的元素数据采用分块的线性结构进行存储，如图所示。deque分成若干线性存储块，称为deque块。块的大小一般为512个字节，元素的数据类型所占用的字节数，决定了每个deque块可容纳的元素个数。

所有的deque块使用一个Map块进行管理，每个Map数据项记录各个deque块的首地址。Map是deque的中心部件，将先于deque块，依照deque元素的个数计算出deque块数，作为Map块的数据项数，创建出Map块。以后，每创建一个deque块，都将deque块的首地址存入Map的相应数据项中。

在Map和deque块的结构之下，deque使用了两个迭代器M_start和M_finish，对首个deque块和末deque块进行控制访问。迭代器iterator共有4个变量域，包括M_first、M_last、M_cur和M_node。M_node存放当前deque块的Map数据项地址，M_first和M_last分别存放该deque块的首尾元素的地址（M_last实际存放的是deque块的末尾字节的地址），M_cur则存放当前访问的deque双端队列的元素地址。

![Deque内部实现原理](http://hiphotos.baidu.com/hins_pan/pic/item/f1da993ec38686a87d1e71ab.jpg)

![Deque内部实现原理](http://hiphotos.baidu.com/hins_pan/pic/item/1a3f18fa18fc617c6d22eba1.jpg)

## Java中(Queue、Deque、Stack)的特点及遍历方式

总结 ：Queue以及Deque都是继承于Collection，Deque是Queue的子接口。

> **Queue**

**特点**

Queue是单端队列，遵循(FIFO)先进先出原则，最早进去的最先出来。

有限队列：有界限，大小长度受限制，常见实现类ArrayBlockingQueue；

无限队列：无界限大小限制，常见实现类LinkedList；

**遍历方式**
 
- 增强for循环
```java
		for (Object o : queue) {
			System.out.println(o);
		}
```
- Iterator迭代器
```java
		Iterator it = queue.iterator();
		while (it.hasNext()) {
			System.out.println(it.next());
		}
```
- while循环条件判断

```java
		while (!queue.isEmpty()) {
			System.out.println(queue.poll());
		}
```

> **Deque**

**遍历方式**

- 增强for循环
```java
		for (Object o : deque) {
			System.out.println(o);
		}
```

- Iterator迭代器

```java
  Iterator it = deque.iterator();
  while(it.hasNext()){
      System.out.println(it.next());
  }
```
- while循环条件判断

```java
    while(deque.pooLast() != null){
        System.out.println(deque.pollLast());
    }
    
    while(!deque.isEmpty()){
        System.out.println(deque.pollLast());
    }
```

> **Stack**

- 增强for循环

```java
		for(Object o : stack) {
			System.out.println(o);
		}
```

- while循环条件判断
```java
		while(!stack.isEmpty()) {
			System.out.println(stack.pop());
		}
```

- Iterator迭代器

```java
  Iterator it = stack.iterator();
  while(it.hasNext()){
      System.out.println(it.next());
  }
```
