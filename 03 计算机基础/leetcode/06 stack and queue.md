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

## 3.Java中(Queue、Deque、Stack)的特点及遍历方式

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

*** 

# 二、 用栈实现队列

> **思路**

> **代码**

> **复杂度分析**

*** 

#  三、用队列实现栈

> **思路**
**原始思路**
用两个队列que1和que2实现队列的功能，que2其实完全就是一个备份的作用，
把que1最后面的元素以外的元素都备份到que2，
然后弹出最后面的元素，再把其他元素从que2导回que1

**优化思路**
一个队列在模拟栈弹出元素的时候只要将队列头部的元素（除了最后一个元素外） 重新添加到队列尾部，此时在去弹出元素就是栈的顺序了。

> **代码**

```java
class MyStack {

    Deque<Integer> queue1 = new ArrayDeque<Integer>();
    // Deque<Integer> queue2 = new ArrayDeque<Integer>();

    public MyStack() {

    }
    
    public void push(int x) {
        queue1.addLast(x);
    }
    
    public int pop() {
        int size = queue1.size();
        size--;
        while(size-- > 0){
            // queue2.addLast(queue1.peekFirst());
            // queue1.pollFirst();
            queue1.addLast(queue1.pollFirst());
        }
        int ans = queue1.pollFirst();

        return ans;
    }
    
    public int top() {
        return queue1.peekLast();
    }
    
    public boolean empty() {
        if(queue1.size() == 0){
            return true;
        }
        return false;
    }
}

/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack obj = new MyStack();
 * obj.push(x);
 * int param_2 = obj.pop();
 * int param_3 = obj.top();
 * boolean param_4 = obj.empty();
 */

```

> **复杂度分析**

- 时间复杂度:入栈操作 O(n)，其余操作都是 O(1)，其中 nn 是栈内的元素个数。
- 空间复杂度:O(n)，其中 n 是栈内的元素个数。需要使用两个队列存储栈内的元素。

*** 

# 四、[有效的括号](https://leetcode.cn/problems/valid-parentheses/)

**括号匹配是使用栈解决的经典问题。**

> **思路**

- 构造栈，遍历所给字符串，如果遇到右括号则入栈

- 如果遇到左括弧则分为如下几种情况
  
  - 如果栈为空，或者栈中右括弧与遇到的左括弧对应的右括弧不匹配 则返回false
  
  -  如果栈中的右括弧与遇到的字符串中的左括弧匹配则移除 

> **代码**

```java
class Solution {

    /**
        哈希表+栈
        将左括弧逐个压入栈，遇到右括弧时判断栈是否为空以及栈顶是否为匹配的右括弧
            if(stack.isEmpty() || map.get(右括弧) ！= stack.pop()){
                return false;
            }
    */
    public boolean isValid(String s) {
        if(s.length() % 2 != 0){
            return false;
        }
        Map<Character,Character> map = new HashMap<Character,Character>();
        map.put(')','(');
        map.put('}','{');
        map.put(']','[');

        Deque<Character> stack = new LinkedList<Character>();

        for(int i = 0;i < s.length();i++){
            Character ch = s.charAt(i);
            if(map.containsKey(ch)){
                if(stack.isEmpty() || stack.peek() != map.get(ch)){
                    return false;
                }else{
                    stack.pop();
                }
            }else{
                stack.push(ch);
            }
        }
        return stack.isEmpty();
    }
}
```

> **复杂度分析**

- 时间复杂度:O(n);
- 空间负责度:O(n+∣Σ∣)，其中Σ 表示字符集，本题中字符串只包含 6 种括号，∣Σ∣=6。栈中的字符数量为 O(n)，而哈希表使用的空间为 O(∣Σ∣)，相加即可得到总空间复杂度

***

# 五、[删除字符串中所有相邻的重复元素](https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/submissions/)

## 5.1 思路一

> **思路**

可以把字符串顺序放到一个栈中，然后如果相同的话栈就弹出，这样最后栈里剩下的元素都是相邻不相同的元素了。

> **代码**

```java
class Solution {
    public String removeDuplicates(String s) {
        Deque<Character> stack = new ArrayDeque<Character>();

        for(int i = 0;i < s.length();i++){
            char ch = s.charAt(i);
            if(stack.isEmpty() || stack.peek() != ch){
                stack.push(ch);
            }else{
                stack.pop();
            }
        }
        String ans = "";
        while(!stack.isEmpty()){
           ans = stack.pop() + ans;
        }
        return ans;

    }
}
```

> **复杂度分析**

- 空间复杂度:O(n);
- 时间复杂度:O(n) 或 O(1)，取决于使用的语言提供的字符串类是否提供了类似「入栈」和「出栈」的接口。注意返回值不计入空间复杂度。

## 5.2 思路二：双指针

```java
class Solution {
    public String removeDuplicates(String s) {
        char[] ch = s.toCharArray();
        int fast = 0;
        int slow = 0;
        while(fast < s.length()){
            // 直接用fast指针覆盖slow指针的值
            ch[slow] = ch[fast];
            // 遇到前后相同值的，就跳过，即slow指针后退一步，下次循环就可以直接被覆盖掉了
            if(slow > 0 && ch[slow] == ch[slow - 1]){
                slow--;
            }else{
                slow++;
            }
            fast++;
        }
        return new String(ch,0,slow);
    }
}
```

***

# 六、[逆波兰表达式求值](https://leetcode.cn/problems/evaluate-reverse-polish-notation/)

> **思路**

从左到右遍历数组

- 如果遇到运算符，则取出栈顶的两个元素，并做相应的运算，将结果压入栈，注意数字的顺序，后出栈的数字应该位于运算符前边；
  
- 如果遇到数字，则将数字压入栈即可。

![思路](https://code-thinking.cdn.bcebos.com/gifs/150.%E9%80%86%E6%B3%A2%E5%85%B0%E8%A1%A8%E8%BE%BE%E5%BC%8F%E6%B1%82%E5%80%BC.gif)

> **代码**

```java
class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<Integer>();

        for(int i = 0;i < tokens.length;i++){
            String ch = tokens[i];
            if( ch.equals("+")){
                stack.push(stack.pop() + stack.pop());
            }else if(ch.equals("-")){
                stack.push(-stack.pop() + stack.pop());
            }else if(ch.equals("*")){
                stack.push(stack.pop() * stack.pop());
            }else if(ch.equals("/")){
                int temp1 = stack.pop();
                int temp2 = stack.pop();
                stack.push(temp2 / temp1);
            }else{
                stack.push(Integer.valueOf(ch));
            }
        }
        return stack.pop();
    }
}
```

> 复杂度分析

- 空间复杂度:O(n);
- 时间复杂度:O(n);

