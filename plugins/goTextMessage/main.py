
from func_timeout import FunctionTimedOut, func_set_timeout
from Events import *
from Models.Plugins import *
from plugins.goTextMessage.Events import GetQQPersonCommand
from plugins.gocqOnQQ.entities.components import At, Node, Plain
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

    # @on(QQ_private_message)
    # def check_cmd(self, event: EventContext,  **kwargs):
    #     message: Union[PersonMessage, GroupMessage] = kwargs["QQevents"]
    #     self.CQHTTP: CQHTTP_Protocol = self.emit(GetCQHTTP__)

        # if message.message[0].text == "reload":
        #     logging.critical("开始插件热重载")
        #     self.emit(Events.SubmitSysTask__, fn=Plugin._reload)
        # elif message.message[0].text == "get":
        #     self.CQHTTP.sendFriendMessage(1636708665, "fuck")
        # else:
        #     tmp = self.emit(GetOpenAi__).request_completion(
        #         "fuck", message.message[0].text)
        #     self.CQHTTP.sendFriendMessage(1636708665, tmp)

    @on(QQ_private_message)
    def check_cmd_and_chat_with_gpt(self, event: EventContext,  **kwargs):
        self.config = self.emit(GetConfig__)
        message: PersonMessage = kwargs["QQevents"]
        self.cqhttp: CQHTTP_Protocol = self.emit(GetCQHTTP__)

        if message.sender == self.config.qq:
            return

        if message.message[0].type != "Plain":
            return

        event.prevent_postorder()
        msg: str = message.message[0].text

        if len(msg) == 0:
            return

        is_adimn = True if \
            message.user_id in self.emit(GetConfig__).admin_list else False

        def time_ctrl_wrapper():
            tmp_id = []
            for _ in range(self.config.retry_times + 1):
                try:
                    @func_set_timeout(self.config.process_message_timeout)
                    def _time_crtl():
                        self.process_message(
                            "person", message.user_id,
                            msg, message.message, message.user_id
                        )
                    _time_crtl()
                    break
                except FunctionTimedOut:
                    logging.warning(f"{message.user_id}: 超时，重试中({_})")
                    tmp_id.append(self.cqhttp.sendFriendMessage(
                        message.user_id, f"[bot]warinig: 超时，重试中({_})"
                    ).message_id)
            else:
                for id_ in tmp_id:
                    self.cqhttp.recall(id_)
        if is_adimn:
            self.emit(SubmitAdminTask__, fn=time_ctrl_wrapper)
        else:
            self.emit(SubmitUserTask__, fn=time_ctrl_wrapper)

    def is_banned(self, launcher_type: str, launcher_id: int):
        """检查发送方是否被禁用"""
        config = self.emit(GetConfig__)
        if launcher_type == "group":
            return launcher_id in config.banned_group_list
        return launcher_id in config.banned_person_list

    def process_message(
            self,
            launcher_type: str,
            launcher_id: int,
            text_message: str,
            message_chain: list,
            sender_id: int) -> None:
        """处理消息

        :param launcher_type: 发起对象类型
        :param launcher_id: 发起对象ID(可能为群号)
        :param text_message: 消息文本
        :param message_chain: 消息链
        :param sender_id: 发送者ID

        :return: None
        """
        session_name = "{}_{}".format(launcher_type, launcher_id)

        # 检查发送方是否被禁用
        if self.is_banned(launcher_type, launcher_id):
            logging.info(f"根据禁用列表忽略{session_name}的消息")
            return

        # 触发命令
        if text_message[0] in ["!", "！"]:
            self.emit(GetQQPersonCommand,
                      message=text_message,
                      message_chain=message_chain
                      )
            return

        # 限速策略
        if session_name in self.processing:
            self.cqhttp.sendFriendMessage(
                sender_id, self.config.message_drop_tip)
            return
        self.processing.add(session_name)
        cqhttp: CQHTTP_Protocol = self.emit(GetCQHTTP__)
        tmp_id = cqhttp.sendFriendMessage(
            sender_id, f"[bot]收到消息, 当前{len(self.processing)}人正在排队").message_id

        # 处理消息
        reply = self.emit(GetOpenAi__).request_completion(
            session_name, text_message)
        cqhttp.sendFriendMessage(sender_id, reply)
        self.processing.remove(session_name)
        cqhttp.recall(tmp_id)

        # logging.info(message.message)
        # if message.message[0].text == "reload":
        #     logging.critical("开始插件热重载")
        #     self.emit(Events.SubmitSysTask__, fn=Plugin._reload)
        # elif message.message[0].text == "get":
        # at = At(qq=1636708665)

        # self.CQHTTP.sendPersonForwardMessage(1636708665, [
        #     Node(name="啊", uin=2944142195, content=[
        #         Plain(text="八")
        #     ]),
        #     Node(name="啊", uin=2944142195, content=[
        #         Plain(text="嘎")
        #     ]),
        #     Node(name="啊", uin=2944142195, content=[
        #         Plain(text="呀")
        #     ]),
        #     Node(name="啊", uin=2944142195, content=[
        #         Plain(text="路")
        #     ])
        # ])

        # self.CQHTTP.sendGroupMessage(104960075, [at, Plain("fuck")])
        # self.CQHTTP.sendGroupForwardMessage(104960075, [

        #     Node(name="落雪ちゃん", uin=2941383730, content=[
        #         Plain(text="nc什么时候cos小老师")
        #     ]),
        #     Node(name="盐焗雾喵", uin=2190945952, content=[
        #         Plain(text="今晚就cos小老师")
        #     ]),
        #     Node(name="Rosemoe♪ ~ requiem ~", uin=2073412493, content=[
        #         Plain(text="好耶")
        #     ])
        # ])

        # else:
        #     # 超时则重试，重试超过次数则放弃
        #     failed = 0
        #     for i in range(self.retry):
        #         try:

        #             @func_set_timeout(config.process_message_timeout)
        #             def time_ctrl_wrapper():
        #                 reply = processor.process_message('person', event.sender.id, str(event.message_chain),
        #                                                   event.message_chain,
        #                                                   event.sender.id)
        #                 return reply

        #             reply = time_ctrl_wrapper()
        #             break
        #         except FunctionTimedOut:
        #             logging.warning(
        #                 "person_{}: 超时，重试中({})".format(event.sender.id, i))
        #             pkg.openai.session.get_session('person_{}'.format(
        #                 event.sender.id)).release_response_lock()
        #             if "person_{}".format(event.sender.id) in pkg.qqbot.process.processing:
        #                 pkg.qqbot.process.processing.remove(
        #                     'person_{}'.format(event.sender.id))
        #             failed += 1
        #             continue

        #     if failed == self.retry:
        #         pkg.openai.session.get_session('person_{}'.format(
        #             event.sender.id)).release_response_lock()
        #         self.notify_admin("{} 请求超时".format(
        #             "person_{}".format(event.sender.id)))
        #         reply = [tips_custom.reply_message]

        # # if reply:
        # #     return self.send(event, reply, check_quote=False)
