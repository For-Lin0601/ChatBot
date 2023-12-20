
# 此文件为调试文件, 上传的文件中并未使用此模块

# 请先安装viztracer, requirement.txt里没有, 因为太大了, 约100MB
# pip安装: pip install viztracer
# 用法: 导入这个包, start()开启录制, stop()保存。多等一会会跳出类似下面的语句：
# vizviewer "D:\path\to\result.json"
# 复制这句到命令行, 即可查看录制结果

# 静态类, 可在不同文件启动与保存
# 理论上自动打开游览器, 若未自动打开, 看命令行提示
# 看完记得关闭命令行, 不然9001端口会被占用

# 注意这个是调试包, 所以很容易导致程序崩溃退出, 基本没录过多少
# 如果实在需要, 可以用try-except包裹一下防止异常终止程序

# 只能录一次看一次。若要同时录制多次一起看, 请自行参考VizTracer的文档调整
# 并且不建议录制过多内容, 会变慢。以及热重载相关的(importlib包)不确定能否正常运行

from viztracer import VizTracer


class InstanceViztracer:
    viztracer: VizTracer = None

    @classmethod
    def start(cls):
        if cls.viztracer:
            cls.viztracer.clear()
            cls.viztracer = None
        cls.viztracer = VizTracer(tracer_entries=100000000)
        cls.viztracer.start()

    @classmethod
    def stop(cls):
        if cls.viztracer:
            cls.viztracer.stop()
            cls.viztracer.save()
