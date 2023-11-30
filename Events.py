########## 主线程必选项 ##########

PluginsLoadingFinished = "plugins_loading_finished"
"""插件加载完成时触发

    kwargs:
        plugins: list[Plugin] 插件列表
"""

PluginsReloadFinished = "plugins_reload_finished"
"""插件重载完成时触发

    kwargs:
        plugins: list[Plugin] 插件列表
"""

Reload = "reload"
"""重载插件时触发

    kwargs:
        None
"""


########## plugin.name='Config' plugin.path='D://workspace ai//chatbot//plugins//__config' ##########
GetConfig__ = "get_config__"
"""获取配置

    kwargs:
        config_name: str 配置名称(为空则返回配置字典)

    returns:
        config: any 配置对象
"""

SetConfig__ = "set_config__"
"""设置配置(不写入 config.py)

    kwargs:
        config: dict 配置字典
"""


########## plugin.name='GPTBot' plugin.path='D://workspace ai//chatbot//plugins//gpt' ##########
SessionExpired = "session_expired"
"""会话过期时触发

    kwargs:
        session_name: str 会话名称(<launcher_type>_<launcher_id>)
        session: pkg.openai.session.Session 会话对象
        session_expire_time: int 已设置的会话过期时间(秒)
"""

KeyExceeded = "key_exceeded"
"""api-key超额时触发

    kwargs:
        key_name: str 超额的api-key名称
        usage: dict 超额的api-key使用情况
        exceeded_keys: list[str] 超额的api-key列表
"""

KeySwitched = "key_switched"
"""api-key超额切换成功时触发, 此事件不支持阻止默认行为

    kwargs:
        key_name: str 切换成功的api-key名称
        key_list: list[str] api-key列表
"""



########## plugin.name='banWordsUtil' plugin.path='D://workspace ai//chatbot//plugins//banwords' ##########
BanWordCheck__ = "ban_word_check__"
"""检查是否包含敏感词

    kwargs:
        message: str 消息

    return:
        bool 是否包含敏感词
"""

BanWordProcess__ = "ban_word_process__"
"""处理敏感词

    kwargs:
        message: str 消息

    return:
        str 处理后的消息
"""
