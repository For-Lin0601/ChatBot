GetConfig__ = "get_config__"
"""获取配置
```python
    kwargs:
        None

    return:
        config: ModuleType  # 配置模块(以 value = config.key 读取)
```"""

SetConfig__ = "set_config__"
"""设置配置(暂存到 __config.config 中, 不写入 config.py, 热重载后丢失, 请谨慎使用)
```python
    kwargs:
        config: dict  # 配置字典

    return:
        None  # 存在会覆盖
```"""
