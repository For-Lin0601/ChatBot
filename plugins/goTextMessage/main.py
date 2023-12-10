
import random
import re
import time
from func_timeout import FunctionTimedOut, func_set_timeout


import Events
from .Events import *
from Models.Plugins import *

from ..gocqOnQQ.entities.components import At, Plain
from ..gocqOnQQ.CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol
from ..gocqOnQQ.QQevents.MessageEvent import PersonMessage, GroupMessage


@register(
    description="文本消息处理",
    version="1.0.0",
    author="For_Lin0601",
    priority=100
)
class TextMessagePlugin(Plugin):

    def __init__(self):
        pass

    @on(PluginsLoadingFinished)
    def first_init(self, event: EventContext,  **kwargs):
        self.processing = set()

    @on(PluginsReloadFinished)
    def get_config(self, event: EventContext,  **kwargs):
        self.processing = self.get_reload_config("processing")

    def on_reload(self):
        self.set_reload_config("processing", self.processing)

    @on(QQ_private_message)
    def check_cmd_and_chat_with_gpt(self, event: EventContext,  **kwargs):
        self.config = self.emit(Events.GetConfig__)
        message: PersonMessage = kwargs["QQevents"]

        # 忽略自身消息
        if message.sender == self.config.qq:
            return

        # 此处只处理纯文本消息
        if message.message[0].type != "Plain":
            return

        self.cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        event.prevent_postorder()

        # 若有附加消息, 给出警告
        check_length = len(message.message) != 1

        msg: str = message.message[0].text

        if len(msg.replace(" ", "")) == 0:
            self.cqhttp.sendPersonMessage(
                message.user_id, "[bot]warinig: 不能发送空消息"
            )
            return

        def time_ctrl_wrapper():
            tmp_id = []
            for _ in range(self.config.retry_times + 1):
                try:
                    @func_set_timeout(self.config.process_message_timeout)
                    def _time_crtl():
                        self.process_message(
                            "person", message.temp_source if message.temp_source else message.user_id,
                            msg, message.message, message.user_id, check_length
                        )
                    _time_crtl()
                    break
                except FunctionTimedOut:
                    logging.warning(f"{message.user_id}: 超时, 重试中({_})")
                    tmp_id.append(self.cqhttp.sendPersonMessage(
                        message.user_id, f"[bot]warinig: 超时, 重试中({_})"
                    ).message_id)
            else:
                for id_ in tmp_id:
                    self.cqhttp.recall(id_)
        if self.is_admin(launcher_id=message.user_id):
            self.emit(Events.SubmitAdminTask__, fn=time_ctrl_wrapper)
        else:
            self.emit(Events.SubmitUserTask__, fn=time_ctrl_wrapper)

    @on(QQ_group_message)
    def check_cmd_and_chat_with_gpt(self, event: EventContext,  **kwargs):
        self.config = self.emit(Events.GetConfig__)
        if not self.config.quote_qq_group:
            return

        message: GroupMessage = kwargs["QQevents"]
        self.cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)

        # 忽略自身消息
        if message.sender == self.config.qq:
            return

        event.prevent_postorder()

        # 判断群是否符合响应规则
        if str(message.group_id) not in self.config.response_rules:
            response_rules = self.config.response_rules["default"]
        else:
            response_rules = self.config.response_rules[str(message.group_id)]

        if response_rules["at"] and \
            message.message[0].type == "At" and \
                message.message[0].qq == str(self.config.qq):  # 符合at响应规则
            message.message = message.message[1:]
        elif message.message[0].type == "Plain":
            msg = message.message[0].text
            for prefix in response_rules["prefix"]:
                if msg.startswith(prefix):  # 符合prefix响应规则
                    break
            else:
                for regexp in response_rules["regexp"]:
                    if re.search(regexp, msg):  # 符合regexp响应规则
                        break
                else:
                    # ramdom_rate字段随机值0.0-1.0
                    if response_rules["random_rate"] > 0.0 and \
                            random.random() > response_rules["random_rate"]:
                        logging.debug(f"根据规则忽略 {message.user_id}: {msg}")
                        return
        else:
            return

        # 若有附加消息, 给出警告
        check_length = len(message.message) != 1

        msg: str = message.message[0].text

        if len(msg.replace(" ", "")) == 0:
            self.cqhttp.sendGroupMessage(
                message.group_id, [
                    Plain(text="[bot]warning: "),
                    At(qq=message.user_id),
                    Plain(text="[bot]warinig: 不能发送空消息")
                ])
            return

        def time_ctrl_wrapper():
            tmp_id = []
            for _ in range(self.config.retry_times + 1):
                try:
                    @func_set_timeout(self.config.process_message_timeout)
                    def _time_crtl():
                        self.process_message(
                            "group", message.group_id,
                            msg, message.message, message.user_id, check_length
                        )
                    _time_crtl()
                    break
                except FunctionTimedOut:
                    logging.warning(f"{message.user_id}: 超时, 重试中({_})")
                    tmp_id.append(self.cqhttp.sendPersonMessage(
                        message.user_id, f"[bot]warinig: 超时, 重试中({_})"
                    ).message_id)
            else:
                for id_ in tmp_id:
                    self.cqhttp.recall(id_)
        if self.is_admin(launcher_id=message.user_id):
            self.emit(Events.SubmitAdminTask__, fn=time_ctrl_wrapper)
        else:
            self.emit(Events.SubmitUserTask__, fn=time_ctrl_wrapper)

    def is_admin(self, launcher_id: int):
        """检查发送方是否为管理员"""
        return launcher_id in self.config.admin_list

    def is_banned(self, launcher_type: str, launcher_id: int):
        """检查发送方是否被禁用"""
        if launcher_type == "group":
            return launcher_id in self.config.banned_group_list
        return launcher_id in self.config.banned_person_list

    def process_message(
            self,
            launcher_type: str,
            launcher_id: int,
            text_message: str,
            message_chain: list,
            sender_id: int,
            check_length: bool
    ) -> None:
        """处理消息

        :param launcher_type: 发起对象类型
        :param launcher_id: 发起对象ID(可能为群号, 或临时会话)
        :param text_message: 消息文本
        :param message_chain: 消息链
        :param sender_id: 发送者ID
        :param check_length: 是否为纯文本消息

        :return: None
        """
        session_name = "{}_{}".format(launcher_type, launcher_id)

        # 检查发送方是否被禁用
        if self.is_banned(launcher_type, launcher_id):
            logging.info(f"根据禁用列表忽略{session_name}的消息")
            return

        # 触发命令
        if text_message[0] in ["!", "！"]:
            self.emit(GetQQPersonCommand if launcher_type == "person" else GetQQGroupCommand,
                      message=text_message[1:],
                      message_chain=message_chain,
                      launcher_id=launcher_id,
                      sender_id=sender_id,
                      is_admin=self.is_admin(sender_id)
                      )
            return

        # 限速策略
        if session_name in self.processing:
            if launcher_type == "person":
                self.cqhttp.sendPersonMessage(
                    sender_id, self.config.message_drop_tip,
                    group_id=launcher_id if launcher_id != sender_id else None)
            return
        self.processing.add(session_name)
        cqhttp: CQHTTP_Protocol = self.emit(Events.GetCQHTTP__)
        tmp_msg = "[bot]收到消息, " + \
            (f"当前{len(self.processing)-1}人正在排队" if len(self.processing)
             > 1 else "当前无人排队, 消息处理中")
        if check_length:
            tmp_msg += f"\n!非文本消息!只取最前面文本为处理内容, 忽略后面特殊类型信息!"
        if launcher_type == "person":
            tmp_id = cqhttp.sendPersonMessage(
                sender_id,  tmp_msg,
                group_id=launcher_id if launcher_id != sender_id else None).message_id
        else:
            tmp_id = cqhttp.sendGroupMessage(launcher_id, [
                At(qq=sender_id), Plain(text=tmp_msg)
            ]).message_id
        start_time = time.time()

        # 处理消息
        reply = self.emit(Events.GetOpenAi__).request_completion(
            session_name, text_message)
        end_time = time.time()
        if end_time - start_time < 0.5:
            time.sleep(0.5 - (end_time - start_time))
        if launcher_type == "person":
            cqhttp.sendPersonMessage(
                sender_id, reply,
                group_id=launcher_id if launcher_id != sender_id else None)
        else:
            cqhttp.sendGroupMessage(launcher_id, [
                At(qq=sender_id), Plain(text=reply)
            ])
        self.processing.remove(session_name)
        cqhttp.recall(tmp_id)
