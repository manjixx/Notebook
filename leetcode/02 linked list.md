# 2. 链表

## 2.1 基础知识

### 1. 链表的类型

- 单链表

- 双链表

- 循环链表

### 2.链表的存储方式


### 3. 链表的定义

```java
class ListNode{
  int val;
  ListNode next;
  
  public ListNode(){
  
  }
  
  public ListNode(int val){
    this.val = val;
  }
  
  public ListNode(int val, ListNode next){
    this.val = val;
    this.next = next;
  }
}
```

### 4.链表操作

- 删除节点

- 添加节点

### 5.性能分析


## [2.2 移除链表元素](https://leetcode.cn/problems/remove-linked-list-elements/)
- 思路

- 代码
```java
class Solution{
    public ListNode removeElements(ListNode head, int val) {
      if(head == null){
          return null;
      }
      ListNode dummy = new ListNode(-1,head);
      ListNode pre = dummy; //注意
      ListNode node = head;
      
      while(node != null){
          if(node.val == val){
              pre.next = node.next;
          }else{
              pre = node;
          }
          ndoe = pre.next;
      }
      
        return dummy.next;
    }
}
```
- 复杂度分析
  - 时间复杂度：${O(n)}$ 
  - 空间复杂度：${O(1)}$  

## 2.3 设计链表

```java
class ListNode{
    int val;
    ListNode next;
    public ListNode(){};
    public ListNode(int val){
        this.val = val;
    };

    public ListNode(int val,ListNode next){
        this.val = val;
        this.next = next;
    };

}
class MyLinkedList {
    int size;
    ListNode head;

    public MyLinkedList() {
        size = 0;
        head = new ListNode(0);
    }
    
    public int get(int index) {
        if(index < 0 || index >= size){
            return -1;
        }
        
        ListNode dummy = head;
        
        for(int i = 0;i <= index;i++){
            dummy = dummy.next;
        }
        
        return dummy.val;        
    }
    
    public void addAtHead(int val) {
        addAtIndex(0,val);
        
    }
    
    public void addAtTail(int val) {
        addAtIndex(size,val);
        
    }
    
    public void addAtIndex(int index, int val) {
        if(index < 0 || index > size){
            return;
        }
        size++;
        
        ListNode dummy = head;
        
        for(int i = 0;i < index;i++){
            dummy = dummy.next;
        }
        
        ListNode node = new ListNode(val);
        node.next = dummy.next;
        dummy.next = node;
    }
    
    public void deleteAtIndex(int index) {
        if(index < 0 || index >= size){
            return;
        }
        size--;
        
        ListNode dummy = head;
        
        
        for(int i = 0;i < index;i++){
            dummy = dummy.next;
        }
        
        dummy.next = dummy.next.next;
        
    }
}

/**
 * Your MyLinkedList object will be instantiated and called as such:
 * MyLinkedList obj = new MyLinkedList();
 * int param_1 = obj.get(index);
 * obj.addAtHead(val);
 * obj.addAtTail(val);
 * obj.addAtIndex(index,val);
 * obj.deleteAtIndex(index);
 */
```


## 2.4 翻转链表

## 2.5 两两交换链表中的节点

## 2.6 删除链表的倒数第N个节点

## 2.7 链表相交

## 2.8 环形链表

