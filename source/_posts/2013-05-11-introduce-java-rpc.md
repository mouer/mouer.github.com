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

{% gist 5559211 %}
