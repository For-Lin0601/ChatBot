##### QQ设置 #####
# go-cq设置不支持热重载

# QQ号 必改！
qq = 3457195338  # 测试用QQ号, 请务必修改!

# 使用手表协议, 扫码登入, 无需密码
# 服务器搭载请在本地运行 ./go-cqhttp/go-cqhttp.exe
# 登入成功后将 ./go-cqhttp/data 文件夹复制到服务器相同目录
# 仅需在第一次配置即可, 后续若无风控则不会丢失 data


# 手表协议无法接收戳一戳等消息, 详情请看https://docs.go-cqhttp.org/guide/config.html#%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF
# 若想启用其他协议, 请自行更改 ./go-cqhttp/device.json 的 protocol 字段, 具体数值参考上述网址
# 提示: 其他协议均不支持扫码登入


##### gocqOnQQ 配置文件 #####
# 没意外此处不用更改, 服务器请开启对应端口的安全组
# 默认请开启 5700, 6700, 6701 端口
# go-cq设置不支持热重载

# 签名服务器地址
host = "127.0.0.1"

# 签名服务器端口号
port = 5700
# 签名服务器 api_key
api_key = "114514"

# 签名服务器 authorization
authorization = "Bearer 114514"

# 正向 Websocket 服务器监听地址
ws_address = "127.0.0.1:6700"

# http 通信
http_address = "127.0.0.1:6701"
