import logging



########## plugin.name='Log' plugin.path='//plugins//__log//main' ##########

# 日志级别
logging_level = logging.DEBUG


########## plugin.name='ThreadCtlPlugin' plugin.path='//plugins//__threadctl//main' ##########
# 线程池相关配置, 该参数决定机器人可以同时处理几个人的消息, 超出线程池数量的请求会被阻塞, 不会被丢弃, 如果你不清楚该参数的意义, 请不要更改
# 线程池不完全支持热重载, 其中系统线程不支持重载, 管理员线程和用户线程可能需要在第二次热重载时才会更新配置, 但由于线程池本体足够使用, 暂不考虑完善此处
sys_pool_num = 8
# 执行管理员请求和指令的线程池并行线程数量, 一般和管理员数量相等
admin_pool_num = 2
# 执行用户请求和指令的线程池并行线程数量, 如需要更高的并发, 可以增大该值
user_pool_num = 6



########## plugin.name='OpenAIInteract' plugin.path='//plugins//OpenAi//main' ##########
# ---------------------------------------------模型参数---------------------------------------------

# [必需] OpenAI的配置，api_key: OpenAI的API Key
# 1.若只有一个api-key，请直接修改以下内容中的"openai_api_key"为你的api-key
# 2.如准备了多个api-key，可以以字典的形式填写，程序会自动选择可用的api-key
openai_api_keys = [
    # "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",  # 第一个，用完了
    # "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",  # 第二个，传说120刀，封咯
    # "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",  # 第三个，用完了
    # "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",  # 第四个，同时WeCHatGPT也在用，封咯
    # "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",  # 第五个，用完了
    # "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",  # 封了
    # "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",  # 封了
    # "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",  # 用完
    "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",
    # "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",  # 用完
    "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",
    "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",
]


# OpenAI补全API的参数，OpenAI的文档: https://beta.openai.com/docs/api-reference/completions/create
# 请在下方填写模型，程序自动选择接口,现已支持的模型有：
#    'gpt-4'	             -->新出的更强4.0接口，目前版本似乎仅plus会员等可用
#    'gpt-4-0314'
#    'gpt-4-32k'
#    'gpt-4-32k-0314'
#    'gpt-3.5-turbo'                -->这个是默认的3.5接口，使用方法复制到下面的"model"：xxx  ，替换xxx
#    'gpt-3.5-turbo-0301'
#    'text-davinci-003'             -->这个是原来的3.0接口，人格相对好设置，但是token收费会更高
#    'text-davinci-002'
#    'code-davinci-002' | 'code-cushman-001' | 'text-curie-001' | 'text-babbage-001' | 'text-ada-001'   ....等等、还有一些你可能用不到的模型
completion_api_params = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.8,  # 数值越低得到的回答越理性，取值范围[0, 1]
    "top_p": 1,  # 生成的文本的文本与要求的符合度, 取值范围[0, 1]
    "frequency_penalty": 0.3,
    "presence_penalty": 1.0,
}


# 消息处理的超时时间，单位为秒
process_message_timeout = 180


# 每次向OpenAI接口发送对话记录上下文的字符数
# 注意：较大的prompt_submit_length会导致OpenAI账户额度消耗更快
prompt_submit_length = 4096


# api-key切换策略
# active：每次请求时都会切换api-key
# passive：仅当api-key超额时才会切换api-key
switch_strategy = "active"



########## plugin.name='QQbot' plugin.path='//plugins//gocqOnQQ//main' ##########
##### QQ设置 #####

# QQ 号 必改！
qq = 3457195338  # 测试用QQ号, 请务必修改!(不支持热重载)

# QQ 管理员列表, 强烈建议有一个, 否则大量指令无法使用
# QQ 管理员不登入账号, 仅做后台发送管理员数据使用
# 支持热重载
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



########## plugin.name='TimeReminderPlugin' plugin.path='//plugins//timeReminder//main' ##########
setsth = 123
# timeReminder


########## plugin.name='TextMessagePlugin' plugin.path='//plugins//goTextMessage//main' ##########

# 消息处理超时重试次数(0为不重试, 负数为取消消息默认处理, 不建议)
retry_times = 1

message_drop_tip = "【检测到时空信号交集，请等待返回信号处理完成】"



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
