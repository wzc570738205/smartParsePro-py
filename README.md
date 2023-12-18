# 地址解析识别python版本
> 👉[JavaScript版本](https://github.com/wzc570738205/smartParsePro)

项目基于[JioNLP 地址解析](https://github.com/dongrixinyu/JioNLP/wiki/Gadget-%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3#user-content-%E5%9C%B0%E5%9D%80%E8%A7%A3%E6%9E%90)来进行地址识别

地址库：[2020年国家统计局行政区划](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020)

基于[结巴分词](https://github.com/fxsjy/jieba) 提供的分词以及语义化分析进行姓名识别

基于[Levenshtein](https://github.com/Levenshtein) 字符串相似度算法来进行详细地址过滤

# 依赖下载
python支持版本：`>=3.8`

JioNLP下载
```bash
pip3 install jionlp
```
结巴分词下载
```bash
pip3 install jieba
```
Levenshtein字符串相似度分析
```bash
pip3 install Levenshtein
```
paddlepaddle语义分析参考[paddlepaddle 3.8 支持](https://github.com/fxsjy/jieba/issues/920)
```bash
pip3 install paddlepaddle==2.4.2
```
flask下载：
```bash
pip3 install flask
```

# 使用
直接运行
```bash
python3 index.py '王志超029-68216000新疆维吾尔自治区乌鲁木齐市沙依巴克区西虹东路463号'
```
接口形式运行 
```bash
# 默认端口3000
python3 index.py serve  
# 指定端口运行
python3 index.py serve 8088 
```
## api调用
```JS
URL: `http://127.0.0.1:3000/smart_address`
METHOD: 'POST'
BODY:`
{
    "text":"王志超029-68216000新疆维吾尔自治区乌鲁木齐市沙依巴克区西虹东路463号",
    "town_village": true, //可不传默认true 指定参数town_village(bool)，可获取乡镇、村、社区两级详细地名 
    "change2new": false //可不传默认false 指定参数change2new(bool)可自动将旧地址转换为新地址
}`
RESPONSE:`
{
    "city": "乌鲁木齐市",
    "county": "沙依巴克区",
    "detail": "西虹东路463号",
    "name": "王志超",
    "phone": "029-68216000",
    "province": "新疆维吾尔自治区",
    "town": "",
    "village": ""
}`
```

#### LICENSE：[Apache License](https://github.com/wzc570738205/smartParsePro/blob/master/LICENSE)
#### IDE:致谢[JetBrains](https://www.jetbrains.com/?from=smartParsePro)为本项目提供免费license支持
[![JetBrains](http://cdn.wangzc.wang/LOGO-1.png)](https://www.jetbrains.com/?from=smartParsePro)
#### 联系我，欢迎交流
<img src="https://user-images.githubusercontent.com/33707245/211184007-971089c8-bdea-4d99-80d9-78de2fd59e01.png" width="300px">

#### qq交流群

![WX20210922-091703.png](https://cdn.wangzc.wang/uPic/WX20210922-09170315%20.png)
