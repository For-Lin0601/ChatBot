import logging
########## 主线程必选项 ##########



########## plugin.name='Log' plugin.path='//plugins//__log//main' ##########

# 日志级别
logging_level = logging.INFO


########## plugin.name='ThreadCtlPlugin' plugin.path='//plugins//__threadctl//main' ##########
# 线程池相关配置，该参数决定机器人可以同时处理几个人的消息，超出线程池数量的请求会被阻塞，不会被丢弃，如果你不清楚该参数的意义，请不要更改
sys_pool_num = 8
# 执行管理员请求和指令的线程池并行线程数量，一般和管理员数量相等
admin_pool_num = 2
# 执行用户请求和指令的线程池并行线程数量，如需要更高的并发，可以增大该值
user_pool_num = 6



########## plugin.name='GPTBot' plugin.path='//plugins//GPT//main' ##########



########## plugin.name='TimeReminderPlugin' plugin.path='//plugins//timeReminder//main' ##########
setsth = 123
# timeReminder


########## plugin.name='ChatModel' plugin.path='//plugins//ChatWithGPT//main' ##########
# haha


########## plugin.name='banWordsUtil' plugin.path='//plugins//banWords//main' ##########
# 是否启用百度云内容安全审核，用于接入百度云，从而智能的拦截机器人发出的不合格图片和消息
# 注册方式查看 https://cloud.baidu.com/doc/ANTIPORN/s/Wkhu9d5iy，如果开启 baidu_check = True
baidu_check = False

# 百度云API_KEY 24位英文数字字符串
baidu_api_key = ""

# 百度云SECRET_KEY 32位的英文数字字符串
baidu_secret_key = ""

# 不合规消息自定义返回
inappropriate_message_tips = "[百度云]请珍惜机器人，当前返回内容不合规"

##### 屏蔽词请前往 plugins/banWords/sensitive.json 中修改!!!
