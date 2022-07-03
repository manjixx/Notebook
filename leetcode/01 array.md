# 1.数组

## 1.1 二分查找

> 二分查找思路

* **使用二分查找的前提**
  * 数组为有序数组
  * 数组中元素不重复，如果重复则返回下标不唯一
  
* 二分法的写法
  * 因为两种写法，左侧总是闭区间，因此```if(nums[mid] < target）```即$target$位于右侧区间时，left总是取$left = mid + 1$
  * 写法一：**$[Left，right]$**
    * ```while(left <= right```，因为**此时为闭区间**所以此处**应该使用$<=$**
    * ```if(nums[mid] > target)```，即$target$位于左侧区间，因为此时取闭区间，且$nums[mid] != target$，所以$right = mid - 1$
  
  ```java
   // 版本一
    public int search(int[] nums, int target) {

        int left = 0;
        int right = nums.length - 1;

        while(left <= right){
            int mid = left +  (right - left) / 2;
            if(nums[mid] == target){
                return mid;
            }

            if(target < nums[mid]){
                right = mid - 1;
            }else{
                left = mid + 1;
            }
        }
        return -1;
    }
  ```

  * 写法二：**$[Left，right)$**
    * ```while(left < right)```，因为**为开区间**，所以**此处应该使用 $<$**
    * ```if(nums[mid] > target)```，即$target$位于左侧区间，此时取$[left,right)$，且$nums[mid] != target$，因此$right = mid$

    ```java
     public int search(int[] nums, int target) {

        int left = 0;
        int right = nums.length;

        while(left < right){
            int mid = left +  (right - left) / 2;
            if(nums[mid] == target){
                return mid;
            }
            if(target < nums[mid]){
                right = mid;
            }else{
                left = mid + 1;
            }
        }
        return -1;
    }
    ```

> 二分查找题目

