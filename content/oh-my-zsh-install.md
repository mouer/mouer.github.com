layout: post
title: oh-my-zsh安装使用
date: 2013-04-20 22:23
comments: true
categories: [shell]

**无意中发现这个最近在github上很火爆的oh-my-zsh，又查询了下zsh，发现兼容bash，那果断升级了。**

```sh
# clone project
git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
# 拷贝配置文件
cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
# 设置默认是zsh
chsh -s /bin/zsh
# 修改默认更新时间
vim ~/.zshrc
export UPDATE_ZSH_DAYS=1
# 添加插件
vim ~/.zshrc
plugins=(git brew svn)
```

所有的主题接图： <https://github.com/robbyrussell/oh-my-zsh/wiki/themes>

所有的插件名字： <https://github.com/robbyrussell/oh-my-zsh/tree/master/plugins>

**注意** 别忘了导入自己定义的PATH.

![zsh-demo1](/pic/oh-my-zsh/oh-my-zsh-1.jpg)
![zsh-demo2](/pic/oh-my-zsh/oh-my-zsh-2.jpg)
