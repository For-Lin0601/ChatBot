import logging
########## 主线程必选项 ##########


########## plugin.name='Log' plugin.path='//plugins//__log//main' ##########

# 日志级别
logging_level = logging.DEBUG


########## plugin.name='ThreadCtlPlugin' plugin.path='//plugins//__threadctl//main' ##########
# 线程池相关配置, 该参数决定机器人可以同时处理几个人的消息, 超出线程池数量的请求会被阻塞, 不会被丢弃, 如果你不清楚该参数的意义, 请不要更改
sys_pool_num = 8
# 执行管理员请求和指令的线程池并行线程数量, 一般和管理员数量相等
admin_pool_num = 2
# 执行用户请求和指令的线程池并行线程数量, 如需要更高的并发, 可以增大该值
user_pool_num = 6



########## plugin.name='QQbot' plugin.path='//plugins//gocqOnQQ//main' ##########
##### QQ设置 #####
# go-cq设置不支持热重载

# QQ 号 必改！
qq = 3457195338  # 测试用QQ号, 请务必修改!

# QQ 管理员列表, 强烈建议有一个, 否则大量指令无法使用
# QQ 管理员不登入账号, 仅做后台发送管理员数据使用
admin_list = [
    1636708665,  # 作者 QQ
]

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



########## plugin.name='GPTBot' plugin.path='//plugins//GPT//main' ##########



########## plugin.name='TimeReminderPlugin' plugin.path='//plugins//timeReminder//main' ##########
setsth = 123
# timeReminder


########## plugin.name='ChatModel' plugin.path='//plugins//ChatWithGPT//main' ##########
# haha


########## plugin.name='banWordsUtil' plugin.path='//plugins//banWords//main' ##########
# 是否启用百度云内容安全审核, 用于接入百度云, 从而智能的拦截机器人发出的不合格图片和消息
# 注册方式查看 https://cloud.baidu.com/doc/ANTIPORN/s/Wkhu9d5iy, 如果开启 baidu_check = True
baidu_check = False

# 百度云API_KEY 24位英文数字字符串
baidu_api_key = ""

# 百度云SECRET_KEY 32位的英文数字字符串
baidu_secret_key = ""

# 不合规消息自定义返回
inappropriate_message_tips = "[百度云]请珍惜机器人, 当前返回内容不合规"

##### 屏蔽词请前往 plugins/banWords/sensitive.json 中修改!!!
