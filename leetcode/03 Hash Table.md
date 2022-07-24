# 一、哈希表理论基础

## 1. 哈希表

- 哈希表(Hash Table):又称散列表，数组就是一个典型的哈希表

- 一般哈希表都是用来快速判断一个元素是否出现集合里

## 2.哈希函数

- 以学生名字映射到哈希表上为例，把学生的姓名直接映射为哈希表上的索引，然后就可以通过查询索引下标快速知道这位同学是否在这所学校里了。

![哈希函数示例](https://img-blog.csdnimg.cn/2021010423484818.png)

- 如果hashCode得到的数值大于 哈希表的大小了，也就是大于tableSize了，怎么办呢？

## 3.哈希碰撞

- 如图所示，小李和小王都映射到了索引下标 1 的位置，这一现象叫做哈希碰撞。

![哈希碰撞](https://img-blog.csdnimg.cn/2021010423494884.png)

- 哈希碰撞一般有两种解决方法

  - 拉链法
  
  ![拉链法](https://img-blog.csdnimg.cn/20210104235015226.png)

  - 线性探测法：一定得保证tablesize > datasize

  ![线性探测法](https://img-blog.csdnimg.cn/20210104235109950.png)
  
## 4. 三种常见的哈希结构

- 三种常见的哈希结构
  - 数组
  - set （集合）
  - map(映射)

- **注意**：使用数组来做哈希的题目，是因为题目都限制了数值的大小。如果题目没有限制数值的大小，而且如果哈希值比较少、特别分散、跨度非常大，使用数组就造成空间的极大浪费。

- Java中set 和 map 分别提供以下三种数据结构

# 二.[有效的字母异位词](https://leetcode.cn/problems/valid-anagram/)

## 思路


- 使用数组分别记录


##  代码
```java
class Solution {
    public boolean isAnagram(String s, String t) {
    
        int[] array = new int[26];
        
        for(int i = 0;i < s.length();i++){
            int index = s.charAt(i) - 'a';
            array[index]++;
        }
        
        for(int i = 0;i < t.length();i++){
            int index = t.charAt(i) - 'a';
            array[index]--;
        }
        
        for(int a: array){
            if(a != 0){
                return false;
            }
        }
        
        return true;
    }
    
}

```

### 复杂度分析
  - 时间复杂度:O(n);
  - 空间复杂度:O(n).

## 其他题目
[383. 赎金信](https://leetcode.cn/problems/ransom-note/)
[49.字母异位词分组](https://leetcode.cn/problems/group-anagrams/)
[438.找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)

# 三、[两个数组的交集](https://leetcode.cn/problems/intersection-of-two-arrays/)

## 思路

利用两个哈希集合，进行重复值判断，其中一个用来存放数组1中的出现的值，第二个用来存放结果，

```java
for (int num : nums1){
  set.add(num);
}

for(int num : nums2){
  if(set.contains(num){
      set2.add(num);
  }
)
```

## 代码
```java
class Solution {
    public int[] intersection(int[] nums1, int[] nums2) {
        Set<Integer> set = new HashSet<Integer>();
        Set<Integer> result = new HashSet<Integer>();

        for(int num : nums1){
            set.add(num);
        }

        for(int num : nums2){
            if(set.contains(num)){
                result.add(num);
            }
        }

        int[] ans = result.stream().mapToInt(x -> x).toArray();

        return ans;
    }
)
```

## 复杂度分析
- 时间复杂度:O(n);
- 空间复杂度:O(n);

## [相似题目-两个数组的交集II](https://leetcode.cn/problems/intersection-of-two-arrays-ii/)
- 思路：
  - 利用哈希映射去统计长度较短数组中元素出现次数
  - 循环遍历长度较长的数组中元素，如果HashMap中元素数量大于0，则将该数字加入结果数组中，并对hashMap中元素个数进行处理。
- 代码：
```java
class Solution {
    public int[] intersect(int[] nums1, int[] nums2) {
        if(nums1.length > nums2.length){
            return intersect(nums2,nums1);
        }

        Map<Integer,Integer> map = new HashMap<Integer,Integer>();

        for(int num : nums1){
            int count = map.getOrDefault(num,0) + 1;
            map.put(num,count);
        }

        int[] ans = new int[nums1.length];
        int index = 0;
      
        for(int num : nums2){
          int count = map.getOrDefault(num, 0);
          if(count > 0){
            ans[index++] = num;
            count--;
            if(count > 0){
                map.put(num,count); 
            }else{
                map.remove(num);
            }
          }
        }
        
        return Arrays.copyOfRange(ans,0,index);
    }
}

```
