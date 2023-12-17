GetWCF__ = "get_wcf__"
"""获取wcf对象
```python
    kwargs:
        None

    return:
        wcf:  # wcf对象, 发送微信消息使用
        # 具体请看 from wcferry import Wcf
```"""


# `WX_`开头的一律不返回, 插件自行处理并提交下方`post`事件


WXClientSuccess = "wx_client_success"
"""微信客户端连接成功(仅在程序启动时触发)(`WX_`开头一律不用返回)
```python
    kwargs:
        None
```"""


##### 微信事件只有WxMsg一种 #####


Wx_msg = "wx_msg"
"""收到微信消息(`WX_`开头一律不用返回)
```python
    kwargs:
        Wx_msg: WxMsg   # 数据存储类
        is_admin: bool  # 是否为管理员
```"""
