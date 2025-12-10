# TodayDeerPipe 今天鹿什么
想法来自群内机器人有的“今天吃什么”功能，应群友要求简单做一个今天鹿什么。  
100%ai制作，感谢claude.ai。  
### 这是什么？
依据n恒泰tag标签页生成随机tag组合之后按照对应tag查询，默认tags文件内包含popular前两页共计240个tag，经过测试再往后添加就会出现大量三个tag无法匹配到对应内容的问题，小众xp可以自行增减tag数量。  
为了方便获取tag，同时添加了通过html代码读取tag的功能，但是分布于两个文件，有需要情自行处理。（其实是今天claude没次数了，以后再说）  
tags.txt文件的格式是tag1 (count), tag2 (count), tag3 (count)，其中count为该tag所有类目的数量和，在生成组合时会展示在生成列表中，可以大致判断是否有符合筛选结果的内容。  
#### 本地
gui完全由自带库实现，所以只需要安装beautifulsoup4即可，不过我想应该也不会有人本地整这个。  
pip install beautifulsoup4  
