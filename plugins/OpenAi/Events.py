GetOpenAi__ = "get_openai__"
"""获取OpenAi对象时触发
```python
    kwargs:
        None

    return:
        openai: pkg.openai.OpenAI
```"""

SessionExpired = "session_expired"
"""会话过期时触发
```python
    kwargs:
        session_name: str 会话名称(<launcher_type>_<launcher_id>)
        session: pkg.openai.session.Session 会话对象
        session_expire_time: int 已设置的会话过期时间(秒)
```"""

KeyExceeded = "key_exceeded"
"""api-key超额时触发
```python
    kwargs:
        key_name: str 超额的api-key名称
        usage: dict 超额的api-key使用情况
        exceeded_keys: list[str] 超额的api-key列表
```"""

KeySwitched = "key_switched"
"""api-key超额切换成功时触发, 此事件不支持阻止默认行为
```python
    kwargs:
        key_name: str 切换成功的api-key名称
        key_list: list[str] api-key列表
```"""
