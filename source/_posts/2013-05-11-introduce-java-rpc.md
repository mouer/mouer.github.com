---
layout: post
title: "当java遇上rpc"
date: 2013-05-11 14:44
comments: true
categories: [java, rpc]
---

### rpc 和 mq

要说rpc就不得不提提mq，两个家伙分工完美，系统才后完美，简单的说，下面几种情况，那么请使用rpc：

* 不需要返回值
* 不依赖执行顺序
* 不想受限与服务端的处理速度

### RPC 是什么

远程过程调用 Remote Procedure Call

key : <code>远程</code> <code>过程</code>

#### 远程
* 相对本地调用函数来说，被调用方法处于独立的进程、地址空间、主机，可能跨语言，硬件体系结构也可能不一样

#### 过程
* 以函数调用的语法出现，看起来像本地。

#### 如何得到接口

* 跨语言 ：IDL （ICE，THRIFT..一般生成stub/skeleton）
* java ： 提供service包，实际调用是个代理类

#### 如何描述对象

* 序列化 （XML，JSON，brinary，hessian，protobuf...）

#### 如何传递

* 可以基于各种传输协议
* 可以基于应用层协议

#### 如何工作

* client->序列化->传输->反序列化->service

# 纯java实现RpcFramework

<code>RpcFramework.java</code>

```java
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
/**
 * User: chen.qi
 * Date: 13-4-19
 * Time: 上午11:26
 */
public class RpcFramework {
    /**
     * 暴露服务接口
     * @param service 服务实现类
     * @param port 服务暴露端口
     * @throws Exception
     */
    public static void expose(final Object service, int port) throws Exception {
        ServerSocket server = new ServerSocket(port);
        ExecutorService es = Executors.newCachedThreadPool();
        while(true) {
            final Socket socket = server.accept();
            es.execute(new Runnable() {
                @Override
                public void run() {
                    ObjectInputStream input = null;
                    ObjectOutputStream output = null;
                    try {
                        // 读入输入
                        input = new ObjectInputStream(socket.getInputStream());
                        String methodName = input.readUTF();
                        Class[] parameterTypes = (Class[])input.readObject();
                        Object[] arguments = (Object[])input.readObject();
                        output = new ObjectOutputStream(socket.getOutputStream());
                        // 运行方法
                        Method method = service.getClass().getMethod(methodName, parameterTypes);
                        Object result = method.invoke(service, arguments);
                        // 返回结果
                        output.writeObject(result);
                    } catch (Exception e) {
                        e.printStackTrace();
                    } finally {
                        org.apache.commons.io.IOUtils.closeQuietly(input);
                        org.apache.commons.io.IOUtils.closeQuietly(output);
                    }
                }
            });
        }
    }
    /**
     * 取得代理对象
     * @param interfaceClass 代理class
     * @param host 主机名
     * @param port 端口
     * @return o
     * @throws Exception
     */
    public static Object getProxy(final Class interfaceClass, final String host, final int port) throws Exception {
        return Proxy.newProxyInstance(interfaceClass.getClassLoader(), new Class[]{interfaceClass}, new InvocationHandler() {
            public Object invoke(Object proxy, Method method, Object[] arguments) throws Throwable {
                Socket socket = new Socket(host, port);
                try {
                    ObjectOutputStream output = new ObjectOutputStream(socket.getOutputStream());
                    try {
                        output.writeUTF(method.getName());
                        output.writeObject(method.getParameterTypes());
                        output.writeObject(arguments);
                        ObjectInputStream input = new ObjectInputStream(socket.getInputStream());
                        try {
                            Object result = input.readObject();
                            if (result instanceof Throwable) {
                                throw (Throwable) result;
                            }
                            return result;
                        } finally {
                            org.apache.commons.io.IOUtils.closeQuietly(input);
                        }
                    } finally {
                        org.apache.commons.io.IOUtils.closeQuietly(output);
                    }
                } finally {
                    org.apache.commons.io.IOUtils.closeQuietly(socket);
                }
            }
        });
    }
}
```

<code>ServerMain.java</code>

```java
import org.mouer.framework.RpcFramework;
import test.service.impl.TestHelloServiceImpl;
/**
 * User: chen.qi
 * Date: 13-4-19
 * Time: 下午12:03
 */
public class ServerMain {
    public static void main(String[] args) throws Exception {
        RpcFramework.expose(new TestHelloServiceImpl(), 7373);
    }
}
```

<code>ClientMain.java</code>

```java
import org.mouer.framework.RpcFramework;
import test.service.TestHelloService;
/**
 * User: chen.qi
 * Date: 13-4-19
 * Time: 下午12:03
 */
public class ClientMain {
    public static void main(String[] args) throws Exception {
        TestHelloService testHelloService = (TestHelloService)RpcFramework.getProxy(TestHelloService.class, "127.0.0.1", 7373);
        for (int i = 1; i < 11; i++) {
            Hello hello = testHelloService.sayHello();
            System.out.println("第" + i + "次：" + hello.getMessge());
        }
    }
}
```