title: 常用shell备忘录
date: 2014-03-13 10:00
tags: shell
category: shell


不定时更新中

```sh

# 查看http链接状态
netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'

# 查看80使用情况
netstat -an -t | grep ':80' | grep ESTABLISHED | awk '{printf "%s %s\n", $5, $6}' | uniq | sort

# cpu数量
cat /proc/cpuinfo | grep -c processor

# 在vim中保存没有权限的修改
:w !sudo tee %

# 显示ascii码表
man ascii

# 在远程机器上执行一个本地脚本
ssh user@server bash < /path/to/local/script.sh

```
