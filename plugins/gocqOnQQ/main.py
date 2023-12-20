import asyncio
import json
import re
import time
from flask import Flask, jsonify
import websockets

import Events
from .Events import *
from Models.Plugins import *
from .QQevents import create_event
from .CQHTTP_Protocol.CQHTTP_Protocol import CQHTTP_Protocol


class RunningFlag:
    def __init__(self) -> None:
        self.flag = False


@register(
    description="QQ机器人",
    version="1.0.0",
    author="For_Lin0601",
    priority=1,
    # enabled=False  # TODO 取消注释这行即可关闭qq链接, 但强烈建议qq保持常开
)
class QQbot(Plugin):

    def __init__(self):
        pass

    @on(GetCQHTTP__)
    def get_cqhttp(self, event: EventContext, **kwargs):
        event.prevent_postorder()
        event.return_value = self.cqhttp_protocol

    def on_reload(self):
        self.running_flag.flag = False
        self.set_reload_config("running_flag", self.running_flag)
        self.set_reload_config("ws_url", self.ws_url)
        self.set_reload_config("http_url", self.http_url)

    def on_stop(self):
        self.running_flag.flag = False

    @on(PluginsLoadingFinished)
    @on(PluginsReloadFinished)
    def get_config_and_set_flask(self, event: EventContext, **kwargs):
        self.config = self.emit(Events.GetConfig__)
        self.admins: list = self.config.admin_list

        if self.is_first_init():
            self.running_flag = RunningFlag()
            # 修改配置文件
            self.ws_url = f'ws://{self.config.ws_address}/'
            self.http_url = f'http://{self.config.http_address}'

            config_file_path = os.path.join((os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))), "config.yml"
            )
            self._update_config(config_file_path, self.config.qq, self.config.host, self.config.port, self.config.api_key,
                                self.config.authorization, self.config.ws_address, self.config.http_address)

            # 启动签名服务器
            app = Flask(__name__)

            @app.route('/sign', methods=['POST'])
            def sign():
                return jsonify({
                    'api_key': self.config.api_key,
                    'authorization': self.config.authorization
                })

            # 启用新线程运行签名服务器
            self.emit(Events.SubmitSysTask__, fn=app.run,
                      kwargs={'host': self.config.host, 'port': self.config.port})

            def run_gocq_exe():
                executable_path = os.path.join(
                    "go-cqhttp", "go-cqhttp_windows_amd64.exe")
                os.system(f'"{executable_path}" -faststart')

            # 启用新线程运行go-cqhttp
            self.emit(Events.SubmitSysTask__, fn=run_gocq_exe)
            # 调试的时候可以注释掉这行, 运行主线程后在新命令行开启go-cqhttp
            # 这样重启或热重载机器人不影响go-cqhttp运行, 大大减少机器人被风控的概率

            self.emit(Events.SubmitSysTask__, fn=self._run)
        else:
            self.running_flag = self.get_reload_config("running_flag")
            self.ws_url = self.get_reload_config("ws_url")
            self.http_url = self.get_reload_config("http_url")
        self.cqhttp_protocol = CQHTTP_Protocol(self.http_url)
        self.running_flag.flag = True

    def _update_config(self, config_file_path,  qq, host, port, api_key, authorization, ws_address, http_address):
        """更改./go-cqhttp/config.yml"""
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config_content = file.read()
        pattern = re.compile(r'uin:\s+(\d+)')
        config_content = pattern.sub(f'uin: {qq}', config_content)

        new_sign_servers = f"""  sign-servers: 
    - url: 'http://{host}:{port}'  # 主签名服务器地址,  必填
      key: '{api_key}'  # 签名服务器所需要的apikey, 如果签名服务器的版本在1.1.0及以下则此项无效
      authorization: '{authorization}'   # authorization 内容, 依服务端设置, 如 'Bearer xxxx'
    - url: '-'  # 备用
      key: '114514'  
      authorization: '-'"""
        pattern = re.compile(r'[^#] sign-servers:(.*?)(?=(\n\n))', re.DOTALL)
        config_content = pattern.sub(new_sign_servers, config_content)

        new_address = f"""
servers:
  # 添加方式, 同一连接方式可添加多个, 具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器
  - http: # HTTP 通信设置
      address: {http_address} # HTTP监听地址
      version: 11     # OneBot协议版本, 支持 11/12
      timeout: 5      # 反向 HTTP 超时时间, 单位秒, <5 时将被忽略
      long-polling:   # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小, 0 表示不限制队列大小, 谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post:           # 反向HTTP POST地址列表
      #- url: ''                # 地址
      #  secret: ''             # 密钥
      #  max-retries: 3         # 最大重试, 0 时禁用
      #  retries-interval: 1500 # 重试时间, 单位毫秒, 0 时立即
      #- url: http://127.0.0.1:5701/ # 地址
      #  secret: ''                  # 密钥
      #  max-retries: 10             # 最大重试, 0 时禁用
      #  retries-interval: 1000      # 重试时间, 单位毫秒, 0 时立即
  # 正向WS设置
  - ws:
      # 正向WS服务器监听地址
      address: {ws_address}
      middlewares:
        <<: *default # 引用默认中间件"""
        pattern = re.compile(r'\nservers:(.*?)(?=(\n\n))', re.DOTALL)
        config_content = pattern.sub(new_address, config_content)

        with open(config_file_path, 'w', encoding='utf-8') as file:
            file.write(config_content)

    def _run(self):
        """监听事件"""
        # time.sleep至少10秒, 推荐12秒
        time.sleep(12)
        logging.info(
            f"QQ: {self.config.qq}, MAH: {self.config.host}:{self.config.port}")
        logging.critical(
            f'程序启动完成,如长时间未显示 "CQ WebSocket 服务器已启动: {self.config.ws_address},  CQ HTTP 服务器已启动: {self.config.http_address}" 请检查配置')

        async def listen():
            self.emit(QQClientSuccess)
            async with websockets.connect(self.ws_url) as websocket_event:

                while True:
                    message = await websocket_event.recv()
                    parsed_message = json.loads(message)

                    if self.running_flag.flag == False:
                        continue

                    try:
                        event_name, QQevents = create_event(
                            parsed_message)
                    except Exception as e:
                        logging.error(e)
                        continue
                    # 判断是否为管理员, 加入对应线程池
                    if event_name in ["QQ_private_message", "QQ_group_message"] \
                            and QQevents.user_id in self.admins:
                        self.emit(
                            Events.SubmitAdminTask__,
                            fn=self.emit,
                            kwargs={
                                'event_name': event_name,
                                'QQevents': QQevents
                            })
                    elif event_name not in ["QQ_heartbeat", "QQ_lifecycle"]:
                        # 这俩太吵了
                        self.emit(
                            Events.SubmitUserTask__,
                            fn=self.emit,
                            kwargs={
                                'event_name': event_name,
                                'QQevents': QQevents
                            })

        self.emit(Events.SubmitSysTask__, fn=asyncio.run(listen()))
