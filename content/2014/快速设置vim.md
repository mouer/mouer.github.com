title: 快速设置vim
date: 2014-04-29 22:00
tags: vim
category: vim

作为一个伪vimer，重装电脑后，第一件事就是配置vim。

```sh
# 需要先安装brew
brew install macvim
git clone git://github.com/ywjno/vundle-vimfiles.git
ln -s vundle-vimfiles
# vimfiles项目给我们提供了几个版本的vimrc
ln -s ~/.vim/vimrc ~/.vimrc
ln -s ~/.vim/gvimrc ~/.gvimrc
git clone git://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
```

进入vim
:BundleInstall


5分钟搞定，over～
