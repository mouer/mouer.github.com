layout: post
title: 也来谈谈java-HashMap
date: 2013-04-30 22:35
comments: true
categories: java

从源码中得到的信息：

1 HashMap没最大容量限制，超出Integer.MAX_VALUE后，size不准确。
```java
void resize(int newCapacity) {
    Entry[] oldTable = table;
    int oldCapacity = oldTable.length;
    if (oldCapacity == MAXIMUM_CAPACITY) {
        threshold = Integer.MAX_VALUE;
        return;
    }
    Entry[] newTable = new Entry[newCapacity];
    transfer(newTable);
    table = newTable;
    threshold = (int)(newCapacity * loadFactor);
}
```

2 HashMap的hash,hash的目的是使其均匀，当然，没有重复是做好状态，相信很多人看过这段代码：
```java

static int hash(int h) {
    // This function ensures that hashCodes that differ only by
    // constant multiples at each bit position have a bounded
    // number of collisions (approximately 8 at default load factor).
    h ^= (h >>> 20) ^ (h >>> 12);
    return h ^ (h >>> 7) ^ (h >>> 4);
}
```

猛一看，瞬间吓尿了。。我们来分析一下： [也可以看这里](http://stackoverflow.com/questions/9335169/understanding-strange-java-hash-function)

```java
public static void main ( String[] args ) {
    int h = 0xffffffff;
    int h1 = h >>> 20;
    int h2 = h >>> 12;
    int h3 = h1 ^ h2;
    int h4 = h ^ h3;
    int h5 = h4 >>> 7;
    int h6 = h4 >>> 4;
    int h7 = h5 ^ h6;
    int h8 = h4 ^ h7;

    printBin ( h );
    printBin ( h1 );
    printBin ( h2 );
    printBin ( h3 );
    printBin ( h4 );
    printBin ( h5 );
    printBin ( h6 );
    printBin ( h7 );
    printBin ( h8 );

}

static void printBin ( int h ) {
    System.out.println ( String.format ( "%32s",
                Integer.toBinaryString ( h ) ).replace ( ' ', '0' ) );
}
```

prints:

```
11111111111111111111111111111111
00000000000000000000111111111111
00000000000011111111111111111111
00000000000011111111000000000000
11111111111100000000111111111111
00000001111111111110000000011111
00001111111111110000000011111111
00001110000000001110000011100000
11110001111100001110111100011111
```

3 存储结构：

table&entry满足下面等式：

```java
// 如果, 其中length是hashmap的长度，默认是1<<30
hash(entryA.key) = hash(entryB.key)
i = hash(entryA.key) & (length)
// 那么, 其中->表示指向,A.B的谁后添加，谁在前面
table[i] -> enrtyA & entryA.next -> entryB
```

4 cpu百分百问题：

真是挺纳闷为什么有那么多蛋疼的人包括自己在研究hashMap的这个问题，在不正当的使用情况下，如多个线程有些插入，有些读取，会出现cpu 100%的情况，有可能是get，有可能是put。

其中[淘宝大牛](http://code.alibabatech.com/blog/dev_related_969/hashmap-result-in-improper-use-cpu-100-of-the-problem-investigated.html)应该分析出了一些情况，但是感觉有些片面。因为扩容之后，以前同一个table[i]下的节点，不一定映射到新table的同一个i上，加之java内存屏障的存在，非线程安全的方法，线程间同步共享变量的时机模糊不定。

在自己做的试验里面：

* 把hashMap源码copy出一份，在扩容后打印 entry entry.next entry.next.next。
* 有出现 entry = entry.next.next 的情况。
* 但更多100%的情况无迹可循。

所以大家知道会出问题就好，不要乱折腾这个了，说不定不同版本的jdk的源码都不一样呢。

絮絮叨叨一大堆。说给自己吧。看《蛇蝎美人》去了。
