layout: post
title: 排序方式
date: 2013-05-16 12:18
comments: true
categories: [sort]

看到一些奇异的排序方式，记录下：

##### 一， 珠排序：

在珠排序中，一行表示一个数字。如果一行里有2颗珠子，该行代表数字2；如果一行里有4颗珠子，该行代表数字4。给定一个数组，数组里有多少个数字，就要有多少行；数组里最大的数字是几，就要准备多少根杆子。

第一步，将珠子悬挂在垂直竹竿上

![BeadSort-1.png](/pic/sort/BeadSort-1.png)


第二步，让珠子掉落

![BeadSort-2.png](/pic/sort/BeadSort-2.png)

实现需矩阵

##### 二， Bogo排序（又称囧排序-扯淡）：

在计算机科学中，Bogo排序（bogo-sort）是个既不实用又原始的排序算法，其原理等同将一堆卡片抛起，落在桌上后检查卡片是否已整齐排列好，若非就再抛一次。其名字源自Quantum bogodynamics，又称bozo sort、blort sort或猴子排序。

```java
Random random = new Random();

public void bogoSort(int[] n) {
    while(!inOrder(n))shuffle(n);
}

public void shuffle(int[] n) {
    for (int i = 0; i < n.length; i++) {
        int swapPosition = random.nextInt(i + 1);
        int temp = n[i];
        n[i] = n[swapPosition];
        n[swapPosition] = temp;
    }
}

public boolean inOrder(int[] n) {
    for (int i = 0; i < n.length-1; i++) {
        if (n[i] > n[i+1]) return false;
    }
    return true;
}
```

五雷轰顶。。


PS：

附上一些排序GIF图片：

鸡尾酒排序：

![Sorting-shaker-sort-anim.gif](/pic/sort/Sorting-shaker-sort-anim.gif)

希尔排序：

![Sorting_shellsort_anim.gif](/pic/sort/Sorting_shellsort_anim.gif)

堆排序(堆排序算法的演示。首先，将元素进行重排，以符合堆的条件。图中排序过程之前简单的绘出了堆树的结构。)：

![Sorting_heapsort_anim.gif](/pic/sort/Sorting_heapsort_anim.gif)

快速排序：

![Sorting_quicksort_anim.gif](/pic/sort/Sorting_quicksort_anim.gif)


