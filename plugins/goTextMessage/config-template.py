
# 消息处理超时重试次数(0为不重试, 负数为取消消息默认处理, 不建议)
retry_times = 1

message_drop_tip = "【检测到时空信号交集，请等待返回信号处理完成】"


# 禁用列表
# person为个人，其中的QQ号会被禁止与机器人进行私聊或群聊交互
# 示例: person = [2854196310, 1234567890, 9876543210]
# group为群组，其中的群号会被禁止与机器人进行交互
# 示例: group = [123456789, 987654321, 1234567890]

# 2854196310是Q群管家机器人的QQ号，默认屏蔽以免出现循环
banned_person_list = [2854196310, 3353064953]
# 204785790是本项目交流群的群号，默认屏蔽，避免在交流群测试机器人
banned_group_list = [204785790, 614876491]
