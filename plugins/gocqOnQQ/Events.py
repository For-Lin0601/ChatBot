GetCQHTTP__ = "get_cqhttp__"
"""获取CQHTTP对象
```python
    kwargs:
        None

    return:
        CQHTTP_pretocol: CQHTTP对象, 发送QQ消息使用, 具体请看 plugins.gocqOnQQ.CQHTTP_pretocol
```"""

QQClientSuccess = "QQ_client_success"
"""QQ客户端连接成功(仅在程序启动时触发)(`QQ_`开头一律不用返回)
```python
    kwargs:
        None
```"""


# `QQ_`开头的一律不返回, 插件自行处理并提交下方`post`事件


##### 以下是WebSocket事件 #####


##### plugins.gocqOnQQ.QQevents.MessageEvent.py #####
# 普通消息


QQ_private_message = "QQ_private_message"
"""收到QQ消息(`QQ_`开头一律不用返回)
```python
    kwargs:
        PersonMessage:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py
```"""

QQ_group_message = "QQ_group_message"
"""收到QQ消息(`QQ_`开头一律不用返回)
```python
    kwargs:
        GroupMessage:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MessageEvent.py
```"""


#


##### plugins.gocqOnQQ.QQevents.RequestEvent.py #####
# 添加请求


QQ_friend_add_event = "QQ_friend_add_event"
"""好友添加请求(`QQ_`开头一律不用返回)
```python
    kwargs:
        FriendAdd:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.RequestEvent.py
```"""

QQ_group_add_event = "QQ_group_add_event"
"""群添加请求(`QQ_`开头一律不用返回)
```python
    kwargs:
        GroupAdd:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.RequestEvent.py
```"""


#


##### plugins.gocqOnQQ.QQevents.NoticeEvent.py #####
# 通知


QQ_client_status = "QQ_client_status"
"""其他客户端在线状态变更(`QQ_`开头一律不用返回)
```python
    kwargs:
        ClientStatusChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_friend_recall = "QQ_friend_recall"
"""好友消息撤回(`QQ_`开头一律不用返回)
```python
    kwargs:
        PersonMessageRecall:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""
QQ_friend_add = "QQ_friend_add"
"""好友添加提示
```python
    kwargs:
        FriendAddEvent:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_offline_file = "QQ_offline_file"
"""接收到离线文件
```python
    kwargs:
        OfflineFileupload:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_recall = "QQ_group_recall"
"""群消息撤回
```python
    kwargs:
        GroupMessageRecall:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_increase = "QQ_group_increase"
"""群成员增加
```python
    kwargs:
        GroupIncrease:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_decrease = "QQ_group_decrease"
"""群成员减少
```python
    kwargs:
        GroupDecrease:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_admin = "QQ_group_admin"
"""群管理员变更
```python
    kwargs:
        GroupAdmin:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_upload = "QQ_group_upload"
"""群文件上传
```python
    kwargs:
        GroupUpload:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_ban = "QQ_group_ban"
"""群名片变更提示[此事件不保证时效性, 仅在收到消息时效验卡片]

    当名片为空, 即 card_new 或者 card_old 为空时, 为空字符串, 不是昵称
```python
    kwargs:
        GroupBan:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_card = "QQ_group_card"
"""群名片变更提示[此事件不保证时效性, 仅在收到消息时效验卡片]
```python
    kwargs:
        GroupCardChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_essence = "QQ_essence"
"""精华消息变更提示
```python
    kwargs:
        GroupEssenceChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_lucky_king = "QQ_lucky_king"
"""群运气王红包提示[此事件无法在手表协议上触发!!!]
```python
    kwargs:
        LuckyKing:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_honor = "QQ_honor"
"""群成员荣誉变更提示[此事件无法在手表协议上触发!!!]
```python
    kwargs:
        GroupHonorChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_title = "QQ_title"
"""群成员头衔变更提示
```python
    kwargs:
        GroupTitleChange:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_person_poke = "QQ_person_poke"
"""好友戳一戳(双击头像)
```python
    kwargs:
        FriendPoke:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""

QQ_group_poke = "QQ_group_poke"
"""群聊戳一戳(双击头像)[此事件无法在手表协议上触发!!!]
```python
    kwargs:
        GroupPoke:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.NoticeEvent.py
```"""


#


##### plugins.gocqOnQQ.QQevents.MetaEvent.py #####
# 统计信息
# 默认不发送此类信息


QQ_heartbeat = "QQ_heartbeat"
"""心跳包(`QQ_`开头一律不用返回)
```python
    kwargs:
        Heartbeat:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MetaEvent.py
```"""

QQ_lifecycle = "QQ_lifecycle"
""" 生命周期(`QQ_`开头一律不用返回)
```python
    kwargs:
        Lifecycle:  # 数据存储类, 详情请看 plugins.gocqOnQQ.QQevents.MetaEvent.py
```"""
