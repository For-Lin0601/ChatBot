import threading
import time
from concurrent.futures import ThreadPoolExecutor

import Events
from .Events import *
from Models.Plugins import *


class Pool:
    """线程池结构"""
    pool_num: int = None
    ctl: ThreadPoolExecutor = None
    task_list: list = None
    task_list_lock: threading.Lock = None
    monitor_type = True

    def __init__(self, pool_num):
        self.pool_num = pool_num
        self.ctl = ThreadPoolExecutor(max_workers=self.pool_num)
        self.task_list = []
        self.task_list_lock = threading.Lock()

    def __thread_monitor__(self):
        while self.monitor_type:
            for t in self.task_list:
                if not t.done():
                    continue
                try:
                    self.task_list.pop(self.task_list.index(t))
                except:
                    continue
            time.sleep(1)


class ThreadCtl:
    def __init__(self, sys_pool_num, admin_pool_num, user_pool_num):
        """线程池控制类

        sys_pool_num: 分配系统使用的线程池数量(>=8)

        admin_pool_num: 用于处理管理员消息的线程池数量(>=1)

        user_pool_num: 分配用于处理用户消息的线程池的数量(>=1)
        """
        if sys_pool_num < 5:
            raise Exception(
                "Too few system threads(sys_pool_num needs >= 8, but received {})".format(sys_pool_num))
        if admin_pool_num < 1:
            raise Exception(
                "Too few admin threads(admin_pool_num needs >= 1, but received {})".format(admin_pool_num))
        if user_pool_num < 1:
            raise Exception(
                "Too few user threads(user_pool_num needs >= 1, but received {})".format(admin_pool_num))
        self.__sys_pool__ = Pool(sys_pool_num)
        self.__admin_pool__ = Pool(admin_pool_num)
        self.__user_pool__ = Pool(user_pool_num)
        self.submit_sys_task(self.__sys_pool__.__thread_monitor__)
        self.submit_sys_task(self.__admin_pool__.__thread_monitor__)
        self.submit_sys_task(self.__user_pool__.__thread_monitor__)

    def __submit__(self, pool: Pool, fn, /, *args, **kwargs):
        t = pool.ctl.submit(fn, *args, **kwargs)
        pool.task_list_lock.acquire()
        pool.task_list.append(t)
        pool.task_list_lock.release()
        return t

    def submit_sys_task(self, fn, /, *args, **kwargs):
        return self.__submit__(
            self.__sys_pool__,
            fn, *args, **kwargs
        )

    def submit_admin_task(self, fn, /, *args, **kwargs):
        return self.__submit__(
            self.__admin_pool__,
            fn, *args, **kwargs
        )

    def submit_user_task(self, fn, /, *args, **kwargs):
        return self.__submit__(
            self.__user_pool__,
            fn, *args, **kwargs
        )

    def shutdown(self):
        self.__user_pool__.ctl.shutdown(cancel_futures=True)
        self.__user_pool__.monitor_type = False
        self.__admin_pool__.ctl.shutdown(cancel_futures=True)
        self.__admin_pool__.monitor_type = False
        self.__sys_pool__.monitor_type = False
        self.__sys_pool__.ctl.shutdown(wait=True, cancel_futures=False)

    def reload(self, admin_pool_num, user_pool_num):
        self.__user_pool__.ctl.shutdown(cancel_futures=True)
        self.__user_pool__.monitor_type = False
        self.__admin_pool__.ctl.shutdown(cancel_futures=True)
        self.__admin_pool__.monitor_type = False
        self.__admin_pool__ = Pool(admin_pool_num)
        self.__user_pool__ = Pool(user_pool_num)
        self.submit_sys_task(self.__admin_pool__.__thread_monitor__)
        self.submit_sys_task(self.__user_pool__.__thread_monitor__)


@register(
    description="线程池控制",
    version="1.0.0",
    author="For_Lin0601",
    priority=-98
)
class ThreadCtlPlugin(Plugin):

    def __init__(self):
        pass

    @on(PluginsLoadingFinished)
    @on(PluginsReloadFinished)
    def get_config(self, event: EventContext, **kwargs):
        self.config = self.emit(Events.GetConfig__)
        if self.is_first_init():
            self.ctl = ThreadCtl(
                sys_pool_num=self.config.sys_pool_num,
                admin_pool_num=self.config.admin_pool_num,
                user_pool_num=self.config.user_pool_num
            )
        else:
            self.ctl = self.get_reload_config("ctl")

    @on(SubmitSysTask__)
    def submit_sys_task(self, event: EventContext, **kwargs):
        logging.debug(f"提交系统任务: {kwargs}")
        event.prevent_postorder()
        fn = kwargs["fn"]
        args = kwargs.get("args", ())
        kwargs = kwargs.get("kwargs", {})
        event.return_value = self.ctl.submit_sys_task(fn, *args, **kwargs)

    @on(SubmitAdminTask__)
    def submit_admin_task(self, event: EventContext, **kwargs):
        logging.debug(f"提交管理员任务: {kwargs}")
        event.prevent_postorder()
        fn = kwargs["fn"]
        args = kwargs.get("args", ())
        kwargs = kwargs.get("kwargs", {})
        event.return_value = self.ctl.submit_admin_task(fn, *args, **kwargs)

    @on(SubmitUserTask__)
    def submit_user_task(self, event: EventContext, **kwargs):
        logging.debug(f"提交用户任务: {kwargs}")
        event.prevent_postorder()
        fn = kwargs["fn"]
        args = kwargs.get("args", ())
        kwargs = kwargs.get("kwargs", {})
        event.return_value = self.ctl.submit_user_task(fn, *args, **kwargs)

    def on_reload(self):
        self.set_reload_config("ctl", self.ctl)
        self.ctl.reload(self.config.admin_pool_num, self.config.user_pool_num)

    def on_stop(self):
        self.ctl.shutdown()
