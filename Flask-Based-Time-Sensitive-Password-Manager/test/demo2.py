# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 20:59
# @Author  : AI悦创
# @FileName: demo2.py
# @Software: PyCharm
# @Blog    ：https://bornforthis.cn/
import pickle


# # 现在，我们可以在任何时候重新加载这些数据
# with open('admins.pickle', 'rb') as f:
#     loaded_data = pickle.load(f)

# 增加（Add）新的数据
# loaded_data['d'] = 'new data'

# 删除（Delete）数据
# del loaded_data['a']

# 查询（Query）数据
# if 'b' in loaded_data:
#     print('Found b:', loaded_data['b'])

# 修改（Update）数据
# loaded_data['b'] = ("modified string", u"modified unicode string")

# 将修改后的数据重新保存
# with open('data.pickle', 'wb') as f:
#     pickle.dump(loaded_data, f)

# 重新加载数据并打印，确认更改已经保存
# with open('data.pickle', 'rb') as f:
#     reloaded_data = pickle.load(f)

# print(reloaded_data)
# print(loaded_data)
# for admin in loaded_data:
#     print(vars(admin))

# 现在，我们可以在任何时候重新加载这些数据
with open('passwords.pickle', 'rb') as f:
    loaded_data = pickle.load(f)
    for pw in loaded_data:
        print(vars(pw))