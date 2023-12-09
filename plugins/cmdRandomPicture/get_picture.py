import logging
import os
import random
import re
import requests
import xml.etree.ElementTree as ET
from io import BytesIO
from PIL import Image

from ..gocqOnQQ.QQmessage.components import Image as QQImage
from Models.headers import get_random_ua


# 基于QChatGPT实现的随机图片的机器人回复
class RandomImg:
    # api 接口队列
    api_item = {}
    # api 返回值处理队列
    api_ret_item = {}
    # 所有API名称
    all_api_name = []
    # 将随机在此处开始获取
    random_num = 0

    def __init__(self):
        # 载入配置文件……
        logging.debug('开始读取配置文件')
        config_file_path = os.path.join(os.path.dirname(__file__), 'conf.xml')

        tree = ET.parse(config_file_path)
        root = tree.getroot()

        self.api_item = {}
        self.all_api_name = []
        for api_elem in root.findall('.//api'):
            api_name = api_elem.get('api_name')
            self.all_api_name.append(api_name)

            api_data = {}
            for url_elem in api_elem.findall('./api_url/*'):
                api_data[url_elem.tag] = url_elem.text

            self.api_item[api_name] = api_data

        logging.debug('配置文件读取成功')
        self.random_num = random.randint(0, len(self.all_api_name) - 1)

    def _loop_random_image(self, random_num, type_img):
        """
        循环获取符合要求的API
        :program 指令队列
        :random_num 随机数值
        :type_img 图片类型(pc&pe&random)
        """
        random_number = random_num
        tmp = self.all_api_name[random_number]
        url = self.api_item[tmp]
        url = url[type_img]
        if url == "":
            for i in range(len(self.all_api_name)):
                try:
                    url = self.api_item[self.all_api_name[random_number]][type_img]
                except IndexError:
                    random_number += 1
                if url != "":
                    break
                if random_number > len(self.all_api_name):
                    random_number = 0
                else:
                    random_number += 1
        if url == "":  # 如果找不到就随机返回壁纸
            url = self.api_item[self.all_api_name[0]]["random"]['url']
        return url

    def get_random_image(self, program: list):
        """
        获取随机图片
        : program 指令队列
        : reply 返回base64编码图片
        : return Base64 Images and image message
        """
        logging.debug('开始获取图片')
        # 判断获取图片类型
        if len(program) == 0 or program[0] == '':
            program = ['随机']
            url = self._loop_random_image(self.random_num, 'random')
        elif re.search('pc|PC|电脑|横屏', program[0]):
            program[0] == '横屏'
            url = self._loop_random_image(self.random_num, 'pc')
        elif re.search('pe|PE|android|mobile|手机|安卓|竖屏', program[0]):
            program[0] == '竖屏'
            url = self._loop_random_image(self.random_num, 'pe')
        elif re.search('random|随机', program[0]):
            url = self._loop_random_image(self.random_num, 'random')
        else:
            reply = YingDaoGetRandomImage().yingdao_name_change_dict.values()
            reply = list(set(reply))
            reply = '、'.join(reply)
            return f'[bot]err: 参数不正确!\n !照片|图片|壁纸|ranimg|闪照 <番名> [pc|PC|电脑|横屏|pe|PE|android|mobile|手机|安卓|竖屏|random|随机|……]\n番名可选:\n[{reply}]', program

        while True:
            try:
                # 获取随机值来随机选择API
                resp = requests.get(url=url,
                                    headers=get_random_ua())
                image_path = os.path.join(
                    os.path.dirname(__file__), 'temp.jpg')
                with open(image_path, 'wb') as file:
                    file.write(resp.content)

                # 使用QQImage.fromFileSystem()加载图片
                reply = QQImage.fromFileSystem(path=image_path)
                break
            except requests.exceptions.SSLError:
                pass
            except Exception as e:
                return f'[bot]err: 网络错误!\n[{e}]', ''

        return reply, program