* [二分查找](https://leetcode-cn.com/problems/binary-search/submissions/)

* [搜索插入位置](https://leetcode.cn/problems/search-insert-position/)
  * 必须使用$O(log n)$的算法
  * 思路：本题与二分查找的不同点在于最终返回值的不同
  
* [在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/)
  * 思路：
    * 判断$target$的位置，总共有三种：
      * $target$位于数组的左侧或者右侧
      * $target$在数组范围内，但是数组中**不存在**$target$
      * $target$在数组范围内，且数组中**存在**$target$
    * 利用二分查找确定左右边界

    ```java
    /**
        二分查找，寻找右边界(不包括target)
        为了处理target在nums左侧，将rightBorder = -2(如数组[3,3]，target为2)
    */
    private int searchRightBorder(int[] nums, int target){
        int rightBorder = -2; 
        int left = 0;
        int right = nums.length - 1;
        while(left <= right){
            int mid = left + (right - left) / 2;
            if(nums[mid] > target){
                // target 在左区间，所以[Left, mid - 1]
                right = mid - 1;
            }else{
                // target 在右区间，所以[mid + 1，right]，同时更新rightBorder
                left = mid + 1;
                rightBorder = left;
            }
        }
        return rightBorder;
    }


    /**
        二分查找，寻找左边界(不包括target)
        为了处理target在nums右侧，leftBorder = -2(如数组[3,3]，target为4)
    */
    private int searchLeftBorder(int[] nums, int target){
        int LeftBorder = -2; 
        int left = 0;
        int right = nums.length - 1;
        while(left <= right){
            int mid = left + (right - left) / 2;
            if(nums[mid] >= target){
                // target 在左区间，所以[Left, mid - 1]，同时更新leftBorder
                right = mid - 1;
                leftBorder = right;
            }else{
                // target 在右区间，所以[mid + 1，right]
                left = mid + 1;
            }
        }
        return leftBorder;
    }
    
    ```

  * 代码
  
  ```java
  public int[] searchRange(int[] nums, int target) {
       int leftBorder = serachLeftBorder(nums,target);
       int rightBorder = serachRightBorder(nums,target);
       if(leftBorder == -2 || rightBorder == -2){
           return new int[]{-1,-1};
       }
       if(rightBorder - leftBorder > 1) return new int[]{leftBorder + 1, rightBorder - 1};
    
        return new int[] {-1,-1};     

    }

    private int serachLeftBorder(int[] nums,int target){
        int leftBorder = -2;
        int left = 0;
        int right = nums.length - 1;
        while(left <= right){
            int mid = left + (right - left) / 2;
            if(nums[mid] >= target){        // 当nums[mid] >= target时，说明target在左侧数组，因此更新右边界，同时更新leftBorder
                right = mid - 1;             
                leftBorder = right;
            }else{                          // 当nums[mid] < target时，说明target在右侧数组，因此更新左边界，因为选择闭区间所以right = mid - 1
                left = mid + 1;
            }
        }
        return leftBorder;
    }

    private int serachRightBorder(int[] nums,int target){
        int rightBorder = -2;
        int left = 0;
        int right = nums.length - 1;
        while(left <= right){
            int mid = left + (right - left) / 2;
           if(nums[mid] > target){        // 当nums[mid] > target时，说明target在左侧数组，因此更新右边界
                right = mid - 1;             
            }else{                          // 当nums[mid] < target时，说明target在右侧数组，因此更新左边界，同时更新rightBorder
                left = mid + 1;
                rightBorder = left;
            }
        }
        return rightBorder;
    }
  
  ```

* [X的平方根](https://leetcode.cn/problems/sqrtx/)
  * 思路：由于 $x$ 平方根的整数部分 $ans$ 是满足 $k^2 <= x$ 因此我们可以对 $k$ 进行二分查找，从而得到答案。
  * 代码

    ```java
    public int mySqrt(int x) {
            int left = 0;
            int right = x;
            int ans = -1;
            while(left <= right){
                int mid = left + (right - left) / 2;
                if((long) mid * mid <= x){
                    ans = mid;
                    left = mid + 1;
                }else{
                    right = mid - 1;
                }
            }
            return ans;
        }
    ```

  * 复杂度分析：
    * 时间复杂度：$O(logn)$
    * 空间复杂度：$O(1)$

* [有效的完全平方数](https://leetcode.cn/problems/valid-perfect-square/)
  * 思路
  * 代码

* [搜索旋转数组](https://leetcode-cn.com/problems/search-in-rotated-sorted-array/solution/sou-suo-xuan-zhuan-pai-xu-shu-zu-by-leetcode-solut/)

* 题目描述
  > 整数数组 nums 按升序排列，数组中的值互不相同 。
  > 在传递给函数之前，nums 在预先未知的某个下标 k（0 <= k < nums.length）上进行了 旋转，使数组变为 [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]（下标 从 0 开始 计数）。例如， [0,1,2,4,5,6,7] 在下标 3 处经旋转后可能变为 [4,5,6,7,0,1,2] 。
  > 给你旋转后的数组 nums 和一个整数 target ，如果 nums 中存在这个目标值 target ，则返回它的下标，否则返回 -1 。

* 解题思路
  * 通过查看当前$mid$位置分割出来的两个部分$[l,mid]$和$[mid + 1,r]$哪一部分是有序的，**可以利用有序部分确定$target$是否在当前区间内**，然后根据有序部分确定如何改变二分查找的上下界。
    * 如果$[l,mid]$是有序的，且target 的大小满足 $[nums[l],nums[mid]]$ ，则我们应该将搜索范围缩小至 $[l, mid - 1]$，否则在 $[mid + 1, r]$ 中寻找。

    * 如果$[mid + 1,r]$是有序的，且target 的大小满足 $[nums[mid + 1],nums[r]]$ ，则我们应该将搜索范围缩小至 $[mid + 1, r]$，否则在 $[l, mid - 1]$ 中寻找。

* 代码

```java
class Solution {
    public int search(int[] nums, int target) {
        int len = nums.length;
        if(len == 1){
            return nums[0] == target ? 0 : -1;
        }

        int left = 0;
        int right = len - 1;

        while(left <= right){
            int mid = left + (right - left) / 2;
            if(nums[mid] == target){
                return mid;
            }
            // 如果左半边有序
            if(nums[0] <= nums[mid]){
                if(nums[0] <= target &&  target < nums[mid]){// 如果target在本区间内，则在[left,mid - 1]中继续寻找
                    right = mid - 1;
                }else{
                    left = mid + 1;
                }
            }else{ // 如果[mid + 1, right]是有序的
                if(nums[mid] < target && target <= nums[right]){
                    left = mid + 1;
                }else{
                    right = mid - 1;
                }
            }
        }
        return -1;
    }
}

```

## 1.2 移除元素

### [移除元素](https://leetcode.cn/problems/remove-element/submissions/)
  * 思路——双指针
    * 利用快慢指针，将$nums[fast] != val$的值全部移到最左端
  
    ```java
    if(nums[fast] != val){
        nums[slow++] = nums[fast];
    }
    ```

    * 复杂度分析
      * 时间复杂度：$O(logn)$
      * 空间复杂度：$O(1)$

### [26.删除排序数组中的重复项](https://leetcode.cn/problems/remove-duplicates-from-sorted-array/)
  * 思路：双指针
    * 定义快慢指针$slow,fast$，二者初始均指向1
    * 然后fast顺序向后移动，如果$nums[fast] != nums[fast - 1]$,则将nums[fast]与nums[slow]交换，同时slow自增1
    * 特殊情况，当数组长度为0时，直接返回0;


## 1.3 [有序数组的平方](https://leetcode.cn/problems/squares-of-a-sorted-array/)

### 思路一：暴力求解

### 思路二：双指针


## 1.4 [长度最小的子数组](https://leetcode.com/problems/minimum-size-subarray-sum/)

### 暴力解法


### 滑动窗口


### 其他题目推荐

- [水果成篮](https://leetcode.com/problems/fruit-into-baskets/)

- [最小覆盖子串](https://leetcode.com/problems/minimum-window-substring/)


## 1.5 [螺旋矩阵II](https://leetcode.com/problems/spiral-matrix-ii/)

### 思路


### 相似题目推荐

- [螺旋矩阵](https://leetcode.com/problems/spiral-matrix/)


## 1.6 总结

- 数组特点

- 解题方法汇总
  - 二分法
  - 双指针法
  - 滑动窗口
  - 模拟法  
