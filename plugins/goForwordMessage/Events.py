
ForwardMessage__ = "forward_message__"
"""包装转发消息, 传入字符串则按一千字左右一分割, 列表则一个元素一分割
```python
    kwargs:
        message: Union[str, list]              # 消息
        qq: Union[int, list] = bot.user_id     # 发送人
        name: Union[str, list] = bot.nickname  # 发送人昵称 可为"default", 会根据kwargs.qq自动查询昵称
        # 若 qq 或 name 为空, 会使用登入号的 QQ号 或 QQ昵称
        # 注意要为列表的话, 三个必须一起为列表, 且长度一致, 将会一一对应转化(name可为"default")
        # message列表可为 list[str] , 也可为自定义小列表, 小列表内应为 .plugins.gocqOnQQ.entitiles.components 中的合法QQ消息
        # message内不可混淆两种方式, 在此仅检查message[0]的种类, 不做额外检查
        # 由于ntqq更新原因, name字段建议省略或填写"default", ntqq不支持自定义名字, 写了也无视

    return:
        Union[list, bool]       # 消息链
```"""
