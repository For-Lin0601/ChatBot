

import re

import Events
from Models.Plugins import *
from plugins.gocqOnQQ.QQevents.MessageEvent import PersonMessage
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol


@register(
    description="向管理员发送信息[s, sent]",
    version="1.0.0",
    author="For_Lin0601",
    priority=203
)
class SentCommand(Plugin):

    def __init__(self):
        self.launcherId_history = 0
        self.answer_history = ""
        self.results = []

    @on(CmdCmdHelp)
    def help(self, event: EventContext, **kwargs):
        event.return_value["sent"] = {
            "is_admin": False,
            "alias": ["s"],
            "summary": "向管理员发送信息",
            "usage": "!sent <信息>",
            "description": (
                "仅支持发送纯文本消息, 若有图片等信息, 只取最前面第一段文字\n"
                "这个尖括号是表示写入信息啊, 为什么那么多人原封不动发一个`!s <信息>`过来, 拜托完全不知道怎么处理了\n"
                "管理员使用需加上对方qq号, `!sent [qq号] <信息>`\n"
                "qq号可以缩写, 会判断寻找最接近的一个好友, 然后可以用简短的数字来选择好友\n"
                "比如可以连续发送`!s 12345`, `!s 1 你好`。即可向`123456`发送消息(末尾6被省略)\n"
                "亦或者用`!s ls`查看当前好友列表(这里允许向群发送, 但不允许群里向管理员发送, 太吵啦)\n"
                "然后可选范围就会很大, 比如有一百个好友, 那么就可以用`!s 100`或者`!s ls100`快速选择到最后一位好友\n"
                "若未输入发送的内容, 将会把选定的qq号暂存, 可以用`!s <信息>`快速发送到暂存的好友\n"
                "暂存的配置是所有管理员共用的, 所以高峰期还请尽量打全qq号, 仅在只有一个人使用的时候这些逻辑判断才会比较顺手\n"
                "此外管理员发送的消息中还可携带命令, 完全以对方身份执行, 但无`message_chain`原型(一般也不用这玩意吧)\n"
                "比如`!s 123456 !help`会向`123456`发送帮助信息, 当然也可以发送携带参数的命令, 都没问题"
            )
        }

    @on(GetQQPersonCommand)
    def cmd_send(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        pattern_alarm = r'^s[^a-zA-Z]+'
        if not (re.search(pattern_alarm, message) or message == "s" or message.startswith("sent")):
            return
        event.prevent_postorder()
        if message.startswith("sent"):
            message = message[4:].strip()
        elif message.startswith("s"):
            message = message[1:].strip()
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        sender_id = kwargs["sender_id"]

        # 发起者为管理员
        if kwargs["is_admin"]:
            self.sent_from_admin(
                message, sender_id, cqhttp, kwargs["message_chain"])
            return

        reply = "[bot] 已向管理员发送信息[{}]".format(
            message[:min(20, len(message))] + ("   ..." if len(message) > 20 else ""))
        if len(message) == 0:
            reply = "[bot]err: 请输入要发送的信息"

        else:
            cqhttp.NotifyAdmin("[{}]向你发送消息:\n{}".format(sender_id, message))
            self.launcherId_history = sender_id

        cqhttp.sendPersonMessage(sender_id, reply)
        return

    @on(GetQQGroupCommand)
    def group_send(self, event: EventContext, **kwargs):
        message: str = kwargs["message"].strip()
        pattern_alarm = r'^s[^a-zA-Z]+'
        if not (re.search(pattern_alarm, message) or message == "s" or message.startswith("sent")):
            return
        event.prevent_postorder()
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        group_id = kwargs["group_id"]
        cqhttp.sendGroupMessage(group_id, "[bot] 群聊暂不支持此命令")

    @on(GetWXCommand)
    def wx_send(self, event: EventContext, **kwargs):
        message: str = kwargs["command"].strip()
        pattern_alarm = r'^s[^a-zA-Z]+'
        if not (re.search(pattern_alarm, message) or message == "s" or message.startswith("sent")):
            return
        event.prevent_postorder()
        sender = kwargs["roomid"] if kwargs["roomid"] else kwargs["sender"]
        self.emit(Events.GetWCF__).send_text("[bot] 微信暂不支持此命令", sender)

    def sent_from_admin(
            self,
            message,
            sender_id,
            cqhttp: CQHTTP_Protocol,
            message_chain: PersonMessage = None  # 只有在管理员发送命令的时候用一下, 目前只兼容了PersonMessage
    ) -> None:
        """以管理员身份发起对话"""
        params = message.split()

        friends_list = cqhttp.getFriendList()
        groups_list = cqhttp.getGroupList()
        id_list = [friend.user_id for friend in friends_list] + \
            [group.group_id for group in groups_list]

        def _find(id: str) -> str:
            """寻找id对应的对象昵称"""
            qq_id = int(id)
            for friend in friends_list:
                if friend.user_id == qq_id:
                    return friend.remark
            for group in groups_list:
                if group.group_id == qq_id:
                    return f"group_{group.group_name}"

        def _msg_add(i: int) -> str:
            """列表显示设置"""
            i = int(i)
            msg = "\n可选择:"
            for j in range(1, min(6, len(self.results)+1)):
                if i == j:
                    msg += "\n【{}】【{}】【{}】".format(
                        j, self.results[j-1], _find(self.results[j-1]))
                else:
                    msg += "\n[{}][{}][{}]".format(
                        j, self.results[j-1], _find(self.results[j-1]))
            if i <= 8:
                for j in range(6, min(i+3, len(self.results)+1)):
                    if i == j:
                        msg += "\n【{}】【{}】【{}】".format(
                            j, self.results[j-1], _find(self.results[j-1]))
                    else:
                        msg += "\n[{}][{}][{}]".format(
                            j, self.results[j-1], _find(self.results[j-1]))
                if len(self.results) > i+2:
                    msg += "\n[更多] ……\n查看全部:\n!<sent/s> ls"
            else:
                msg += "\n[更多] ……"
                for j in range(i-2, min(i+3, len(self.results)+1)):
                    if i == j:
                        msg += "\n【{}】【{}】【{}】".format(
                            j, self.results[j-1], _find(self.results[j-1]))
                    else:
                        msg += "\n[{}][{}][{}]".format(
                            j, self.results[j-1], _find(self.results[j-1]))
                if len(self.results) > i+2:
                    msg += "\n[更多] ……"
                msg += "\n查看全部:\n!<sent/s> ls"
            return msg

        # 判断内容是否为特殊指令ls
        if len(params) >= 1 and \
                (params[0] == 'ls' or (params[0].startswith('ls') and params[0][2:].isdigit())):

            # 如果输入"ls + ' ' + 汉字"格式则报错
            if not (' '.join(params) == 'ls' or (''.join(params).startswith('ls') and ''.join(params)[2:][0].isdigit())):
                cqhttp.sendPersonMessage(sender_id, "[bot]err: 请输入合法的对象编号")
                return
            self.results = id_list[:]

            # 取出输入的成员编号
            i = 0
            params_replaceLS = ''
            params_replaceLS_i = ''.join(params)[2:]
            try:
                while params_replaceLS_i[i].isdigit():
                    params_replaceLS += params_replaceLS_i[i]
                    i += 1
            except:
                pass
            reply_pd = False  # 是否查找到对应对象
            msg = "[bot] "
            if self.launcherId_history != 0:
                msg += "默认发送: [{}][{}]".format(self.launcherId_history,
                                               _find(self.launcherId_history))
            msg += "\n全部对象:"

            # 循环取出所有对象
            i = 0
            for i in range(1, len(self.results)+1):
                if self.results[i-1] == self.launcherId_history:
                    msg += "\n【{}】【{}】【{}】".format(
                        i, self.results[i-1], _find(self.results[i-1]))
                else:
                    msg += "\n[{}][{}][{}]".format(
                        i, self.results[i-1], _find(self.results[i-1]))
                if str(i) == params_replaceLS:
                    reply_pd = True
                    self.launcherId_history = self.results[i-1]
                    msg = "[bot] 已将默认选择切换至[{}][{}]".format(
                        self.launcherId_history, _find(self.launcherId_history))
                    msg += _msg_add(i)
                    break

            # 如果有输入信息，则继续判断输入
            if not reply_pd and params_replaceLS != '':
                cqhttp.sendPersonMessage(sender_id, "[bot]err: 请输入合法的对象编号")
                return
            params[0] = params[0][2:]
            if params[0] == '':
                params.pop(0)
            if len(params) == 0 or (len(params) == 1 and self.answer_history == ''):
                cqhttp.sendPersonMessage(sender_id, msg)
                return
            else:
                params[0] = str(self.launcherId_history)

        # 开始判断输入
        if len(params) < 1:
            if self.launcherId_history == 0 and len(self.results) == 0:
                cqhttp.sendPersonMessage(sender_id, "[bot]err: 请输入内容")
                return
            else:
                msg = "[bot] "
                if self.launcherId_history != 0:
                    msg += "默认发送: [{}][{}]".format(
                        self.launcherId_history, _find(self.launcherId_history))
                if len(self.results) != 0:
                    msg += "\n可选择:"
                    for i in range(1, len(self.results)+1):
                        if self.results[i-1] == self.launcherId_history:
                            msg += "\n【{}】【{}】【{}】".format(
                                i, self.results[i-1], _find(self.results[i-1]))
                        else:
                            msg += "\n[{}][{}][{}]".format(
                                i, self.results[i-1], _find(self.results[i-1]))
                reply = msg

        # 找不到历史记录，并且没有输入过目标QQ号，但允许暂存输入的信息
        elif self.launcherId_history == 0 and not params[0].isdigit():
            self.answer_history = ' '.join(params)
            cqhttp.sendPersonMessage(sender_id, "[bot]err: 请输入对象QQ,将发送信息: [{}]".format(
                self.answer_history[:min(20, len(self.answer_history))] + ("   ..." if len(self.answer_history) > 20 else "")))
            return

        # 输入的数字并非可查询的目标QQ号，查找给出3个较接近的选择
        elif params[0].isdigit() and not (int(params[0]) in id_list or int(params[0]) <= len(self.results)):
            distances = {}  # 记录每个QQ号与目标QQ号的距离
            for qq in id_list:
                m, n = len(str(qq)), len(params[0])
                dp = [[0] * (n + 1) for _ in range(m + 1)]
                for i in range(m + 1):
                    dp[i][0] = i
                for j in range(n + 1):
                    dp[0][j] = j
                for i in range(1, m + 1):
                    for j in range(1, n + 1):
                        if str(qq)[i - 1] == params[0][j - 1]:
                            dp[i][j] = dp[i - 1][j - 1]
                        else:
                            dp[i][j] = min(
                                dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                distances[qq] = dp[m][n]
            self.results = sorted(
                distances.keys(), key=lambda x: distances[x])[:3]

            msg = "[bot] "
            if self.launcherId_history != 0:
                msg += "默认发送: [{}][{}]".format(
                    self.launcherId_history, _find(self.launcherId_history))
            if len(self.results) != 0:
                msg += "\n可选择(更新):"
                for i in range(1, len(self.results)+1):
                    if self.results[i-1] == self.launcherId_history:
                        msg += "\n【{}】【{}】【{}】".format(
                            i, self.results[i-1], _find(self.results[i-1]))
                    else:
                        msg += "\n[{}][{}][{}]".format(
                            i, self.results[i-1], _find(self.results[i-1]))
            reply = msg

        # 管理员请勿向自身发送信息
        elif int(params[0]) == sender_id if params[0].isdigit() else \
                self.launcherId_history == sender_id:
            cqhttp.sendPersonMessage(sender_id, "[bot]err: 请勿向自身发送信息")
            return

        # 目标QQ号已确认，开始发送
        else:
            try:
                # 将目标QQ号放入 self.launcherId_history，信息放入 answer
                number = int(params[0])-1
                if number < len(self.results):
                    params[0] = self.results[number]
                self.launcherId_history = int(params[0])
                answer = ' '.join(params[1:])

                # 查询是否有暂存的信息，若有则继续发送
                if answer == '':
                    if len(self.answer_history) == 0:
                        msg = "[bot] 已将默认选择切换至[{}][{}]".format(
                            self.launcherId_history, _find(self.launcherId_history))
                        if len(self.results) != 0:
                            for i, result in enumerate(self.results):
                                if result == self.launcherId_history:
                                    msg += _msg_add(i+1)
                                    break
                        cqhttp.sendPersonMessage(sender_id, msg)
                        return
                    else:
                        answer = self.answer_history
                        self.answer_history = ''

            # 未输入目标QQ号，用上次记录的self.launcherId_history作为目标QQ号
            except ValueError:
                answer = ' '.join(params)

            # 判断信息是否为命令
            if (answer.startswith("!") or answer.startswith("！")):
                if self.launcherId_history in [friend.user_id for friend in friends_list]:
                    try:
                        message_chain.user_id = self.launcherId_history
                        message_chain.message[0].text = message_chain.message[0].text[1:].strip()
                        # 以对方身份执行命令
                        self.emit(
                            GetQQPersonCommand,
                            message=answer.replace("!", "").replace("！", ""),
                            message_chain=message_chain,
                            launcher_id=self.launcherId_history,
                            sender_id=self.launcherId_history,
                            is_admin=self.launcherId_history in self.emit(GetConfig__).admin_list)

                        cqhttp.sendPersonMessage(
                            self.launcherId_history, "[admin]\n管理员以你的身份发起了命令:\n[{}]".format(answer))

                        reply = "[bot] 成功以[{}][{}]的身份执行命令:\n[{}]".format(
                            _find(self.launcherId_history), self.launcherId_history, answer)
                    except Exception as e:
                        reply = f"[bot]err: {e}"
                else:
                    reply = "[bot]err: 暂不支持将命令发送到群组"

            else:
                import re
                # "数字+感叹号+字母+任意字符" 这个格式很像命令 "!sent 20!talk" 这种形式，故判定为疑似命令
                pattern = r'^\d+[!！][a-zA-Z]+.*$'
                match = re.search(pattern, answer)
                if match:
                    self.answer_history = answer
                    reply = '[bot]err: 信息未发出！该信息疑似命令，请重新组织语言，或用 "!sent" 再次确认发送\n正则表达式: ^\d+[!！][a-zA-Z]+.*$'
                else:
                    # 发送信息
                    if self.launcherId_history in [friend.user_id for friend in friends_list]:
                        cqhttp.sendPersonMessage(
                            self.launcherId_history, "[admin]\n{}".format(answer))
                        reply = "[bot] 信息: [{}]\n成功发送至[{}][{}]".format(
                            answer[:min(20, len(answer))] +
                            ("   ..." if len(answer) > 20 else ""),
                            _find(self.launcherId_history), self.launcherId_history
                        )
                    else:
                        cqhttp.sendGroupMessage(
                            self.launcherId_history, "[admin]\n{}".format(answer))
                        reply = "[bot] 信息: [{}]\n成功发送至[{}][{}]".format(
                            answer[:min(20, len(answer))] +
                            ("   ..." if len(answer) > 20 else ""),
                            _find(self.launcherId_history), self.launcherId_history
                        )

        cqhttp.sendPersonMessage(sender_id, reply)
        return
