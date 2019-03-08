# Bilibili-Invalid-Fav-Dump
抓取Bilibili收藏夹中的无效视频，输出到本地txt文件中。


#### 2019.03.06 - 由于B站更新了返回消息内容，失效视频的标题全部为“已失效视频”，也就是说无法再获取标题。目前此脚本已无实际作用，如果有人能告知获取失效AV信息的方法，请PM我。

#### Intro
当你逛B站打开自己的收藏夹，会发现这种情况：
![Demo1 Img]

以前Bilibili收藏夹中无效视频还可以看到缩略图和标题，现在只能F12查看json流。
写了个python小脚本，可以提取无效视频信息并输出到本地。

#### 前置需求：
  - 所抓取的用户有公开的收藏夹
  - 需要python运行时,直接[官网](https://www.python.org/downloads/)安装
  - 安装requests库
```cmd
  pip install requests
```

#### 简易用法：
  - 下载InvalidVideos.py\n
  - 查找自己B站的mid
  - cmd输入
```cmd
  python InvalidVideos.py 你的mid  
```
#### 详细用法：
  - 安装完整的[python运行时](https://www.python.org/downloads/)
  - 开始菜单-输入cmd 回车
  - 输入pip install requests
  - 等待库下载完成。
  - 进入自己在B站的空间，例如：space.bilibili.com/17819768/#/ (数字既为你的mid)
  - 下载InvalidVideos.py到某文件夹，比如C:/misc/
  - 进入该文件夹，在里边shift+右键，寻找‘在这里打开控制台’类似的命令
  - 在控制台中输入
```cmd
  python InvalidVideos.py 17819768
```
#### 输出结果：
会在当前目录下输出一个invalidFavVideos.txt。
长这样子。
![Demo2 Img]

赞美太阳 \\[T] /



[Demo1 Img]:             https://github.com/yuiwong/Bilibili-Invalid-Fav-Dump/blob/master/misc/p1.PNG
[Demo2 Img]:             https://github.com/yuiwong/Bilibili-Invalid-Fav-Dump/blob/master/misc/p2.PNG
