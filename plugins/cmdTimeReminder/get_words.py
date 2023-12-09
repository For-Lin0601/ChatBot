import os
import msvcrt
import calendar
import re
from datetime import datetime, timedelta
import time

def get_words(text: str) -> list:
    """自然语言处理成为 [日期, 时间, [步频], 重复] 形式"""

    synonyms = {
        "年": ["(\d+)年", "(\d+)year"],
        "月": ["(\d+)月", "(\d+)mon"],
        "日": ["(\d+)日", "(\d+)天", "(\d+)号", "(\d+)day"],
        "时": ["(\d+)时", "(\d+)h"],
        "分": ["(\d+)分", "(\d+)min"],
        "秒": ["(\d+)秒", "(\d+)s"],
        "重复次数": ["(\d+)次", "(\d+)回", "(\d+)遍"],
        "重复频率": ["每", "每:", "隔", "隔:", "过", "过:", "频率", "频率:", "步频", "步频:", "步长", "步长:"],
    }

    replace_dict = {
        '钟': '', '点': '时', '小时': '时', '个时': '时', '个月': '月',
        '明早': '明天早', '明晚': '明天晚', '早': '早上', '晚': '晚上', '每早': '每1天早', '每晚': '每1天晚',
        '周': '星期', '礼拜': '星期', '星期日': '星期7 ', '星期天': '星期7 ',
        '以后': '后', '片刻': '15分后', '一会': '15分后', '过会': '15分后', '晚些': '15分后',
        '隔天': '隔1天', '隔月': '隔1月', '隔年': '隔1年',
        '每秒': '每1秒', '每分': '每1分', '每时': '每1时', '每天': '每1天', '每月': '每1月', '每年': '每1年',
        '半分': '30秒', '半时': '30分', '半天': '12时', '半月': '15天', '半年': '6月',
        '时半': '时30分', '1刻': '15分',
        '星期末': '星期7 ', '下分': '1分后',
    }

    def add_datetime(converted_datetime, years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
        """日期进位算法"""
        try:
            datetime_obj = datetime.fromtimestamp(converted_datetime.timestamp())
        except:
            datetime_obj = datetime.fromtimestamp(time.mktime(converted_datetime))
        month_overflow = (datetime_obj.month - 1 + months) // 12
        new_year = datetime_obj.year + years + month_overflow
        new_month = ((datetime_obj.month - 1 + months) % 12) + 1
        max_day = calendar.monthrange(new_year, new_month)[1]
        new_day = min(datetime_obj.day, max_day) + days

        while new_day > max_day:
            new_day -= max_day
            new_month += 1
            if new_month > 12:
                new_month = 1
                new_year += 1
            max_day = calendar.monthrange(new_year, new_month)[1]

        new_datetime = datetime(new_year, new_month, new_day, datetime_obj.hour, datetime_obj.minute, datetime_obj.second)
        new_datetime += timedelta(hours=hours, minutes=minutes, seconds=seconds)

        return new_datetime.timetuple()

    def cn_number(string: str) -> str:
        """把字符串中的中文数字转化成阿拉伯数字"""

        CN_NUM = {
            '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
            '貮': 2, '两': 2, '俩': 2,
        }
        CN_UNIT = {
            '十': 10, '拾': 10, '百': 100, '佰': 100, '千': 1000, '仟': 1000,
            '万': 10000, '萬': 10000, '亿': 100000000, '億': 100000000,
        }

        def cn1dig(cn):
            """处理只包含中文数字的字符串"""
            result = ''
            for char in cn:
                result += str(CN_NUM[char])
            return result

        def cn2dig(cn):
            """处理包含中文数字与数字单位的字符串"""

            lcn = list(cn)
            unit = 0 #当前的单位
            ldig = []#临时数组
            while lcn:
                cndig = lcn.pop()

                if cndig in CN_UNIT:
                    unit = CN_UNIT.get(cndig)
                    if unit == 10000:
                        ldig.append('w')    #标示万位
                        unit = 1
                    elif unit == 100000000:
                        ldig.append('y')    #标示亿位
                        unit = 1
                    continue

                else:
                    dig = CN_NUM.get(cndig)
                    if unit:
                        dig = dig * unit
                        unit = 0
                    ldig.append(dig)

            #处理10-19的数字
            if unit == 10:
                ldig.append(10)

            ret = 0
            tmp = 0
            while ldig:
                x = ldig.pop()
                if x == 'w':
                    tmp *= 10000
                    ret += tmp
                    tmp = 0
                elif x == 'y':
                    tmp *= 100000000
                    ret += tmp
                    tmp = 0
                else:
                    tmp += x

            ret += tmp
            return str(ret)

        pattern = r'[{}]+'.format(''.join(CN_NUM.keys()) + ''.join(CN_UNIT.keys()))
        matches = re.findall(pattern, string)
        for match in matches:
            if any(unit in match for unit in CN_UNIT):
                converted = cn2dig(match)
            else:
                converted = cn1dig(match)
            string = string.replace(match, converted, 1)

        return string

    def extract_count(text):
        """重复次数"""

        frequency = '无'
        for synonym_list in synonyms["重复次数"]:
            pattern = r"{}".format(synonym_list)
            match = re.search(pattern, text)
            if match:
                frequency_text = match.group(0)
                frequency = re.findall(r'\d+', frequency_text)[-1]
                text = text.replace(frequency_text, ' ')
                break

        return frequency, text

    def extract_frequency(text):
        """重复频率"""

        frequency = None
        time_unit = None
        year_month_day_time = ['年', '月', '日', '时', '分', '秒']
        for synonym in synonyms["重复频率"]:
            for index, time_unit in enumerate(year_month_day_time):
                pattern = r"{}(?:{})".format(synonym, "|".join(synonyms[time_unit]))
                match = re.search(pattern, text)
                if match:
                    frequency_text = match.group(0)
                    frequency = int(re.findall(r"\d+", frequency_text)[-1])
                    text = text.replace(match.group(), ' ')
                    break
            if frequency:
                break

        reply = ['0', '0', '0', '0', '0', '0']
        if frequency and time_unit:
            reply[index] = str(frequency)

        return reply, text

    def extract_date(text):
        """年、月、日"""

        today = add_datetime(datetime.today())
        pattern = r"(\d+)/(\d+)/(\d+)"
        match = re.search(pattern, text)
        if match:
            text = text.replace(match.group(), ' ')
            if len(match.group(1)) == 2:
                year = f"{str(today.tm_year)[:2]}{match.group(1)}"
            else:
                year = match.group(1)
            return year, match.group(2), match.group(3), text

        target_date = today
        year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(target_date.tm_mday)

        if any(keyword in text for keyword in ["后年", "下下一年", "下下年"]):
            month, day = '01', '01'
            target_date = add_datetime(target_date, years=+2)
            year = str(target_date.tm_year)
            text = re.sub(r"(后年|下下一年|下下年)", ' ', text)
        elif any(keyword in text for keyword in ["明年", "后一年", "下一年", "下年"]):
            month, day = '01', '01'
            target_date = add_datetime(target_date, years=+1)
            year = str(target_date.tm_year)
            text = re.sub(r"(明年|后一年|下一年|下年)", ' ', text)

        if "下下月" in text:
            day = '01'
            target_date = add_datetime(target_date, months=+2)
            year, month = str(target_date.tm_year), str(target_date.tm_mon)
            text = text.replace("下下月", ' ')
        elif "下月" in text:
            day = '01'
            target_date = add_datetime(target_date, months=+1)
            year, month = str(target_date.tm_year), str(target_date.tm_mon)
            text = text.replace("下月", ' ')

        weekday_num = int(datetime.today().strftime('%w'))
        if "下下星期" in text:
            match = re.search(r'下下星期(\d+)', text)
            if match:
                number = int(match.group(1))
                target_date = add_datetime(target_date, days=+(14-weekday_num+number))
            else:
                target_date = add_datetime(target_date, days=+14)
            year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(target_date.tm_mday)
            text = text.replace("下下星期", ' ')
        elif "下星期" in text:
            match = re.search(r'下星期(\d+)', text)
            if match:
                number = int(match.group(1))
                target_date = add_datetime(target_date, days=+(7-weekday_num+number))
            else:
                target_date = add_datetime(target_date, days=+7)
            year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(target_date.tm_mday)
            text = text.replace("下星期", ' ')
        elif "星期" in text:
            match = re.search(r'星期(\d+)', text)
            if match:
                number = int(match.group(1))
                target_date = add_datetime(target_date, days=+(number-weekday_num))
            else:
                target_date = add_datetime(target_date, days=+7)
            year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(target_date.tm_mday)
            text = text.replace("星期", ' ')

        if "大大后天" in text:
            target_date = add_datetime(target_date, days=+4)
            year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(target_date.tm_mday)
            text = text.replace("大大后天", ' ')
        elif "大后天" in text:
            target_date = add_datetime(target_date, days=+3)
            year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(target_date.tm_mday)
            text = text.replace("大后天", ' ')
        elif "后天" in text or "后儿" in text:
            target_date = add_datetime(target_date, days=+2)
            year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(target_date.tm_mday)
            text = text.replace("后天", ' ').replace("后儿", ' ')
        elif "明天" in text or "明儿" in text:
            target_date = add_datetime(target_date, days=+1)
            year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(target_date.tm_mday)
            text = text.replace("明天", ' ').replace("明儿", ' ')

        pattern = r"(?:{})+(?:之)?后".format("|".join(synonyms["日"] + synonyms["月"] + synonyms["年"]))
        match = re.search(pattern, text)
        if match:
            for i in range(len(match.groups()) + 1):
                try:
                    number = int(match.group(i))
                    break
                except:
                    pass
            unit = match.group(0)
            text = text.replace(unit, ' ')
            day = target_date.tm_mday
            if '年' in unit:
                target_date = add_datetime(target_date, years=+number)
            elif '月' in unit:
                target_date = add_datetime(target_date, months=+number)
            else:
                target_date = add_datetime(target_date, days=+number)
                day = target_date.tm_mday
            year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(day)

        pattern = r"{}".format("|".join(synonyms["年"]))
        match = re.search(pattern, text)
        if match:
            for i in range(len(match.groups()) + 1):
                try:
                    year = int(match.group(i))
                    break
                except:
                    pass
            year = str(year)
            text = text.replace(match.group(), ' ')
            month, day = '01', '01'

        pattern = r"{}".format("|".join(synonyms["月"]))
        match = re.search(pattern, text)
        if match:
            for i in range(len(match.groups()) + 1):
                try:
                    month = int(match.group(i))
                    break
                except:
                    pass
            month = str(month)
            text = text.replace(match.group(), ' ')
            day = '01'

        pattern = r"{}".format("|".join(synonyms["日"]))
        match = re.search(pattern, text)
        if match:
            for i in range(len(match.groups()) + 1):
                try:
                    day = int(match.group(i))
                    break
                except:
                    pass
            day = str(day)
            text = text.replace(match.group(), ' ')

        return year, month, day, text

    def extract_time(text):
        """时、分、秒"""

        pattern = r"(\d+):(\d+):(\d+)"
        match = re.search(pattern, text)
        if match:
            text = text.replace(match.group(), ' ')
            return match.group(1), match.group(2), match.group(3), text, '', '', ''

        target_date = add_datetime(datetime.now())
        year, month, day = '', '', ''
        hour, minute, second = '00', '00', '00'
        pattern = r"(?:{})+(?:之)?后".format("|".join(synonyms["时"] + synonyms["分"] + synonyms["秒"]))
        match = re.search(pattern, text)
        if match:
            for i in range(len(match.groups()) + 1):
                try:
                    number = int(match.group(i))
                    break
                except:
                    pass
            unit = match.group(0)
            text = text.replace(unit, '')
            if '时' in unit:
                target_date = add_datetime(target_date, hours=+number)
            elif '分' in unit:
                target_date = add_datetime(target_date, minutes=+number)
            else:
                target_date = add_datetime(target_date, seconds=+number)
            year, month, day = str(target_date.tm_year), str(target_date.tm_mon), str(target_date.tm_mday)
            hour, minute, second = str(target_date.tm_hour), str(target_date.tm_min), str(target_date.tm_sec)

        pattern = r"{}".format("|".join(synonyms["时"]))
        match = re.search(pattern, text)
        if match:
            for i in range(len(match.groups()) + 1):
                try:
                    hour = int(match.group(i))
                    break
                except:
                    pass
            hour = str(hour)
            text = text.replace(match.group(), ' ')
            minute, second = '00', '00'

        pattern = r"{}".format("|".join(synonyms["分"]))
        match = re.search(pattern, text)
        if match:
            for i in range(len(match.groups()) + 1):
                try:
                    minute = int(match.group(i))
                    break
                except:
                    pass
            minute = str(minute)
            text = text.replace(match.group(), ' ')
            second = '00'

        pattern = r"{}".format("|".join(synonyms["秒"]))
        match = re.search(pattern, text)
        if match:
            for i in range(len(match.groups()) + 1):
                try:
                    second = int(match.group(i))
                    break
                except:
                    pass
            second = str(second)
            text = text.replace(match.group(), ' ')

        if ('下午' in text or '晚' in text) and int(hour) < 12:
            hour = str(int(hour) + 12)
            text = text.replace("下午", ' ').replace("晚", ' ')

        return hour, minute, second, text, year, month, day



    # 中文数字转阿拉伯数字
    text = cn_number(text)
    text = text + ' '

    start_month = True if '月初' in text else False
    middle_month = True if '月中' in text else False
    end_month = True if '月末' in text or '月底' in text else False

    # 简单处理
    for old_value, new_value in replace_dict.items():
        text = text.replace(old_value, new_value)

    index = text.find("星期")
    if index != -1:
        try:
            if 1 <= int(text[index + 2]) <= 7:
                text = text[:index + 3] + ' ' + text[index + 3:]
            else:
                text = text[:index] + text[index + 3:]
        except:
            text = text[:index] + text[index + 2:]

    match = re.search(r"(上)(\d+)", text)
    if match:
        index = match.end()
        if not text[index:].startswith(('时', 'h')):
            text = text[:index] + '时' + text[index:]

    match = re.search(r"(\d+)(时)(\d+)", text)
    if match:
        index = match.end()
        if not text[index:].startswith(('分', 'min')):
            text = text[:index] + '分' + text[index:]

    match = re.search(r"(\d+)分(\d+)", text)
    if match:
        index = match.end()
        if not text[index:].startswith(('秒', 's')):
            text = text[:index] + '秒' + text[index:]

    match = re.search(r"(\d+)月(\d+)", text)
    if match:
        index = match.end()
        if not text[index:].startswith(('日', '号', '天', 'day')):
            text = text[:index] + '日' + text[index:]

    match = re.search(r"(?<!\d)月", text)
    match1 = re.search(r"下月", text)
    if match and not match1:
        text = re.sub(r"(?<!\d)月", "{}月".format(datetime.now().month), text)

    # 开始处理
    count_dict, text = extract_count(text)

    frequency_dict, text = extract_frequency(text)
    if count_dict == '无':
        count_dict = '-1' if sum(1 for _ in frequency_dict if _ != '0') else '1'

    year, month, day, text = extract_date(text)
    if start_month:
        day = '01'
    if middle_month:
        day = '15'
    if end_month:
        day = '31'

    hour, minute, second, text, year1, month1, day1 = extract_time(text)

    if day1:
        if len(month1) < 2:
            month1 = '0' + month1
        if len(day1) < 2:
            day1 = '0' + day1
        event_date = year1 + '/' + month1 + '/' + day1
    else:
        if len(month) < 2:
            month = '0' + month
        if len(day) < 2:
            day = '0' + day
        event_date = year + '/' + month + '/' + day

    if len(hour) < 2:
        hour = '0' + hour
    if len(minute) < 2:
        minute = '0' + minute
    if len(second) < 2:
        second = '0' + second
    event_time = hour + ':' + minute + ':' + second

    if int(count_dict) > 0:
        count_dict = str(int(count_dict) - 1)

    return event_date, event_time, frequency_dict, count_dict



def user_event_input(qq_name: str, qq_number: str,
               event_date_describe: str, event_time: str, time_delta=['0', '0', '0', '0', '0', '0'], repeat_count='0',
               message="定时提醒~") -> str:
    """
    边界判断并存入文件, 可随意传参\n
    自动获取合法 event_id 并存入 waiting_events.txt\n
    返回 报错/成功 信息
    """

    try:
        if not (time_delta[1] == '0' or time_delta[1] == 0):
            event_date_delta = event_date_describe.split('/')
            event_date_delta = [int(i) for i in event_date_delta]
            if not (event_date_delta[0] < datetime.now().year + 11
                    and 1 <= event_date_delta[1] <= 12
                    and 1 <= event_date_delta[2] <= 31):
                return "[bot]err: [日期范围错误]\n日期: [{}]".format(event_date_describe)
            event_date1 = min(event_date_delta[2], calendar.monthrange(event_date_delta[0], event_date_delta[1])[1])
            event_date = "{}/{}/{}".format(event_date_delta[0], event_date_delta[1], event_date1)
        else:
            event_date = event_date_describe
        insert_date = datetime.strptime(event_date + ' ' + event_time, "%Y/%m/%d %H:%M:%S")
    except Exception as e:
        return "[bot]err: [{}]\n日期: [{}]".format(e, event_date_describe)
    try:
        datetime.strptime(event_time, "%H:%M:%S")
    except Exception as e:
        return "[bot]err: [{}]\n时间: [{}]".format(e, event_time)

    try:
        time_delta = [int(i) for i in time_delta]
    except Exception as e:
        return "[bot]err: [{}]\n步频: [{}]".format(e, ' '.join(map(str, time_delta)))
    non_zero_count = sum(1 for i in time_delta if i != 0)
    index = 0
    if non_zero_count == 1:
        index = next(index for index, i in enumerate(time_delta) if i != 0)
        index += 1
    elif non_zero_count != 0:
        return "[bot]err: [步频参数异常]\n步频: [{}]".format(' '.join(map(str, time_delta)))
    if not (0 <= time_delta[0] < 11 and 0 <= time_delta[1] < 12 and
        0 <= time_delta[2] < 101 and 0 <= time_delta[3] < 24 and
        0 <= time_delta[4] < 301 and 0 <= time_delta[5] < 1001):
        return "[bot]err: [步频参数不合理]\n步频: [{}]".format(' '.join(map(str, time_delta)))
    try:
        repeat_count = int(repeat_count)
    except Exception as e:
        return "[bot]err: [{}]\n重复次数: [{}]".format(e, repeat_count)

    if repeat_count > 20:
        return "[bot]err: [重复次数不合理(2~20)]\n重复次数: [{}]".format(repeat_count)
    if repeat_count > 0:
        if index == 0:
            return "[bot]err: [有重复 却没有步频]\n步频: [{}]\n重复次数: [{}]".format(' '.join(map(str, time_delta)), repeat_count)
    elif repeat_count < 0:
        if index == 0:
            return "[bot]err: [无限重复 却没有步频]\n步频: [{}]\n重复次数: [{}]".format(' '.join(map(str, time_delta)), repeat_count)
        if sum(1 for i in time_delta[3:] if i == 0) != 3:
            return "[bot]err: [无限重复 但步频过小]\n步频: [{}]\n重复次数: [{}]".format(' '.join(map(str, time_delta)), repeat_count)
    else:
        if sum(1 for i in time_delta if i == 0) != 6:
            return "[bot]err: [没有重复次数 却有步频]\n步频: [{}]\n重复次数: [{}]".format(' '.join(map(str, time_delta)), repeat_count)

    if time.mktime(time.localtime()) - time.mktime(time.strptime(event_date + ' ' + event_time, "%Y/%m/%d %H:%M:%S")) >= 0:
        if repeat_count >= 0:
            return "[bot]err: [时间已过期]\n日期: [{}]".format(event_date + ' ' + event_time)
        else:
            repeat_count = -2

    try:
        message = message.strip().replace('\n', ' ').replace('\r', ' ').strip()
        if not message.endswith('\n'):
            message += '\n'
        reply_line = f"{event_date_describe} {event_time} {' '.join(map(str, time_delta))} {repeat_count} {qq_name} {qq_number} {message}"
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_file_path, "waiting_events.txt")
        with open(file_path, "r+", encoding="utf-8") as file:
            file_descriptor = file.fileno()
            msvcrt.locking(file_descriptor, msvcrt.LK_LOCK, 1)

            lines = file.readlines()
            event_id_list = []
            event_id = 1
            if lines:
                for line in lines:
                    split_data = line.strip().split()[0]
                    event_id_list.append(split_data)
                event_id_list = [int(event_id) for event_id in event_id_list]
                event_id_list.sort()
                while event_id in event_id_list:
                    event_id += 1

            for i, line in enumerate(lines):
                line_data_describe = line.split()[1:3]
                line_data1 = line_data_describe[0].split('/')
                line_data2 = min(int(line_data1[2]), calendar.monthrange(int(line_data1[0]), int(line_data1[1]))[1])
                line_data = "{}/{}/{} {}".format(line_data1[0], line_data1[1], line_data2, line_data_describe[1])
                line_datetime = datetime.strptime(line_data, "%Y/%m/%d %H:%M:%S")
                if insert_date < line_datetime:
                    lines.insert(i, f"{event_id} {reply_line}")
                    break
            else:
                lines.append(f"{event_id} {reply_line}")
            file.seek(0)
            file.writelines(lines)
            file.truncate()

    except Exception as e:
        return "[bot]err: 未知错误！\n[{}]".format(e)

    if repeat_count > 0:
        reply_continue = "\n重复: 剩余 [{}] 次~".format(repeat_count + 1)
    elif repeat_count < 0:
        reply_continue = "\n重复: 进行中~"
    elif not all(delta == 0 for delta in time_delta):
        reply_continue = "\n重复: 最后 [1] 次~"
    else:
        reply_continue = "\n重复: 无"

    if repeat_count != 0:
        year_month_day_time = ["年", "月", "天", "小时", "分钟", "秒"]
        reply_continue += "\n间隔: 每 ["
        for i in range(6):
            if time_delta[i] != 0:
                reply_continue += "{}{}".format(time_delta[i], year_month_day_time[i])
                break
        reply_continue += "] 一次"

    message = message.replace('\n', '')
    event_time_describe = '\n\n检测到时间不合理, 已做更改~\n!a ls 查看详情' if repeat_count == -2 else ''

    return "[bot] 成功设置定时提醒~\n\n编号: [{}]{}\n昵称: [{}]\nQQ号: [{}]\n时间: [{}]\n信息: [{}]{}\n\n设置天气: !a set {} <城市名称>".format(
            event_id, reply_continue, qq_name, qq_number, event_date + ' ' + event_time,
            message[:min(40, len(message))] + ("   ..." if len(message) > 40 else ''), event_time_describe, event_id)
