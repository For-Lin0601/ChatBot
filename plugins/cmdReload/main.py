

import Events
from Models.Plugins import *
from plugins.gocqOnQQ.entities.components import At, Plain


@register(
    description="热重载[re, reload]",
    version="1.0.0",
    author="For_Lin0601",
    priority=203,
)
class ReloadPlugin(Plugin):

    def __init__(self):
        pass

    def on_reload(self):
        pass

    def on_stop(self):
        pass

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value.append(
            "!reload - 执行热重载"
        )

    @on(GetQQPersonCommand)
    @on(GetQQGroupCommand)
    def cmd_reload(self, event: EventContext, **kwargs):
        message: str = kwargs["message"]
        if message not in ["re", "reload"]:
            return
        event.prevent_postorder()
        if not kwargs["is_admin"]:
            if kwargs["launcher_id"] == kwargs["sender_id"]:  # 私聊
                self.emit(Events.GetCQHTTP__).sendFriendMessage(
                    kwargs["sender_id"], "[bot] 权限不足")
            else:
                self.emit(Events.GetCQHTTP__).sendGroupMessage(
                    kwargs["launcher_id"], [
                        Plain(text="[bot]warning: "),
                        At(qq=kwargs["sender_id"]),
                        Plain(text="权限不足")
                    ])
            return

        logging.critical("开始插件热重载")
        self.emit(Events.SubmitSysTask__, fn=Plugin._reload)

    @on(PluginsReloadFinished)
    def on_plugins_reload_finished(self, event: EventContext, **kwargs):
        logging.critical("插件热重载完成")
        self.emit(Events.GetCQHTTP__).NotifyAdmin("[bot] 插件热重载完成")
