title: ionicFramework简介
date: 2014-08-10 10:00
tags: android, ios, phoneGap
category: android, ios, phoneGap

简单说一下[Ionic](http://ionicframework.com/)是一款让你可以通过H5+CSS+JS做出原生应用的前端框架。

需要用到下面的技术：

* [Sass](http://sass-lang.com/)
* [AngularJS](https://angularjs.org/)
* [phoneGap/Cordova](http://cordova.apache.org/)

安装:

```sh
# 安装 cordova ionic
npm install -g cordova ionic

# 需要先安装ant, 生成一个带边栏（类似知乎）的例子
ionic start myApp sidemenu

# 生成android工程
ionic platform add android
ionic build android
```

下面就可以开发了：

* 打开intellij -> inport project -> xxx/platform/android -> Create project from existing sources
-> 一路next -> modules select android -> sdk里面勾选 android api
* 工程里面编辑 android/assets/www/xxxx
* AVD调试就可以了

玩的愉快～
