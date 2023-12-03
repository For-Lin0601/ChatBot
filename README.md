# ChatBot

a fucking ChatBot link QQ, weChat to GPT.

# 挂载项目

## 使用 `python 3.10` 环境

1. 拉取仓库
2. 直接运行`main.py`文件, 会弹出`config.py`文件
3. 根据注释提示完善`config.py`文件
4. 安装所有依赖(请注意先运行`main.py`, 此处有元编程运用)
   `pip install -r requirements.txt`
   若想启用虚拟环境在此处启用即可
   后期可能改自动安装, 目前在开发阶段, 还请手动安装
5. 重新启动`main.py`, 即可使用

### 目前还没啥用, 当前进度: 连接 QQ

本项目使用了[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)作为连接 QQ 的方式

# 插件编写规范

# 1. 主线程流程

启动主程序后

1. 加载 log 和 config
2. 加载所有[插件基类](#2-插件基类编写规范plugin)
3. while True: time.sleep(0xFF)不返回

   如果意外出错, 在这里做配置保存等

由于主线程的插件特性, 可直接删去`gocqOnQQ`文件夹而不报错, 但实际因为内部耦合度大, 并不建议这么做

实际上只有双下划线开头的不可删除, 其余`./plugins`下的文件并非必须项

[当前已有插件的优先级](#当前已有插件的优先级：)

# 2. 插件基类编写规范(`Plugin`)

插件目录结构应如下

- ChatBot
  - `plugins`
    - `__config`
      - `__init__.py`
      - `Events.py`
      - `main.py`
    - ... ...
    - `yourPluginName`
      - `__init__.py`
      - `config-template.py`
      - `Events.py`
      - `main.py`
      - `requirements.txt`
    - ... ...

1. `__init__.py`(空文件)和`main.py`不可省略, 其余可省略。

   但如果日后有计划使用此配置, 可提前用同名空文件占位

2. 项目采用了一些元编程元素, 在`__config.py`中按插件优先级读取`config-template.py`, `Events.py`, `requirements.txt`中的内容写入主线程的同名文件中。以`##### {plugin.name=} {plugin.path=} #####`作为分隔。

   程序启动时会更新上述文件, 但不更新`config.py`(用户填写, 并在程序启动时创建该文件)

3. 插件基类应当有`__init__`, `on_reload`, `on_stop`三个函数, 分别为初始化, 热重载和程序异常尝试保存

4. 每个插件基类同时最多应当只有主线程创建的唯一实例

5. 插件中的函数应被`@Plugin.on()`注册, 否则函数不会被`self.emit()`直接触发
   (`@Plugin.on()`可简写为`@on()`, `emit()`由于方便日志记录等原因, 出于可读性考虑不支持简写)

6. 尽量使用封装的`emit()`函数调用其他插件的函数

   当然在 Plugin 中拥有`plugin_list`保存了插件列表, 按优先级排序, 请自行确保安全调用

插件的`main.py`编写示例：

```python
from Models.Plugins import *
from plugins.__config.Events import *

@register(
    description="输出hello world",  # 插件描述
    version="1.0.0",                # 插件版本
    author="For_Lin0601",           # 作者
    priority=500,                   # 负数应预留给程序运行必须项, 请尽量不要出现重复的优先级, 否则函数触发顺序不易确定
)
class Config(Plugin):               # 注意类名会作为一些 不安全 函数的标识, 尽管在书写这些不安全函数时做了声明, 但还希望类名不重复

    def __init__(self):
        if self.is_first_init():                              # 判断程序是否为第一次启动
            self.config = None
        else:
            self.config = Plugin.get_reload_config("config")  # `get_reload_config()`不传参则返回热重载前设定的整个字典
            # 此函数背后字典将于热重载结束后清空, 推荐在热重载`on_reload`中通过`set_reload_config(key, value)`存入

    # 事件应写在`Events.py`中
    # GetConfig__ = "get_config__"
    # """获取配置

    #     kwargs:
    #         config_name: str 配置名称(为空则返回配置字典)

    #     returns:
    #         config: ModuleType 配置模块(以 value = config.key 读取)
    # """

    @on(GetConfig__)                                          # 双下划线结尾表示必阻塞事件, 即只应当有此事件开发者自己注册此事件, 供外部`self.emit(GetConfig__)`
    def get_config(self, event: EventContext,  **kwargs):     # 函数名实际上没关系, 但建议规范命名, 以及不和`Plugin`中的函数名冲突
        """获取配置列表"""
        event.prevent_postorder()
        event.return_value = self.config                      # 插件不显式`return`
        # 返回值请自行保存到`event.return_value`中, 主线程不做任何合法性判断

    # 若希望程序启动和重载完后都触发, 可以使用如下连续两个`@on()`装饰同一个函数
    @on(PluginsLoadingFinished)                               # 插件首次加载时触发(程序启动时)
    @on(PluginsReloadFinished)                                # 插件重载完成时触发
    def get_Config(self, event: EventContext,  **kwargs):
        from Event import GetConfig__
        # 此处除了主线程必须项必然出现, 其余项可能在程序第一次运行后才创建
        # 故此处强烈建议动态导入
        config = self.emit(GetConfig__)                       # `emit`返回值请看`Events.py`中的注解
        # `emit`后续参数只接受`**kwargs`, 且在响应插件内打包为`kawrgs`参数
        # 优点是响应插件内必解包`kwargs`, 可做类型声明

    def on_reload(self):
        self.set_reload_config("config", self.config)
        # 此处会将配置写入`Plugin.__reload_config__`字典, 此字典将在热重载完成后清空。
        # 故如果有配置不需要热重载, 可在此暂存
        # 同时在`__init__.py`中判断`self.is_first_init()`来决定设置配置或读取配置

    def on_stop(self):
        # 程序异常停止时调用, 比如数据库存储, 日志记录等
        # 无意外不调用
        pass
```

# 当前已有插件的优先级：

- -100: **\_\_config**
- -99: **\_\_log**
- -98: **\_\_threadctl**