class YingDaoGetRandomImage:

    def __init__(self):
        self.yingdao_name_change_dict = {
            '赛马娘': '赛马娘',
            '东京食尸鬼': '东京食尸鬼',
            'Fate': 'Fate',
            'fate': 'Fate',
            '为美好世界献上祝福': '为美好世界献上祝福',
            '献上祝福': '为美好世界献上祝福',
            '某科学的超电磁炮': '某科学的超电磁炮',
            '超电磁炮': '某科学的超电磁炮',
            '原神': '原神',
            '元神': '原神',
            '神奇宝贝': '神奇宝贝',
            '龙珠': '龙珠',
            '罪恶王冠': '罪恶王冠',
            '鬼灭之刃': '鬼灭之刃',
            '鬼灭': '鬼灭之刃',
            '火影忍者': '火影忍者',
            '火影': '火影忍者',
            '海贼王': '海贼王',
            '进击的巨人': '进击的巨人',
            '巨人': '进击的巨人',
            '从零开始的异世界生活': '从零开始的异世界生活',
            '异世界生活': '从零开始的异世界生活',
            '从零开始': '从零开始的异世界生活',
            '刀剑神域': '刀剑神域',
            '钢之炼金术师': '钢之炼金术师',
            '炼金术师': '钢之炼金术师',
            '妖精的尾巴': '妖精的尾巴',
            '缘之空': '缘之空',
            '动漫综合': '动漫综合',
            '动漫': '动漫综合',
            '漫画': '动漫综合',
            '我的世界系列': '我的世界系列',
            '我的世界': '我的世界系列',
            'minecraft': '我的世界系列',
            'mc': '我的世界系列',
            '东方project': '东方project',
            '东方': '东方project',
            '猫娘': '猫娘',
            '风景系列': '风景系列',
            '风景': '风景系列',
            '物语系列': '物语系列',
            '物语': '物语系列',
            '少女前线': '少女前线',
            '前线': '少女前线',
            '明日方舟': '明日方舟',
            '方舟': '明日方舟',
            '重装战姬': '重装战姬',
            'P站系列': 'P站系列',
            'P站': 'P站系列',
            'p站': 'P站系列',
            'CG系列': 'CG系列',
            'CG': 'CG系列',
            'cg': 'CG系列',
            '守望先锋': '守望先锋',
            '守望': '守望先锋',
            '王者荣耀': '王者荣耀',
            '王者': '王者荣耀',
        }

        self.yingdao_has_screens = {
            # [0, 0]表示无后缀
            # [1, 1]表示只有后缀1有效
            # [1, 10]表示后缀1~10都有效
            # 若没出现, 则表示有(横屏、竖屏、随机)
            '动漫综合': [1, 18],
            '我的世界系列': [1, 1],
            '东方project': [1, 1],
            '猫娘': [1, 1],
            '风景系列': [1, 10],
            '物语系列': [1, 2],
            '少女前线': [1, 1],
            '明日方舟': [1, 2],
            '重装战姬': [1, 1],
            'P站系列': [1, 4],
            'CG系列': [1, 5],
            '守望先锋': [0, 0],
            '王者荣耀': [0, 0],
        }

    def check_pc_or_pe(self, program: list):
        """判断是否有番剧名出现"""
        if len(program) > 0 and program[0] in self.yingdao_name_change_dict:
            program[0] = self.yingdao_name_change_dict[program[0]]
            return True
        elif len(program) > 0 and program[0][:-2] in self.yingdao_name_change_dict:
            if len(program) < 2:
                program.append(program[0][:-2])
            else:
                program[1] = program[0][:-2]
            program[0] = self.yingdao_name_change_dict[program[0][:-2]]
            return True

        return False

    def _convert_base64_to_image(self, image):
        """把图片保存到本地, 这样转成jpg格式。返回本地路径"""
        file_path = os.path.join(os.path.dirname(__file__), "temp.jpg")
        image = Image.open(BytesIO(image))
        image.save(file_path)
        return file_path

    def yingdao_get_random_image(self, program: list):
        """获取指定番剧图片"""
        logging.debug('开始获取图片')
        if program[0] in self.yingdao_has_screens:
            if len(program) > 1:
                program[1] = '[warning]: 当前游戏不支持选择横竖屏~'

            ran = self.yingdao_has_screens[program[0]]
            if ran[0] == 0:
                yingdao_url = f'https://api.r10086.com/樱道随机图片api接口.php?图片系列={program[0]}'
            else:
                ran = random.randint(ran[0], ran[1])
                yingdao_url = f'https://api.r10086.com/樱道随机图片api接口.php?图片系列={program[0]}{ran}'
        else:
            if len(program) > 1:
                if re.search('pc|PC|电脑|横屏', program[1]):
                    program[1] = '横屏'
                    yingdao_url = f'https://api.r10086.com/樱道随机图片api接口.php?图片系列={program[0]}横屏系列1'
                elif re.search('pe|PE|android|mobile|手机|安卓|竖屏', program[1]):
                    program[1] = '竖屏'
                    yingdao_url = f'https://api.r10086.com/樱道随机图片api接口.php?图片系列={program[0]}竖屏系列1'
                elif re.search('random|随机', program[1]):
                    program[1] = '随机'
                    yingdao_url = f'https://api.r10086.com/樱道随机图片api接口.php?自适应图片系列={program[0]}'
                else:
                    reply = self.yingdao_name_change_dict.values()
                    reply = list(set(reply))
                    reply = '、'.join(reply)
                    return f'[bot]err: 参数不正确!\n !照片|图片|壁纸|ranimg|闪照 <番名> [pc|PC|电脑|横屏|pe|PE|android|mobile|手机|安卓|竖屏|random|随机|……]\n番名可选:\n[{reply}]', program
            else:
                program.append('随机')
                yingdao_url = f'https://api.r10086.com/樱道随机图片api接口.php?自适应图片系列={program[0]}'

        while True:
            try:
                # 获取随机值来随机选择API
                resp = requests.get(url=yingdao_url,
                                    headers=get_random_ua())
                tmp = self._convert_base64_to_image(resp.content)
                reply = QQImage.fromFileSystem(path=tmp)
                break
            except requests.exceptions.SSLError:
                pass
            except Exception as e:
                return f'[bot]err: 网络错误!\n[{e}]', ''

        return reply, program


def process_mod(program):
    """选择图片"""
    yingdao = YingDaoGetRandomImage()
    if yingdao.check_pc_or_pe(program):
        reply, program = yingdao.yingdao_get_random_image(program)
    else:
        reply, program = RandomImg().get_random_image(program)

    return reply, program
