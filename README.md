A python crawler of xiami

简易版本，女朋友会用，亲测
============

修改'config'文件指定要下载的音乐

运行 'python upunload.py'， windows用户可以直接双击dist文件夹下的'upunload.exe'


待下载音乐列表的网址列在'url='后面，不同网址用英文分号( ; )分隔。可供解析的网页地址包括专辑，精选集等，不解析单曲页面。
每个网址对应的全部音乐写入一个文件夹，可以修改'outdir'指定存放位置，默认为当前文件夹下。

单进程单线程，每次下载之间暂停5s，无代理直接连接



modify file 'config' to specify music to be downloaded

run 'python upunload.py', or double click 'dist/upunload.exe' for windows users

single process, 5 seconds' sleeping between each download, direct fetch




