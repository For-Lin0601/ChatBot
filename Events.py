########## 主线程必选项 ##########

PluginsLoadingFinished = "plugins_loading_finished"
"""插件首次加载时触发(程序启动时)

    kwargs:
        None

    returns:
        None
"""

PluginsReloadFinished = "plugins_reload_finished"
"""插件重载完成时触发, 等同于在`plugin.__init__`中判断`not self.is_first_init()`后的代码块

    kwargs:
        None

    returns:
        None
"""

# 若希望程序启动和重载完后都触发, 可以使用
# @on(PluginsLoadingFinished)
# @on(PluginsReloadFinished)
# def your_function(self, event: EventContext, **kwargs):
#   ...

Reload = "reload"
"""重载插件时触发

    kwargs:
        None

    returns:
        None
"""



########## plugin.name='Log' plugin.path='//plugins//__log//main' ##########
SetLogs__ = "set_logs__"
"""设置日志(在有插件修改了日志之后)

    kwargs:
        None

    returns:
        None
"""


########## plugin.name='Config' plugin.path='//plugins//__config//main' ##########
GetConfig__ = "get_config__"
"""获取配置

    kwargs:
        config_name: str 配置名称(为空则返回配置字典)

    returns:
        config: ModuleType 配置模块(以 value = config.key 读取)
"""

SetConfig__ = "set_config__"
"""设置配置(暂存到 __config.config 中，不写入 config.py)

    kwargs:
        config: dict 配置字典
"""



########## plugin.name='ThreadCtlPlugin' plugin.path='//plugins//__threadctl//main' ##########
SubmitAdminTask = "SubmitAdminTask"
"""提交后台任务
"""



########## plugin.name='GPTBot' plugin.path='//plugins//GPT//main' ##########
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



########## plugin.name='banWordsUtil' plugin.path='//plugins//banWords//main' ##########
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
