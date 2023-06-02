# import jwt
# import datetime
#
# # 替换为你的密钥
# JWT_SECRET = "huangjiabao"
#
# # 设置令牌有效期（例如 7 天）
# exp = datetime.datetime.utcnow() + datetime.timedelta(days=7)
#
# payload = {
#     "exp": exp
# }
#
# token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
# print(token)
from passlib.hash import sha256_crypt

password = "aiyc"
hashed_password = sha256_crypt.hash(password)
print(hashed_password)

import time

# 获取当前 Unix 时间戳
current_time = int(time.time())

# 计算 30 天后的 Unix 时间戳
expiration_time = current_time + 30 * 24 * 60 * 60

print(expiration_time)
