title: 关于Java虚拟机（JVM）
date: 2013-04-17 21:53
tags: java, jvm, gc
category: java

### Java虚拟机

![jvm-logo](/pic/jvm/jvm-1.gif)

### 概述

**JVM**, 是让JAVA凌驾与操作系统之上的一个程序。大内总管的角色。

纵观历史，感觉Java的崛起JVM功不可没，很多大牛都是被那句对外声称的“**编写一次，到处运行**”勾引过来的。

近些年，JVM已经发展成一个生态圈，里面有众多语言，当然，如：

> Jython &gt; http://www.jython.org/

> JRuby &gt; http://JRuby.org/

> Groovy &gt; http://groovy.codehaus.org/

> Scala &gt; http://www.scala-lang.org/

### 哪里可以找到JVM？

	windows:
		jdk/jre/bin/jvm.dll
		jdk/jvm.dll
	linux:
		没找到，官方文档没有。知道的同学可以告诉下。

#### JRE

	JRE（Java Runtime Environment，Java运行环境），是运行JAVA程序所必须的环境的集合，包含JVM标准实现及Java核心类库。
	核心类库：jre/lib/rt.jar
	java.awt.*
	java.lang.*
	java.io.*
	java.net.*

	javax.imageio.*
	javax.net.ssl.*
	javax.swing.*

	org.w3c.dom.*

所以，运行java程序，rt.jar必须包含在classPath里面。

#### JDK

	JDK (Java Development Kit, JAVA开发者工具) ， 提供各种开发者工具，最主要的功能是 *.java -> *.class

	传奇jar包 ： jdk/lib/dt.jar and jdk/lib/tools.jar

	不知道大家注意没有，在安装完IDE，选择完jdk的路径之后，tools和dt.jar并没有加入到环境变量里面。也就是说明，我们平时编写程序，用不到这2个jar包。

	tools.jar: jdk/bin下比/jdk/jre/bin下多的功能，都是由tools实现。
		mouer@mouer-MacBook@02:02:09:~/Desktop/jdk1.7.0_05/bin
		$du -h *
		8.0K	javac
		8.0K	javah
		8.0K	javap

		我们看到每个命令及其的小，这是不科学的，实际上早期的jdk版本如1.4，java和javac等命令都是可以用vim查看的（当然是在linux下）。
		javac = java -p=$JAVA_HOME/lib/tools.jar xx.xxx.Main XXX.java
		最后把java便宜成class。

****

	dt.jar: BeanInfo设计类 swing 相关，告诉ide，哪个属性可以设置，哪个不可以设置，在NetBeans下用GUIDesigner的时候会叫你选择，找到一篇文章，看了一遍没有理解，只知道个大概，有兴趣同学可以参考：

	http://www.blogjava.net/landon/archive/2011/05/15/350285.html


#### 运行java Test.java后，java都干了什么(openJDK1.5, Oracle的没有找到)

	public class Test {
		public static void main(String[] args){
			System.out.println("hello world!")
		}
	}

	1. 根据$PATH定位JAVA的据对路径。
	2. 加载JVM.conf文件
	3. 调用Java_md.c中的方法检查环境是否一致（平台，cpu架构）
	4. 调用系统（linux：LoadLibray）api装载JVM
	5. 初始化JVM，获得JNI调用接口
	6. 调用java.c的LoadClass加载Test.class
	7. 解释执行。


### 运行时数据区域

![jvm-yunxing](/pic/jvm/jvm-2.jpg)

#### 程序计数器

对于一个运行中的Java程序而言，其中的每一个线程都有它自己的PC（程序计数器），在线程启动时创建。 大小是一个字长。它的作用可以看作是当前线程所执行的字节码的行号指示器。字节码解释器工作的时候就是通过改变这个计数器的值来选取下一条要执行的字节码命令，如分支，循环，跳转，异常处理，线程恢复。

**在规范中唯一没有规定OutOfMemoryError情况的区域。**

#### 虚拟机栈

java栈由许多栈帧(stack frame)组成的，栈帧主要包含局部变量表，存放了编译可知的各种基本数据类型(boolean, byte, char, short, int, float, long, double)，对象引用类型(d, ints) **32位机器占4个字节，64位机器占8个字节**。

	int[] ints = ArrayUtils.EMPTY_INT_ARRAY;
	Deal d = dealService.getDeal(66666);

