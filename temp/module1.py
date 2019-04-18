from operator import itemgetter
from itertools import groupby
from collections import Counter

arr = [
    {'codeName': '오랩요리란(난백)200g', 'previousStock': 36968, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 36968},
    {'codeName': 'SSL Carton 1kg 1등급 난백', 'previousStock': 38552, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 38552},
    {'codeName': '(외)Carton pack 950 난백', 'previousStock': 1812, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 1812},
    {'codeName': '(외)Carton pack(냉동) 1000 난백', 'previousStock': 2860, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 2860},
    {'codeName': '계란대신 오랩 요리란(전란) 500g', 'previousStock': 33626, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 33626},
    {'codeName': '(외)오랩요리란(전란)200g', 'previousStock': 1277, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 1277},
    {'codeName': 'ESL Carton 500g(전란)', 'previousStock': 30714, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 30714},
    {'codeName': 'SSL Carton 250g(난백)', 'previousStock': 223680, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 223680},
    {'codeName': 'Bag in Box pouch 5kg', 'previousStock': 49146, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 49146},
    {'codeName': '(외)계란대신 오랩 요리란(난백) 500g', 'previousStock': 1516, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 1516},
    {'codeName': '오랩요리란(전란)200g', 'previousStock': 25042, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 25042},
    {'codeName': 'SSL Carton 1kg 난황', 'previousStock': 107983, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 107983},
    {'codeName': '동물복지 유정란  전란 200g', 'previousStock': 46199, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 46199},
    {'codeName': '동물복지 유정란  전란 200g', 'previousStock': None, 'in': 444, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 51322},
    {'codeName': '(외)Carton pack 500 난황', 'previousStock': 601, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 601},
    {'codeName': '계란대신 오랩 요리란(전란) 200g', 'previousStock': 50590, 'in': None, 'in_price': None, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 50590},
    {'codeName': 'SSL Carton(냉동) 1kg 난백', 'previousStock': None, 'in': 3, 'in_price': 33, 'loss': None, 'insert': None, 'release': None, 'adjust': None, 'currentStock': 3}]

result = sorted(arr, key=lambda k: k['codeName'])
first_codeName = result[0]['codeName']

temp = [ item['codeName'] for item in result ]
print(len(temp), len(set(temp)))
if len(temp) != len(set(temp)):
    pass # 시작


for i in range(len(result)):
    if len(result) > i + 1 and result[i]['codeName'] == result[i+1]['codeName']:
        print('###')
        if not result[i]['previousStock']:
            result[i]['previousStock'] = result[i+1]['previousStock']
        if not result[i]['in']:
            result[i]['in'] = result[i+1]['in']
        if not result[i]['in_price']:
            result[i]['in_price'] = result[i+1]['in_price']
        result[i]['currentStock'] = result[i]['previousStock'] + result[i]['in'] + int(result[i]['release'] or 0)
        result.pop(i+1) 
    else:
        continue
    

print(result)