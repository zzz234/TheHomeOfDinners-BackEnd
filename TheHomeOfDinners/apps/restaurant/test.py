import re

param = 'c小吃l无卡是'
pattern = r'[cl]{1,1}(.*)[l]{0,1}(.*)'
ps = re.findall(pattern, param)
print(ps)
# print(ps[2])
# print(ps[2] == '')
