layout: post
title: git-flow的介绍及使用
date: 2013-04-23 14:12
comments: true
categories: git

#### git-flow 简介

git-flow基于git，是根据实际经验设计出一套基于分支的开发/发布模型。

项目地址： <https://github.com/nvie/gitflow>

模型概念如下图：

![git-flow-sketch](/pic/gitflow/gitflow.jpg)

#### 安装使用纪录

因为公司服务器是svn，本地用git-svn + git-flow，所以hotfix功能一直没用

用的是<code>git flow feature start xxx</code> 简单纪录如下：

```sh
# 安装git-flow
brew install git-flow
# 开启zsh的git-flow插件
plugins=(git git-flow brew svn rake vim)
# 初始化以后的git目录, 一路回车下一步
cd xxx && git flow init
# 开始做一个需求， 会自动切换到feature/task1分支，这时候可以写代码。
git flow feature start task1
# 当这个需求做完了。这时候会把task1的提交merge回develop中
git flow feature finish task1
# 对于git-svn用户，那么可以提交到svn了
git svn rebase;
git svn dcommit;
```

很多方法正在摸索，不定时更新之。。
