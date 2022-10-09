# Day01 整数

+ 一般要计算位的问题最好都用位运算，位运算比加减乘除好像快一点，算是一种优化
+ 只不过字符串如果是数字类型的问题的话，最好先转换成数组（快），或者直接两个指针（容易出错）。不要修改字符串本身,字符串在内存中通常都是以constant存储的，如果直接修改字符串意味着每次都要生成新的constant。转换成数组的话可以用栈的库函数操作

## 1 整数除法

给定两个整数 a 和 b ，求它们的除法的商 a/b ，要求不得使用乘号 '*'、除号 '/' 以及求余符号 '%' 。

+ 溢出与边界情况
  + 当被除数为 32 位有符号整数的最小值-2^31时
  + 当除数为32位有符号整数的最小值-2^31时；
  + 当被除数为0时；

+ 因为负数最小取值为-2^31 - 1.因此可有考虑将被除数与除数全部转化为负数进行计算

+ 【题解】类二分法
  + 首先将Y不断乘以2(通过加法运算实现)，并将结果放入数组中，其中数组的第i项为（Y *2<sup>i</sup>)。这一过程直到(Y* 2<sup>i</sup>) 严格小于X为止；

  + 对数组进行逆序遍历。当遍历到第 i 项时，如果其大于等于 X，我们就将答案增加 2^i ，并且将 X 中减去这一项的值。

```java
class Solution {
    public int divide(int a, int b) {
        //被除数为0
        if(a == 0) return 0;

        //被除数为整数的最小值 -2^31
        if(a == Integer.MIN_VALUE){
            if(b == -1) return Integer.MAX_VALUE;
            if(b == 1) return Integer.MIN_VALUE;
        }

        // 被除数为整数的最大值 2^31
        if(b == Integer.MIN_VALUE){
            if(a == Integer.MIN_VALUE ) return 1;
            else return 0;
        }

        //处理符号 true:-1 false:1
        boolean sign = false;
        if(a > 0){
            a = -a;
            sign = !sign;
        }

        if(b > 0){
            b = -b;
            sign = !sign;
        }
        
        List<Integer> candidates = new ArrayList<Integer>();
        candidates.add(b);
        int index = 0;
        
        //注意溢出
        while(candidates.get(index) >= a - candidates.get(index)){
            candidates.add(candidates.get(index) + candidates.get(index));
            ++ index;
        }

        System.out.println(index);
        int ans = 0;
        for(int i = candidates.size() - 1; i >= 0;--i){
            if(candidates.get(i) >= a){
                ans+= 1<<i;
                a =  a - candidates.get(i);
            }
        }
        return sign ? -ans : ans;
    }
}
```

## 2 二进制加法

+ 两数相加问题中关键是：进位问题，每一位的结果都等于：两个加数的对应位加上进位
+ 十进制中“逢十进一”，二进制中“逢二进一”
+ 十进制中 每一位答案 = (carry + a + b) mod 10； 下一位进位= （carry + a + b）/10
+ 二进制中 每一位答案 = (carry + a + b) mod 2； 下一位进位= （carry + a + b）/2

 ```java
 class Solution {
    public String addBinary(String a, String b) {
        StringBuffer ans = new StringBuffer();

        int n = Math.max(a.length(), b.length()), carry = 0;
        for (int i = 0; i < n; ++i) {
            carry += i < a.length() ? (a.charAt(a.length() - 1 - i) - '0') : 0;
            carry += i < b.length() ? (b.charAt(b.length() - 1 - i) - '0') : 0;
            ans.append((char) (carry % 2 + '0'));
            carry /= 2;
        }

        if (carry > 0) {
            ans.append('1');
        }
        ans.reverse();

        return ans.toString();
    }
}

 ```

## 前 n 个数字二进制中 1 的个数

 给定一个非负整数 n ，请计算 0 到 n 之间的每个数字的二进制表示中 1 的个数，并输出一个数组。

+ 然后求数字中的1的个数的基本套路是，每个数字跟1相与（可以得到这个数字的最后一位是否是1），然后把这个数字右移一位

【题解】动态规划最低有效位