当一个线程调用java方法时，虚拟机压入一个新的栈帧到java栈中，当方法返回的时候，这个栈帧被从java栈弹出并被抛弃。


![jvm-stack](/pic/jvm/jvm-3.jpg)

	方法调用：
	线程一：A->B->C->D;
	线程二：A->B->C;
	线程三：A->B->native

**在这个区域，规范中定义了StackOverflowError和OutOfMemoryError。**

#### 本地方法栈

本地方法栈，顾名思义，用来存放本地方法，和虚拟机栈工作原理相同。


**貌似 Sun HotSpot 将虚拟机栈和本地方法栈合二为一了， 在网站上没有找到相关介绍，待验证。**

#### Java堆

是jvm所管理的内存中最大的一块。java堆是被所有线程**共享**的一块区域.

jvm规范中是这么描述的，The heap is the runtime data area from which memory for **all class instances and arrays** is allocated. （所有的对象和数组都在这个区域）

	不过，在jdk1.6中，加入了一项功能，在代码运行的时候，进行逃逸分析（Escape Analysis）， 功能很多，其中一个作用是，如果能够证明别的方法或者线程不能通过任何途径访问道一个对象。那么这个对象将在栈上分配。打破了栈和堆的限制。有兴趣的同学可以研究下。
<http://dl.acm.org/citation.cfm?id=320386>  Escape analysis for Java - Choi

#### 方法区

和java堆一样，是各个线程共享的内存区域，它用于存储已被jvm加载的信息，常量，静态变量。

摘抄（未验证）：

	对于习惯在HotSopt虚拟机上开发和部署程序的开发者来说，很多人愿意把方法区成为“永久代”，本质上两者不相等，仅仅是因为HotSpot虚拟机的设计团队把GC分代筹集扩致方法区，或者说使用永久代来实现方法区而已，对于其他团队（BEA，IBM）来说是不存在永久代的概念的。即使HotSpot虚拟机本身，根据官方发布的路线图信息，现在也有放弃永久代并“搬家”至Native Memory来实现方法去的规划了。

	这说明在我们用的jvm中，方法区存在于堆中，和一般网上说的信息相符。


#### 运行时常量

存放String， 是方法区的一部分， 看资料说HotSopt放在堆中。

#### 直接内存

非jvm控制， 但是超过物理内存的限制，会抛出OutOfMemoryError，jdk1.4 NIO 中的 Channel 和 Buffer 的io方式。


### 各种异常

```java
/**
 * VM Args: -Xms10m -Xmx10m
 * 结果：java.lang.OutOfMemoryError: Java heap space堆超过10m抛出。
 */
public class Test {
	List list = new ArrayList();
	public static void main(String[] args){
	    while(true) {
			list.add(new Object());
		}
	}
}
/**
 * VM Args: -Xss128k
 * 结果：java.lang.StackOverflowError栈深度大于jvm允许的深度，抛出之。
 */
public class Test {
	public static void main(String[] args){
		SOF a = new SOF();
	}
}
class SOF {
	private SOF a;
	public SOF(){
		a = new SOF();
	}
}
/**
 * VM Args: -Xss2m
 * 结果：java.lang.OutOfMemoryError: unable to create new native thread慎用，死机。。。。！！！！
 */
public class Test {
	public static void main(String[] args){
		while(true) {
			Thread t = new Thread(new Runnable(){
				public void run() {
					while(true) {
						// doNothing...
					}
				}
			});
			t.start();
		}
	}
}
/**
 * 常量池溢出
 * VM Args: -XX:PermSize=5m -XX:MaxPermSize=5m
 * 结果：java.lang.OutOfMemoryError: PermGen space
 */
public class Test {
	public static void main(String[] args){
		List<String> list = new ArrayList<String>();
		int i = 0;
		while(true) {
			list.add(""+ i++);
		}
	}
}
/**
 * VM Args: -XX:MaxDirectMemorySize=5m -Xmx10m
 * 结果：java.lang.OutOfMemoryError
 */
public class Test {
	public static void main(String[] args){
		Field field = Test.class.getDeclaredFields()[0];
		field.setAccessible(true);
		while(true) {
			field.get(null).allocateMemory(1024 * 1024);
		}
	}
}
```

### 垃圾收集器

