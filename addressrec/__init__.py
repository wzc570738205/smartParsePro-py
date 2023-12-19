# encoding=utf-8
import jieba
import paddle
import jionlp as jio
import jieba.posseg as pseg
import re
import Levenshtein
import sys

paddle.enable_static() 
jieba.enable_paddle()

# 地址识别 
# address_string 需要识别的字符串
# town_village   指定参数town_village(bool)，可获取乡镇、村、社区两级详细地名
# change2new     指定参数change2new(bool)可自动将旧地址转换为新地址
def run(address_string,town_village=True, change2new=False):
  obj = {
    'phone': "",
    'province': "",
    'city': "",
    'county': "",
    'town': "",
    'village': "",
    'detail': "",
  } 
  text = ""


  # 提取电话
  phones = jio.extract_phone_number(address_string)
  for phone in phones:
     address_string = address_string.replace(phone, " ")

  obj = merge_dicts(obj, process_phones(phones))
  
  address = jio.parse_location(address_string, town_village, change2new)

  obj['province'] = address.get('province') if address and address.get('province') is not None else ""
  obj['city'] = address.get('city') if address and address.get('city') is not None else ""
  obj['county'] = address.get('county') if address and address.get('county') is not None else ""
  obj['town'] = address.get('town') if address and address.get('town') is not None else ""
  obj['village'] = address.get('village') if address and address.get('village') is not None else ""
  obj['detail'] = address.get('detail')
  
  text = address_string.replace(obj.get('province'),'').replace(obj.get('city'),'').replace(obj.get('county'),'').replace(obj.get('town'),'').replace(obj.get('village'),'')
  
  obj['name'] = find_name(text,obj)
  # 清理详情信息中的名字以及乡镇、村、社区
  obj['detail'] = address.get('detail').replace(obj.get('name'),"").replace(obj.get('town'),'').replace(obj.get('village'),'').strip()

  return obj

def merge_dicts(dict1, dict2):
    merged_dict = dict1.copy()
    merged_dict.update(dict2)
    return merged_dict

def process_phones(phones):
    if len(phones) == 1:
        return {'phone': phones[0]}
    else:
        phone_dict = {f'phone{i}' if i > 0 else 'phone': phone for i, phone in enumerate(phones)}
        return phone_dict

def find_name(text, obj):
  name_list = []

  # 使用jieba进行分词
  seg_list = jieba.cut(text, cut_all=False)
  for word in seg_list:
    names = pseg.cut(word)
    for name in names:
      if extract_text_before_nr(name) is not None:
        name_list.append({'value':extract_text_before_nr(name)})

  # 计算名字的相似度
  for item in name_list:
     similarity_score = calculate_similarity(item.get('value'), obj.get('province')+obj.get('city')+obj.get('county')+obj.get('town')+obj.get('village')+obj.get('province'))
     item['similarity_score'] = similarity_score
  if name_list:
    min_element = min(name_list, key=lambda x: x['similarity_score'])
    return min_element.get('value')
  else:
    return ''


def extract_text_before_nr(input_text):
    # 定义正则表达式
    pattern = re.compile(r'(.+)/nr')

    # 使用正则表达式匹配文本
    match = pattern.search(str(input_text))

    # 如果匹配成功，返回匹配到的文本
    if match:
        return match.group(1)
    else:
        return None

def calculate_similarity(str1, str2):
    # 计算 Levenshtein 距离
    distance = Levenshtein.distance(str1, str2)

    # 计算相似度（值越小越相似）
    similarity = 1 - distance / max(len(str1), len(str2))

    return similarity


def extract_phone_numbers(text):
    # 手机号正则表达式
    mobile_pattern = re.compile(r'1[3456789]\d{9}')
    
    # 座机号正则表达式（简化版，仅匹配数字和横杠）
    landline_pattern = re.compile(r'\d{3,4}[-]?\d{7,8}')

    # 提取手机号
    mobile_numbers = re.findall(mobile_pattern, text)

    # 提取座机号
    landline_numbers = re.findall(landline_pattern, text)

    return {
        'mobile_numbers': mobile_numbers,
        'landline_numbers': landline_numbers
    }


   