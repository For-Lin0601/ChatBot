
# 消息处理超时重试次数(0为不重试, 负数为取消消息默认处理, 不建议)
wx_retry_times = 1

# 消息处理的超时时间, 单位为秒
# 此处不填写, 与QQ机器人保持一致
# process_message_timeout = 180

# 禁用列表
# 填写其wxid, 会被禁止与机器人进行私聊或群聊交互
# 私聊和群聊都有wxid
wx_banned_list = []


# 是否响应群消息(默认False不响应, 群聊更容易被风控)
quote_wx_group = False

# 仅在quote_wx_group为True时有效
# 群内响应规则, 符合此消息的群内消息即使不包含at机器人也会响应
# 支持消息前缀匹配及正则表达式匹配
# 注意每个规则的优先级为: 消息前缀 > 正则表达式 > 随机响应
# 且字典不能缺失字段, 若不需要, 可为空
# 正则表达式简明教程: https://www.runoob.com/regexp/regexp-tutorial.html
wx_response_rules = {
    "default": {  # 默认, 若未特殊标注则引用此处规则
        "at": False,  # 是否响应at机器人的消息, ps: 就是群聊艾特会不会回, 如果为False则不回
        "prefix": [],
        "regexp": [],
        "random_rate": 0.0,  # 随机响应概率, 取值范围 0.0-1.0     0.0为完全不随机响应  1.0响应所有消息, 仅在前几项判断不通过时生效
    },
    "45786776627@chatroom": {  # 测试群
        "at": True,
        "prefix": ["/", "!", "！", "ai"],
        "regexp": ["怎么?样.*", "怎么.*", "如何.*", ".*咋办"],
        "random_rate": 0.0,
    },
}
