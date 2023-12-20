
import os


def check_permission(sender_id):
    """检查对象是否通过权限, 此处传入`qq号`或`微信wxid`皆可"""
    sender_id = str(sender_id)

    qq_default_password_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'default_password.txt')
    with open(qq_default_password_path, 'r') as file:
        account_list = file.readlines()
        account_list = [account.strip() for account in account_list]  # 删除末尾换行符
        if sender_id in account_list:
            return True

    wx_default_password_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'default_password_wx.txt')
    with open(wx_default_password_path, 'r') as file:
        account_list = file.readlines()
        account_list = [account.strip() for account in account_list]  # 删除末尾换行符
        if sender_id in account_list:
            return True

    return False
