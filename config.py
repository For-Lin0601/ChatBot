import logging

########## 主线程必选项 ##########


########## plugin.name='Log' plugin.path='D://workspace ai//chatbot//plugins//log' ##########

# 日志级别
logging_level = logging.DEBUG


########## plugin.name='GPTBot' plugin.path='D://workspace ai//chatbot//plugins//gpt' ##########


########## plugin.name='TimeReminderPlugin' plugin.path='D://workspace ai//chatbot//plugins//timereminder' ##########
setsth = 123
# timeReminder


########## plugin.name='ChatModel' plugin.path='D://workspace ai//chatbot//plugins//chatwithgpt' ##########
# haha


########## plugin.name='banWordsUtil' plugin.path='D://workspace ai//chatbot//plugins//banwords' ##########
# 是否启用百度云内容安全审核，用于接入百度云，从而智能的拦截机器人发出的不合格图片和消息
# 注册方式查看 https://cloud.baidu.com/doc/ANTIPORN/s/Wkhu9d5iy，如果开启 baidu_check = True
baidu_check = False

# 百度云API_KEY 24位英文数字字符串
baidu_api_key = ""

# 百度云SECRET_KEY 32位的英文数字字符串
baidu_secret_key = ""

# 不合规消息自定义返回
inappropriate_message_tips = "[百度云]请珍惜机器人，当前返回内容不合规"

# 屏蔽词请前往 plugins/banWords/sensitive.json 中修改!!!
