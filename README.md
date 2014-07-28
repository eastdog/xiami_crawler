upunload

============

A python crawler for xiami music

修改'config'文件指定要下载的音乐
待下载音乐列表的网址列在'url='后面，不同网址用英文';'分隔。可供解析的网页地址包括专辑，精选集等，单曲页面会有错误。
每个网址对应的全部音乐写入一个文件夹，可以修改'outdir'指定存放位置，默认为当前文件夹下。
单进程，每次下载之间暂停5s，直接连接

modify file 'config' to specify music to be downloaded
single process, 5 seconds' sleeping between each download, direct fetch