+ 偶数末尾为0，因此 bits[x] = bits[x/2] = bits[x >> 1]
+ 奇数末尾为1，因此 bits[x] = bits[x/2] + 1 = bits[x >> 1] + 1, 其中1可视为x除以2的余数，即 x & 1；
+ 基于上述思想可以得到：

  ```java
    bits[x] = bits[x >> 1] + (x & 1);
  ```

 ```java
 class Solution {
    public int[] countBits(int n) {
        int[] bits = new int[n + 1];
        for(int i = 0;i <= n;i++){
            bits[i] = bits[i >> 1] + (i & 1);
        }
    return bits;
    }
}
 ```

# JAVA知识补充

## 集合

## StringBuffer类与StringBuilder类

+ 当对字符串进行修改的时候，需要使用 StringBuffer 和 StringBuilder 类。
+ 和 String 类不同的是，StringBuffer 和 StringBuilder 类的对象能够被多次的修改，并且不产生新的未使用对象
+ StringBuilder类和StringBuffer类之间最大的不同在于StringBuilder的方法不是线程安全的（不能同步访问）

![avatar](F:\我的坚果云\Notebook\Leetcode\picture\stringbufferandstringbuilder.png)

### StringBuffer

```java
/**
在应用程序安全的情况下，必须使用StringBuffer类
**/
public class Test{
  public static void main(String args[]){
    StringBuffer sBuffer = new StringBuffer("菜鸟教程官网：");
    sBuffer.append("www");
    sBuffer.append(".runoob");
    sBuffer.append(".com");
    System.out.println(sBuffer);  //菜鸟教程官网：www.runoob.com
  }
}
```

+ 方法
  + public StringBuffer append(String s)
  + public StringBuffer reverse()
  + public delete(int start, int end)
  + public insert(int offset, int i)
  + insert(int offset, String str)
  + replace(int start, int end, String str)

### StringBuilder

```java
public class RunoobTest{
    public static void main(String args[]){
        StringBuilder sb = new StringBuilder(10);
        sb.append("Runoob.."); 
        System.out.println(sb);  // Runoob.. 
        sb.append("!");
        System.out.println(sb);  //Runoob..!
        sb.insert(8, "Java");
        System.out.println(sb);  //Runoob..Java!
        sb.delete(5,8);
        System.out.println(sb);   //RunoobJava!
    }
}
```

# Day 03 数组

## 剑指 Offer II 008. 和大于等于 target 的最短子数组

```

给定一个含有 n 个正整数的数组和一个正整数 target 。

找出该数组中满足其和 ≥ target 的长度最小的 连续子数组 [numsl, numsl+1, ..., numsr-1, numsr] ，并返回其长度。如果不存在符合条件的子数组，返回 0 。

```

【题解】前缀和+二分查找

+ 创建数组sums用于存储数组nums的前缀和，其中sums[i]表示从nums[0]到nums[i - 1]的元素和
+ 通过二分查找找到sums下标bound，使得sums[bound] - sums[i] >= target,此时最小数组长度是bound - (i - 1)

【注意】

+ 本题中二分查找通过调用Arrays.binarySearch()方法实现
+ 实现binarySearch方法

  ```java
  //此处请补充二分法查找实现代码
  
  ```

##  剑指 Offer II 009. 乘积小于 K 的子数组

  ```
  给定一个正整数数组 nums和整数 k ，请找出该数组内乘积小于 k 的连续的子数组的个数。
  ```

【题解】双指针法

+ 循环right ++ pro = pro * nums[right],此时就包括 right - left + 1个子数组
+ 当pro >= k pro = pro / nums[left] left++


## 剑指offer II 010.和为 k 的子数组

```
给定一个整数数组和一个整数 k ，请找到该数组中和为 k 的连续子数组的个数。
```

【前缀和+遍历】
+ 求前缀和数组sums，其中sums[i]表示从nums[0]到sums[i-1]的元素和
+ 遍历两遍寻找使得sums[left] - sums[right] = k的子数组，并计数;


## 剑指 Offer II 011. 0 和 1 个数相同的子数组
```

给定一个二进制数组 nums , 找到含有相同数量的 0 和 1 的最长连续子数组，并返回该子数组的长度。
```

【题解】
+ 
