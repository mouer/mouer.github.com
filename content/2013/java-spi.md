layout: post
title: java-spi机制介绍
date: 2013-04-24 22:20
comments: true
categories: java spi

SPI指<code>Service Provider Interface</code>，在开源项目中常常能看到，主要是定义好接口，让别人去完善这个功能。

如要开发一个文本编辑器，已经实现了现在市面上所有的文件类型，但过了一阵子忽然冒出来个新的文件类型，就不能用了。

如果通过<code>Java SPI</code>开发的解析接口（<code>com.edit.service.ParseFile</code>），那么给用户一个补丁包，这个补丁包仅仅包括一个jar包：

* 一个解析新文件类型的实现(com.edit.service.impl.ParseXXXFileImpl)
* META-INF/services/com.edit.service.ParseFile 写入 com.edit.service.impl.ParseXXXFileImpl

把补丁包放入class path 里就可以了。

```java
package com.ohoo.spi.service;
import java.util.ServiceLoader;
/**
 * User: chen.qi
 * Date: 13-4-24
 * Time: 下午9:54
 */
public class TestSPI {
    public static void main(String[] args) {
        ServiceLoader<ContainerService> serviceLoader = ServiceLoader.load(ContainerService.class);
        for (ContainerService containerService : serviceLoader){
            containerService.start();
            containerService.stop();
        }
    }
}
```

```java
package com.ohoo.spi.service;
/**
 * User: chen.qi
 * Date: 13-4-24
 * Time: 下午9:49
 */
public interface ContainerService {
    public void start();
    public void stop();
}
```

```java
package com.ohoo.spi.service.impl;
import com.ohoo.spi.service.ContainerService;
/**
 * User: chen.qi
 * Date: 13-4-24
 * Time: 下午9:51
 */
public class CContainerServiceImpl implements ContainerService {
    @Override
    public void start() {
        System.out.println("c start ...");
    }
    @Override
    public void stop() {
        System.out.println("c stop ...");
    }
}
```

<code>META-INF/services/com.ohoo.spi.service.ContainerService</code>

```
com.ohoo.spi.service.impl.AContainerServiceImpl
com.ohoo.spi.service.impl.BContainerServiceImpl
com.ohoo.spi.service.impl.CContainerServiceImpl
```