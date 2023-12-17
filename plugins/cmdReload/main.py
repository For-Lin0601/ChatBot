

import Events
from Models.Plugins import *
from plugins.gocqOnQQ.entities.components import At, Plain


@register(
    description="热重载[re, reload]",
    version="1.0.0",
    author="For_Lin0601",
    priority=207
)
class ReloadCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value.append(
            "!reload - 执行热重载"
        )

    @on(GetQQPersonCommand)
    @on(GetQQGroupCommand)
    def cmd_reload(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if message not in ["re", "reload"]:
            return
        event.prevent_postorder()
        if not kwargs["is_admin"]:
            if kwargs["launcher_id"] == kwargs["sender_id"]:  # 私聊
                self.emit(Events.GetCQHTTP__).sendPersonMessage(
                    kwargs["sender_id"], "[bot] 权限不足")
            else:
                self.emit(Events.GetCQHTTP__).sendGroupMessage(
                    kwargs["launcher_id"], [
                        Plain(text="[bot]warning: "),
                        At(qq=kwargs["sender_id"]),
                        Plain(text="权限不足")
                    ])
            return

        self.set_reload_config("reload_command_from", "qq")
        self.emit(Events.SubmitSysTask__, fn=Plugin._reload)

    @on(GetWXCommand)
    def wx_send(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        if message not in ["re", "reload"]:
            return
        event.prevent_postorder()
        sender = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        if not kwargs["is_admin"]:
            self.emit(Events.GetWCF__).send_text("[bot] 权限不足", sender)
            return

        self.set_reload_config("reload_command_from", sender)
        self.emit(Events.SubmitSysTask__, fn=Plugin._reload)

    @on(PluginsReloadFinished)
    def on_plugins_reload_finished(self, event: EventContext, **kwargs):
        reload_command_from = self.get_reload_config("reload_command_from")
        if reload_command_from == "qq":
            self.emit(Events.GetCQHTTP__).NotifyAdmin("[bot] 插件热重载完成")
        else:
            self.emit(Events.GetWCF__).send_text(
                "[bot] 插件热重载完成", reload_command_from)
