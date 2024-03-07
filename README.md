# 地址解析识别python版本
> 👉[JavaScript版本](https://github.com/wzc570738205/smartParsePro)

[在线体验colab](https://colab.research.google.com/drive/1AQ4UAT8N6KeZCSNXfKmrlCaVyah72bKy#scrollTo=gIU_U088qX-g)

项目基于[JioNLP 地址解析](https://github.com/dongrixinyu/JioNLP/wiki/Gadget-%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3#user-content-%E5%9C%B0%E5%9D%80%E8%A7%A3%E6%9E%90)来进行地址识别

地址库：[2020年国家统计局行政区划](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020)

基于[结巴分词](https://github.com/fxsjy/jieba) 提供的分词以及语义化分析进行姓名识别

基于[Levenshtein](https://github.com/Levenshtein) 字符串相似度算法来进行详细地址过滤

# [依赖下载](https://pypi.org/project/addressrec/)
python支持版本：`>=3.8 and <= 3.10`

```bash
pip3 install addressrec
```
# 使用
直接运行
```bash
import addressrec
print(addressrec.run('王志超029-68216000新疆维吾尔自治区乌鲁木齐市沙依巴克区西虹东路463号', True, False))

# addressrec.run(text, town_village, town_village)
# "text":"王志超029-68216000新疆维吾尔自治区乌鲁木齐市沙依巴克区西虹东路463号",
# "town_village": True, //可不传默认True 指定参数town_village(bool)，可获取乡镇、村、社区两级详细地名 
# "change2new": False //可不传默认True 指定参数change2new(bool)可自动将旧地址转换为新地址
```

返回结果：
```json
{
    "city": "乌鲁木齐市",
    "county": "沙依巴克区",
    "detail": "西虹东路463号",
    "name": "王志超",
    "phone": "029-68216000",
    "province": "新疆维吾尔自治区",
    "town": "",
    "village": ""
}
```
封装为接口调用：
```python
# pip3 install flask
from flask import Flask, request, jsonify
import addressrec

app = Flask(__name__)
@app.route('/smart_address', methods=['POST'])
def handle_smart_address():
    data = request.get_json()

    text = data.get('text', '')
    town_village = data.get('town_village', True)
    change2new = data.get('change2new', False)
    result = addressrec.run(text, town_village, change2new)

    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to process the request"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

#URL: `http://127.0.0.1:3000/smart_address`
#METHOD: 'POST'
#BODY:
#{
#    "text":"王志超029-68216000新疆维吾尔自治区乌鲁木齐市沙依巴克区西虹东路463号",
#    "town_village": true, //可不传默认true 指定参数town_village(bool)，可获取乡镇、村、社区两级详细地名 
#    "change2new": false //可不传默认false 指定参数change2new(bool)可自动将旧地址转换为新地址
#}
```
# 识别结果测试
```bash
广东省珠海市香洲区盘山路28号幸福茶庄,陈景勇，13593464918 识别结果：
{'city': '珠海市',
 'county': '香洲区',
 'detail': '盘山路28号幸福茶庄,，',
 'name': '陈景勇',
 'phone': '13593464918',
 'province': '广东省',
 'town': '',
 'village': ''}
-----------------
马云，陕西省西安市雁塔区丈八沟街道高新四路高新大都荟  13593464918  识别结果：
{'city': '西安市',
 'county': '雁塔区',
 'detail': '高新四路高新大都荟',
 'name': '马云',
 'phone': ' 13593464918',
 'province': '陕西省',
 'town': '丈八沟街道',
 'village': ''}
-----------------
陕西省西安市雁塔区丈八沟街道高新四路高新大都荟710061 刘国良 13593464918  识别结果：
{'city': '西安市',
 'county': '雁塔区',
 'detail': '高新四路高新大都荟710061',
 'name': '刘国良',
 'phone': ' 13593464918',
 'province': '陕西省',
 'town': '丈八沟街道',
 'village': ''}
-----------------
西安市雁塔区丈八沟街道高新四路高新大都荟710061 刘国良 13593464918  识别结果：
{'city': '西安市',
 'county': '雁塔区',
 'detail': '高新四路高新大都荟710061',
 'name': '刘国良',
 'phone': ' 13593464918',
 'province': '陕西省',
 'town': '丈八沟街道',
 'village': ''}
-----------------
雁塔区丈八沟街道高新四路高新大都荟710061 刘国良 13593464918  识别结果：
{'city': '西安市',
 'county': '雁塔区',
 'detail': '高新四路高新大都荟710061',
 'name': '刘国良',
 'phone': ' 13593464918',
 'province': '陕西省',
 'town': '丈八沟街道',
 'village': ''}
-----------------
收货人: 李节霁手机号码: 15180231234所在地区: 浙江省金华市婺城区西关街道详细地址: 金磐路上坞街 识别结果：
{'city': '金华市',
 'county': '婺城区',
 'detail': '详细地址: 金磐路上坞街',
 'name': '李节',
 'phone': ' 15180231234',
 'province': '浙江省',
 'town': '西关街道',
 'village': ''}
-----------------
收货人: 马云手机号码: 150-3569-6956详细地址: 河北省石家庄市新华区中华北大街68号鹿城商务中心6号楼1413室 识别结果：
{'city': '石家庄市',
 'county': '新华区',
 'detail': '中华北大街68号鹿城商务中心6号楼1413室',
 'name': '马云',
 'phone': ' 150-3569-6956',
 'phone1': '150-3569-6956',
 'province': '河北省',
 'town': '',
 'village': ''}
-----------------
```
#### LICENSE：[Apache License](https://github.com/wzc570738205/smartParsePro/blob/master/LICENSE)
#### IDE:致谢[JetBrains](https://www.jetbrains.com/?from=smartParsePro)为本项目提供免费license支持
[![JetBrains](http://cdn.wangzc.wang/LOGO-1.png)](https://www.jetbrains.com/?from=smartParsePro)
#### 联系我，欢迎交流
<img src="https://user-images.githubusercontent.com/33707245/211184007-971089c8-bdea-4d99-80d9-78de2fd59e01.png" width="300px">

#### qq交流群

![WX20210922-091703.png](https://cdn.wangzc.wang/uPic/WX20210922-09170315%20.png)
