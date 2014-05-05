title: 异常处理
date: 2014-05-05 10:00
tags: exception
category: java
---

近期接触新的项目，发现原有异常设计是这样的，每个层抛出自己的 *checked exception* （可能包含异常信息，而且信息的格式五花八门）。
如分为4层 Action -> Service -> Biz -> DAO，异常结构是 Action 捕获 *ServiceException(BizException(DAOException("insert db error")))*，然后给用户展示 *e.getMessage()*

虽然觉得这么做不好，但是为什么不好呢。。

---

## 1.《Effective Java》中关于异常处理的几条建议
#### 1). 只针对不正常的情况才使用异常
不要用异常来控制流程。如：跳出循环 
#### 2). 对于可恢复的条件使用被检查的异常，对于程序错误使用运行时异常
#### 3). 避免不必要的使用被检查的异常
如果用checked exception需要同时满足以下两点：
1. 即使正确使用API并不能阻止异常条件的发生。
2. 产生了异常，使用API的程序员可以采取有用的动作对程序进行处理。
#### 4). 尽量使用标准的异常
|异常名|使用场景|
|----|----|
|IllegalArgumentException|参数的值不合适|
|IllegalStateException|参数的状态不合适|
|UnsupportedOperationException|对象不支持客户请求的方法|
|...|...|
#### 5). 抛出的异常要适合于相应的抽象
在Java的集合框架AbstractSequentialList的get()方法如下:

```java
public E get(int index) {
    try {
        return listIterator(index).next();
    } catch (NoSuchElementException exc) {
        throw new IndexOutOfBoundsException("Index: "+index);
    }
}
```
listIterator(index)会返回ListIterator对象，调用该对象的next()方法可能会抛出NoSuchElementException异常。而在get()方法中，抛出NoSuchElementException异常会让人感到困惑。所以，get()对NoSuchElementException进行了捕获，并抛出了IndexOutOfBoundsException异常。即，相当于将NoSuchElementException转译成了IndexOutOfBoundsException异常。
#### 6). 每个方法抛出的异常都要有文档
#### 7). 在细节消息中包含失败 -- 捕获消息
#### 8). 不要忽略异常

---

## 2. exception 真的性能好低

exception 继承与 throwable，里面有个fillInStackTrace，这个方法的定义：

```java
public synchronized native Throwable fillInStackTrace();   
```

jdk的具体实现：

```c
    Java_java_lang_Throwable_fillInStackTrace(JNIEnv *env, jobject throwable)  
    {  
        JVM_FillInStackTrace(env, throwable);  
        return throwable;  
    }  
      
    JVM_ENTRY(void, JVM_FillInStackTrace(JNIEnv *env, jobject receiver))  
      JVMWrapper("JVM_FillInStackTrace");  
      Handle exception(thread, JNIHandles::resolve_non_null(receiver));  
      java_lang_Throwable::fill_in_stack_trace(exception);  
    JVM_END  
      
    void java_lang_Throwable::fill_in_stack_trace(Handle throwable, TRAPS) {  
      if (!StackTraceInThrowable) return;  
      ResourceMark rm(THREAD);  
      
      ……………………………………………….  
      BacktraceBuilder bt(CHECK);  
      ………………………………………………  
      for (frame fr = thread->last_frame(); max_depth != total_count;) {  
        methodOop method = NULL;  
        int bci = 0;  
      ………………………………………………  
        bt.push(method, bci, CHECK);  
        total_count++;  
      }  
      
      // Put completed stack trace into throwable object  
      set_backtrace(throwable(), bt.backtrace());  
    }  
```

上面的代码中，这一系列调用可以发现，当你new一个exception的时候，jvm已经在exception里构建好了所有的stacktrace（BacktraceBuilderbt），这里花费的代价是可观的，试想一下，在web项目中，调用栈的深度可是很大的。因此，当你对stacktrace不感兴趣的时候，不需要这样的信息时，最好不要随便的new exception。

---

总结1和2，虽然现在的系统异常结构不好，修改量过大，复写了fillInStackTrace，直接返回null，对程序无影响。