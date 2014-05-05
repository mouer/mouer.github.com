Title: 使用Octopress搭建github博客
Date: 2012-12-15 21:53
Category: Octopress
Tags: Octopress, github

 因为gfw的原因，Google App Engine当真实蛋疼的紧，有不想花钱弄主机，就在这里搞的blog吧，记录下安装步骤。

### 安装
```
bash -s stable < <(curl -s https://raw.github.com/wayneeseguin/rvm/master/binscripts/rvm-installer) # 安装RVM
echo '[[ -s "$HOME/.rvm/scripts/rvm" ]] && . "$HOME/.rvm/scripts/rvm" ' >> ~/.bash_profile    # 添加环境变量到 ~/.bash_profile
source ~/.bash_profile  # source 一下，让它起作用
rvm install 1.9.3    # 安装ruby1.9.3 (rvm install 1.9.3 --with-gcc=clang)
rvm 1.9.3 --default  # 设置ruby默认版本为1.9.3
ruby --version       # 查看当前ruby版本是否已经被设置1.9.3
git clone git://github.com/imathis/octopress.git octopress  #从github clone octopress的源代码
cd octopress
### 安装一些依赖
gem install bundler
bundle install
rake install  # 安装主题
rake preview  # 本地预览 （http://localhost:4000/）
```

### 注意
如果有同学觉得 **gem** 或者 **rvm** 使用缓慢可以尝试淘宝的ruby源。
[taoBaoRuby](http://ruby.taobao.org/)

### 把blog部署到github
```
cd octopress
rake setup_github_pages # 和github创建关联
git@github.com:your_username/your_username.github.com.git   # 提示输入github URL
rake generate # 把你所有编辑的内容生成你的Blog静态页面
rake deploy   # 如果检查没有任何问题就可以 push 你的 blog 到 github master branch

### 状态检查
cd ~/octopress
git status   # 应该显示 On branch source
cd _deploy/  # 应该显示 On branch master

### 最后提交到source branch
git add .
git commit -m 'first commit'
git push origin source # 如果这一步出错，请再次检查仓库名称是否按要求命名，同时检查Admin面板下Default Branch是否为 master
```

### 更新Octopress
```
git pull octopress master     # Get the latest Octopress
bundle install                # Keep gems updated
rake update_source            # update the template's source
rake update_style             # update the template's style
```

### 新建文章
```
rake new_post["title"]		   # yyyy-MM-dd-post-title.md
```

### 分类方式
```
categories: [octopreess, github]
```

### 如果已经存在了github上面的Octopress，取回本地的操作
```
git clone -b source git@github.com:username/username.github.com.git octopress # get the source code from your "source" branch of your octopress on github
cd octopress
git clone git@github.com:username/username.github.com.git _deploy # get your static pages content from your "master"branch of your cotopress on github
```

### 一般操作
```
1. rake new_post["title"]
2. 快乐的点东西
3. rake generate
4. rake deploy
5. git add . && git commit -am 'blog' && git push origin source     # 把写的文件备份到source分支
```




