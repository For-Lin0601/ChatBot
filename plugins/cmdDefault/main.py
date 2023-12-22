

import Events
from Models.Plugins import *
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol
from wcferry import Wcf


@register(
    description="查看所有情景预设[de, default]",
    version="1.0.0",
    author="For_Lin0601",
    priority=205
)
class DefalutCommand(Plugin):

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["default"] = {
            "is_admin": False,
            "alias": ["de"],
            "summary": "查看所有情景预设",
            "usage": (
                "!default\n"
                " - 查看所有情景预设\n"
                "!default ls\n"
                " - [管理员]查看高级权限好友列表\n"
                "!default all\n"
                " - [管理员]查看所有情景预设\n"
                "!default [密码]\n"
                " - 切换高级权限"
            ),
            "description": "- password 请前往`config.py`中配置`default_prompt_permission_password`字段"
        }

    @on(GetQQPersonCommand)
    def cmd_reload(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not (message.startswith("de ") or message == "de" or
                message.startswith("default")):
            return
        if message.startswith("default"):
            message = message[7:].strip()
        elif message.startswith("de "):
            message = message[2:].strip()
        elif message == "de":
            message = ""
        event.prevent_postorder()
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        config = self.emit(Events.GetConfig__)
        sender_id = kwargs["sender_id"]
        params = message.split()

        if len(params) == 0:
            params = [None]
        # 输出目前所有情景预设
        import os
        default_prompt_describe = config.default_prompt_describe
        default_prompt_permission = config.default_prompt_permission
        default_prompt_permission_password = config.default_prompt_permission_password
        prompts = config.default_prompt
        openai = self.emit(Events.GetOpenAi__)
        session = openai.sessions_dict.get(f'person_{sender_id}')
        if session is None:
            session_name = "default"
            is_plus = "default"
            use_gpt4 = "否"
        else:
            session_name = session.role_name
            is_plus = session.params_name if session.params_name else "default"
            use_gpt4 = '是' if session.is_plus else '否'
        reply_str = f"[bot] 当前情景预设：{session_name}\n"
        reply_str += f"当前配置: {is_plus}\n"
        reply_str += f"是否启用GPT4: {use_gpt4}\n\n"
        reply_str += "场景预设和配置详情请看`!cmd reset`\n\n"
        reply_str += "\n情景预设名称列表:\n"
        default_password_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'default_password.txt')

        # 用文件的方式记录已经输入过密码的人
        with open(default_password_path, 'r') as file:
            account_list = file.readlines()
        account_list = [account.strip() for account in account_list]  # 删除末尾换行符
        permission = True if str(
            sender_id) in account_list else False  # False表示只能查看部分
        if params[0] == default_prompt_permission_password and not str(sender_id) in account_list:
            with open(default_password_path, 'a') as file:
                try:
                    friends_list = cqhttp.getFriendList()
                    for friend in friends_list:
                        if friend.user_id == sender_id:
                            friend_name = friend.remark
                            break
                    cqhttp.sendPersonMessage(
                        sender_id, "[{}]通过default_password验证".format(sender_id))
                    cqhttp.NotifyAdmin(
                        "[{}][{}]通过default_password验证".format(friend_name, sender_id))
                    file.write('{}\n'.format(sender_id))
                    permission = True
                except Exception as e:
                    cqhttp.sendPersonMessage(
                        sender_id, f"[bot]err: 意外的错误! 请联系管理员处理!{e}")
            return

        # 查看通过default_password验证的用户
        elif params[0] == "ls":
            if kwargs["is_admin"]:
                account_reply = ""
                friends_list = cqhttp.getFriendList()
                for qq_id in account_list:
                    for friend in friends_list:
                        if friend.user_id == int(qq_id):
                            account_reply += f"\n[{friend.remark}][{qq_id}]"
                            break
                    else:
                        account_reply += f"\n[未知][{qq_id}]"
                cqhttp.sendPersonMessage(
                    sender_id, "通过default_password验证的列表: {}".format(account_reply))
            else:
                cqhttp.sendPersonMessage(sender_id, "[bot] 权限不足")
            return

        # 查看所有情景预设的详细信息
        elif params[0] == "all":
            if kwargs["is_admin"]:
                i = 1
                for key in prompts:
                    reply_str += f"   - [{i}]{key}\n"
                    i += 1
                reply_str += "\n\n详细信息:\n\n"
                i = 1
                segments = []

                # 四个一组, 输出为转发消息
                for key in prompts:
                    reply_str += f"[{i}] 名称: {key}"
                    reply_str += f"\n{prompts[key]}"
                    i += 1
                    segments.append(reply_str)
                    reply_str = ''
                    if (i % 4 == 1 and i != 1) or i == len(prompts)+1:
                        forward = self.emit(
                            Events.ForwardMessage__, message=segments)
                        cqhttp.sendPersonForwardMessage(sender_id, forward)
                        segments = []
            else:
                cqhttp.sendPersonMessage(sender_id, "[bot] 权限不足")
            return

        i = 1
        for key in prompts:
            if key in default_prompt_permission or permission:
                reply_str += "   - [{}]{}\n".format(i, key)
                i += 1
        reply_str += "\n\n详细信息:"
        i = 1
        for key in prompts:
            if key in default_prompt_permission or permission:
                reply_str += "\n\n[{}] 名称: {}".format(i, key)
                i += 1
                if key in default_prompt_describe:
                    reply_str += "\n   - [role] 自我介绍\n   - [content] {}".format(
                        default_prompt_describe[key])
                else:
                    reply_str += "\n   - 该角色尚无自我介绍"

        reply = self.emit(Events.ForwardMessage__, message=reply_str)
        cqhttp.sendPersonForwardMessage(sender_id, reply)
        return

    @on(GetQQGroupCommand)
    def cmd_default(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        if not (message.startswith("de ") or message == "de" or
                message.startswith("default")):
            return
        event.prevent_postorder()
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        cqhttp.sendGroupMessage(
            kwargs["group_id"], "[bot] 群聊暂不支持此命令")

    @on(GetWXCommand)
    def cmd_default(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        if not (message.startswith("de ") or message == "de" or
                message.startswith("default")):
            return
        if message.startswith("default"):
            message = message[7:].strip()
        elif message.startswith("de "):
            message = message[2:].strip()
        elif message == "de":
            message = ""
        event.prevent_postorder()
        wcf: Wcf = self.emit(Events.GetWCF__)
        config = self.emit(Events.GetConfig__)
        sender = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        params = message.split()

        if len(params) == 0:
            params = [None]
        # 输出目前所有情景预设
        import os
        default_prompt_describe = config.default_prompt_describe
        default_prompt_permission = config.default_prompt_permission
        default_prompt_permission_password = config.default_prompt_permission_password
        prompts = config.default_prompt
        openai = self.emit(Events.GetOpenAi__)
        session = openai.sessions_dict.get(f'wx_{sender}')
        if session is None:
            session_name = "default"
            is_plus = "default"
            use_gpt4 = "否"
        else:
            session_name = session.role_name
            is_plus = session.params_name if session.params_name else "default"
            use_gpt4 = '是' if session.is_plus else '否'
        reply_str = f"[bot] 当前情景预设：{session_name}\n"
        reply_str += f"当前配置: {is_plus}\n"
        reply_str += f"是否启用GPT4: {use_gpt4}\n\n"
        reply_str += "场景预设和配置详情请看`!cmd reset`\n\n"
        reply_str += "\n情景预设名称列表:\n"
        default_password_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'default_password_wx.txt')

        # 用文件的方式记录已经输入过密码的人
        with open(default_password_path, 'r') as file:
            account_list = file.readlines()
        account_list = [account.strip() for account in account_list]  # 删除末尾换行符
        permission = True if sender in account_list else False  # False表示只能查看部分
        if params[0] == default_prompt_permission_password and not sender in account_list:
            if kwargs["message"].from_group():
                wcf.send_text(
                    "[bot] 群聊暂不支持无限制模式~", sender)
                return
            with open(default_password_path, 'a') as file:
                try:
                    friends_list = wcf.get_friends()
                    for friend in friends_list:
                        if friend["wxid"] == sender:
                            friend_name = friend["remark"] if friend["remark"] else friend["name"]
                            break
                    wcf.send_text(
                        "[{}]通过default_password验证".format(sender), sender)
                    self.emit(Events.GetCQHTTP__).NotifyAdmin(
                        "微信[{}][{}]通过default_password验证".format(friend_name, sender))
                    file.write('{}\n'.format(sender))
                    permission = True
                except Exception as e:
                    wcf.send_text(
                        f"[bot]err: 意外的错误! 请联系管理员处理!\n{e}", sender)
            return

        # 查看通过default_password验证的用户
        elif params[0] == "ls":
            if kwargs["is_admin"]:
                account_reply = ""
                friends_list = wcf.get_friends()
                for wx_id in account_list:
                    for friend in friends_list:
                        if friend["wxid"] == wx_id:
                            account_reply += f'\n[{friend["remark"] if friend["remark"] else friend["name"]}][{wx_id}]'
                            break
                    else:
                        account_reply += f"\n[未知][{wx_id}]"
                wcf.send_text(
                    "通过default_password验证的列表: {}".format(account_reply), sender)
            else:
                wcf.send_text("[bot] 权限不足", sender)
            return

        # 查看所有情景预设的详细信息
        elif params[0] == "all":
            if kwargs["is_admin"]:
                wcf.send_text("[bot] 请前往QQ查看", sender)
            else:
                wcf.send_text("[bot] 权限不足", sender)
            return

        i = 1
        for key in prompts:
            if key in default_prompt_permission or permission:
                reply_str += "   - [{}]{}\n".format(i, key)
                i += 1
        reply_str += "\n\n详细信息:"
        i = 1
        for key in prompts:
            if key in default_prompt_permission or permission:
                reply_str += "\n\n[{}] 名称: {}".format(i, key)
                i += 1
                if key in default_prompt_describe:
                    reply_str += "\n   - [role] 自我介绍\n   - [content] {}".format(
                        default_prompt_describe[key])
                else:
                    reply_str += "\n   - 该角色尚无自我介绍"

        wcf.send_text(reply_str, sender)
        return