#### Serial 收集器

	Serial 收集器是最基本、历史最悠久的收集器，单线程的方式收集新生代的收集器，进行收集工作时会停止用户所有的工作线程（Stop the world），比较适合运行在 **Client** 模式下的虚拟机。

#### ParNew 收集器

	Serial 收集器的多线程版本，是运行在 **Server** 模式下虚拟机首选的新生代收集器，可以使用 -XX:+UseParNewGC 选项来强制指定它。

#### Parallel Scavenge 收集器

	使用了复制算法的新生代收集器，和 ParNew 一样，也是多线程实现的，他们的区别在于：Parallel Scavenge 收集器关注的是尽可能地达到一个可控的吞吐量，如虚拟机总共运行了100分钟，其中垃圾收集花掉1分钟，则吞吐量就是99%。

#### Serial Old 收集器

	Serial 收集器的老年代版本，使用“标记-整理”算法，比较时候在 Client 模式的虚拟机使用。

#### Parallel Old 收集器

	Parallel Scavenge 收集器的老年代版本，使用多线程的“标记-整理”算法。

#### CMS （Concurrent Mark Sweep）收集器

	CMS 收集器是一种以获取最短回收停顿时间为目标的收集器，基于“标记-清除”算法。

#### G1 (Garbage First) 收集器

	理论上的下一代收集器。jdk1.6 update14 后，跟随一个测试版，jdk1.7默认收集器。
	牛逼的它号称不会产生碎片，适合长时间运行，取消新生代和老年代的定义，划分成固定大小的独立空间。
	后台有个优先级的列表，清理垃圾最多的块（这可能是名字的由来）

#### 各种垃圾收集器搭配的方式

![jvm-gc](/pic/jvm/jvm-4.jpg)

官方推荐搭配：

	* Parallel Scavenge + Parallel Old
	* ParNew + CMS

一般来说，如果能使用 Parallel Scavenge + Parallel Old 的话就不要用 CMS，因为 Parallel 的吞吐量率更高，只要停顿时间不是太长的话，就不需要使用CMS收集器。

### 优化建议
	1.建议用64位操作系统，Linux下64位的jdk比32位jdk要慢一些，但是吃得内存更多，吞吐量更大。
	2.XMX和XMS设置一样大，MaxPermSize和MinPermSize设置一样大，这样可以减轻伸缩堆大小带来的压力。
	3.调试的时候设置一些打印参数，如-XX:+PrintClassHistogram -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintHeapAtGC -Xloggc:log/gc.log，这样可以从gc.log里看出一些端倪出来。
	4.系统停顿的时候可能是GC的问题也可能是程序的问题，多用jmap和jstack查看。
	5.仔细了解自己的应用，如果用了缓存，那么年老代应该大一些，缓存的HashMap不应该无限制长，建议采用LRU算法的Map做缓存，LRUMap的最大长度也要根据实际情况设定。
	6.不管怎样，永久代还是会逐渐变满，所以隔三差五重起java服务器是必要的。
	7.采用并发回收时，年轻代小一点，年老代要大，因为年老大用的是并发回收，即使时间长点也不会影响其他程序继续运行，网站不会停顿。

	在Resin论坛看到这样一个配置，据说比较牛B，8个G的情况下：
	$JAVA_ARGS .= " -Dresin.home=$SERVER_ROOT -server
    -Xms6000M -Xmx6000M -Xmn500M -XX:PermSize=500M -XX:MaxPermSize=500M
    -XX:SurvivorRatio=65536 -XX:MaxTenuringThreshold=0 -Xnoclassgc
    -XX:+DisableExplicitGC -XX:+UseParNewGC -XX:+UseConcMarkSweepGC
    -XX:+UseCMSCompactAtFullCollection -XX:CMSFullGCsBeforeCompaction=0
    -XX:+CMSClassUnloadingEnabled -XX:-CMSParallelRemarkEnabled
    -XX:CMSInitiatingOccupancyFraction=90 -XX:SoftRefLRUPolicyMSPerMB=0
    -XX:+PrintClassHistogram -XX:+PrintGCDetails -XX:+PrintGCTimeStamps
    -XX:+PrintHeapAtGC -Xloggc:log/gc.log "

    要满足：(Xmx-Xmn)*(100-CMSInitiatingOccupancyFraction)/100>=Xmn


