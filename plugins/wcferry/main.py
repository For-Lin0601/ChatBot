import time
from queue import Empty

import Events
from .Events import *
from Models.Plugins import *

from wcferry import Wcf, WxMsg


class RunningFlag:
    def __init__(self) -> None:
        self.flag = False


@register(
    description="微信机器人",
    version="1.0.0",
    author="For_Lin0601",
    priority=2,
    enabled=False  # TODO 有需要请打开, 此处不支持热重载
)
class WeChatbot(Plugin):

    def __init__(self):
        pass

    @on(GetWCF__)
    def get_cqhttp(self, event: EventContext, **kwargs):
        event.prevent_postorder()
        event.return_value = self.wcf

    def on_reload(self):
        self.running_flag.flag = False
        self.set_reload_config("running_flag", self.running_flag)
        self.set_reload_config("wcf", self.wcf)

    def on_stop(self):
        self.running_flag.flag = False

    @on(PluginsLoadingFinished)
    @on(PluginsReloadFinished)
    def get_config_and_set_flask(self, event: EventContext, **kwargs):
        self.config = self.emit(Events.GetConfig__)
        self.admins: list = self.config.wx_admin_list
        # 登入微信
        if self.is_first_init():
            self.running_flag = RunningFlag()
            self.emit(Events.SubmitSysTask__, fn=self._run)
        else:
            self.running_flag = self.get_reload_config("running_flag")
            self.wcf = self.get_reload_config("wcf")

        self.running_flag.flag = True

    def is_admin(self, wxid: str):
        """检查发送方是否为管理员"""
        if wxid in self.admins:
            return True
        for friend in self.wcf.get_contacts():
            if friend['code'] == wxid:
                if friend['code'] in self.admins:
                    return True
                return False
        return False

    def _run(self):
        """监听事件"""
        # wcferry 登入在QQ之后
        time.sleep(13)
        self.wcf = Wcf(debug=False)
        # wechatpy 文档建议预留五秒以加载微信数据
        time.sleep(5)
        self.wcf.enable_receiving_msg()
        i = 0
        while not self.wcf.is_receiving_msg() and i < 10:
            time.sleep(1)
            i += 1
        logging.critical(
            f'微信程序启动完成,如长时间未显示 "wcferry version: xx.xx.xx.xx" 请检查配置')
        self.emit(WXClientSuccess)
        while True:
            if not self.running_flag.flag:
                time.sleep(1)
                continue
            try:
                msg: WxMsg = self.wcf.get_msg()
                logging.info(f"收到微信消息: {msg}")
            except Empty:
                continue  # Empty message
            except Exception as e:
                logging.error(f"Receiving message error: {e}")
                continue

            # 忽略自身消息
            if msg.from_self():
                continue

            # 判断是否为管理员, 加入对应线程池
            if self.is_admin(msg.sender):
                self.emit(
                    Events.SubmitAdminTask__,
                    fn=self.emit,
                    kwargs={
                        'event_name': Wx_msg,
                        'Wx_msg': msg,
                        'is_admin': True
                    })
            else:
                self.emit(
                    Events.SubmitUserTask__,
                    fn=self.emit,
                    kwargs={
                        'event_name': Wx_msg,
                        'Wx_msg': msg,
                        'is_admin': False
                    })
