GetConfig__ = "get_config__"
"""获取配置

    kwargs:
        config_name: str 配置名称(为空则返回配置字典)

    returns:
        config: ModuleType 配置模块(以 value = config.key 读取)
"""

SetConfig__ = "set_config__"
"""设置配置(暂存到 __config.config 中, 不写入 config.py)

    kwargs:
        config: dict 配置字典
"""
