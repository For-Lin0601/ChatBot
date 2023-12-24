
import re

import Events
from Models.Plugins import *
from ..cmdDefault.CheckPermission import check_permission
from ..OpenAi.main import Session, OpenAiInteract
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol
from wcferry import Wcf


@register(
    description="重置当前情景预设[r, reset]",
    version="1.0.0",
    author="For_Lin0601",
    priority=206
)
class ResetCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["reset"] = {
            "is_admin": False,
            "alias": ["r"],
            "summary": "重置当前情景预设",
            "usage": (
                "!reset <预设名|预设编号>\n"
                " - 用`!default`查看所有预设\n"
                "!reset -<配置名>\n"
                " - 切换配置, 注意短横线\n"
                "!reset <预设名|预设编号> -<配置名>\n"
                " - 前两者命令结合\n"
                "!reset ls\n"
                " - [管理员]查看当前所有人配置\n"
                "!reset all\n"
                " - 查看当前配置可选项"
            ),
            "description": (
                "[场景预设] 举例: `!reset 提词器`, 或者缩写为`!r 2`(请注意提词器的编号不一定为2)\n"
                "也称之为角色扮演, 或者感觉对话太卡顿可以用`!reset`重置。清除历史记录可能会优化一点对话体验\n"
                "[修改配置] 举例: `!reset 提词器 -gpt4`, 或者缩写为`!r2-gpt4`(空格可完全省略)\n"
                "默认情况切`gpt4`需要[高级权限], 详情请看`!cmd default`\n"
                "可以自己提供预设给管理员, 让管理员写入`config.py`中的`default_prompt`字段, 即可使用。注意`config.py`中该字段的上下文, 有几个相邻的字段都需要完善。相关提示写在`config.py`中\n"
                "配置名请到`config.py`中配置`completion_api_params`字段, 默认只有`default`和`gpt4`两种"
            )
        }

    @on(GetQQPersonCommand)
    def cmd_reset(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        pattern_reset = r'^r[^a-zA-Z]+'
        if not (re.search(pattern_reset, message) or message == "r" or message.startswith("reset")):
            return
        event.prevent_postorder()
        if message.startswith("reset"):
            message = message[5:].strip()
        else:
            message = message[1:].strip()
        params = message.replace("-", " -").split()
        params = [param for param in params if param.strip() != ""]
        sender_id = kwargs["sender_id"]
        session_name = f"person_{sender_id}"
        reply = self.set_reset(
            sender_id, session_name, params, kwargs["is_admin"])
        self.emit(Events.GetCQHTTP__).sendPersonMessage(sender_id, reply)

    @on(GetQQGroupCommand)
    def cmd_reset(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        pattern_reset = r'^r[^a-zA-Z]+'
        if not (re.search(pattern_reset, message) or message == "r" or message.startswith("reset")):
            return
        event.prevent_postorder()
        cqhttp = self.emit(Events.GetCQHTTP__)
        cqhttp.sendGroupMessage(kwargs["group_id"], "[bot] 群聊暂不支持此命令")

    @on(GetWXCommand)
    def cmd_reset(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        pattern_reset = r'^r[^a-zA-Z]+'
        if not (re.search(pattern_reset, message) or message == "r" or message.startswith("reset")):
            return
        event.prevent_postorder()
        if message.startswith("reset"):
            message = message[5:].strip()
        else:
            message = message[1:].strip()
        params = message.replace("-", " -").split()
        params = [param for param in params if param.strip() != ""]
        sender = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        session_name = f"wx_{sender}"

        reply = self.set_reset(
            sender, session_name, params, kwargs["is_admin"])
        self.emit(Events.GetWCF__).send_text(reply, sender)

    def set_reset(self, sender_id, session_name, params, is_admin) -> str:
        """统一接口"""
        config = self.emit(Events.GetConfig__)
        open_ai: OpenAiInteract = self.emit(GetOpenAi__)
        if len(params) == 0 or params[0].startswith("-"):
            open_ai.sessions_dict[session_name] = Session(
                session_name, "default", config.default_prompt["default"], config.session_expire_time)
            reply = config.command_reset_message

            if params and params[0].startswith("-"):
                text = params[0][1:]
                if not check_permission(sender_id):
                    reply += f"\n[启用配置{text}]warning: 权限不足, 启用默认配置"
                else:
                    if text in config.completion_api_params:
                        open_ai.sessions_dict[session_name]\
                            .set_plus_params(text)
                        reply += f"\n[启用配置{text}]: success"
                    else:
                        reply += f"\n无效的配置名[{text}], 启用默认配置"
            return reply

        permission = check_permission(sender_id)
        if params[0] == "all":
            if permission:
                reply = "[bot] 可用配置:\n"
                reply += "模型倍率与分组倍率与账单成比例, 请按需自取\n\n"
                for index, (key, value) in enumerate(config.completion_api_params.items()):
                    reply += f"[{index+1}] -{key}:\n"
                    reply += f"  描述: {value['description']}\n" if "description" in value else ""
                    reply += f"  最大token: {value['max_tokens']}\n" if "max_tokens" in value else ""
                    reply += f"  训练数据截止: {value['traning_data']}\n" if "traning_data" in value else ""
                    reply += f"  模型倍率: {value['model_multi']}\n" if "model_multi" in value else ""
                    reply += f"  分组倍率: {value['group_multi']}\n" if "group_multi" in value else ""
                    reply += "\n"
                return reply.strip()
            return "[bot] 权限不足"

        if params[0] == "ls":
            if is_admin:
                reply = "[bot] 当前所有人配置:"
                # plus写在前面
                open_ai.sessions_dict = dict(sorted(
                    open_ai.sessions_dict.items(),
                    key=lambda x: (x[1].is_plus, x[0])
                ))
                for index, (session_name, session) in enumerate(open_ai.sessions_dict.items()):
                    reply += f"\n\n[{index+1}]{session.statistical_usage()}"
                return reply
            return "[bot] 权限不足"

        try:
            prompts = config.default_prompt
            key_list = list(prompts.keys())

            if not permission:
                key_list = [
                    key for key in key_list if key in config.default_prompt_permission]
            if params[0].isdigit() and int(params[0]) <= len(key_list):
                index = int(params[0])-1
                params[0] = key_list[index]
            if not permission and params[0] not in key_list:
                return "[bot]会话重置失败: 没有找到场景预设: {}".format(params[0])
            open_ai.sessions_dict[session_name] = Session(
                session_name, params[0], prompts[params[0]], config.session_expire_time)
            reply = config.command_reset_name_message + "{}".format(params[0])
            reply += f"\n当前预设长度: {len(prompts[params[0]])}字符, 请注意api key消耗"

            if len(params) > 1 and params[1].startswith("-"):
                text = params[1][1:]
                if not permission:
                    reply += f"\n[启用配置{text}]warning: 权限不足, 启用默认配置"
                else:
                    if text in config.completion_api_params:
                        if "is_plus" in config.completion_api_params[text] and \
                                config.completion_api_params[text]["is_plus"]:
                            open_ai.sessions_dict[session_name]\
                                .set_plus_params(text)
                            reply += f"\n[启用GPT4配置{text}]: success"
                            if len(prompts[params[0]]) > 100:
                                reply += "\n当前预设长度较长, 请注意api key消耗!!!"
                        else:
                            open_ai.sessions_dict[session_name]\
                                .set_params(text)
                            reply += f"\n[启用配置{text}]: success"
                    else:
                        reply += f"\n无效的配置名[{text}], 启用默认配置"
        except Exception as e:
            reply = "[bot]会话重置失败: {}".format(e)

        return reply
