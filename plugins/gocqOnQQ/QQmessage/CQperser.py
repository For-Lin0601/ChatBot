
import logging
import re

from plugins.gocqOnQQ.QQmessage.components import ComponentTypes


class CQParser:
    @classmethod
    def __replaceChar(cls, string, char, start, end):
        string = list(string)
        del (string[start:end])
        string.insert(start, char)
        return ''.join(string)

    # 获得文本中每一个 CQ 码的起始和结束位置
    @classmethod
    def __getCQIndex(cls, text):
        cqIndex = []
        for m in re.compile("(\[CQ:(.+?)])").finditer(text):
            cqIndex.append((m.start(), m.end()))
        cqIndex.append((len(text), len(text)))
        return cqIndex

    # 转义中括号
    @classmethod
    def escape(cls, text, isEscape=True):
        if isEscape:
            text = text.replace("&", "&amp;")
            text = text.replace(",", "&#44;")
            text = text.replace("[", "&#91;")
            text = text.replace("]", "&#93;")
        else:
            text = text.replace("&amp;", "&")
            text = text.replace("&#44;", ",")
            text = text.replace("&#91;", "[")
            text = text.replace("&#93;", "]")
        return text

    # 将纯文本转换成类型为 plain 的 CQ 码
    @classmethod
    def plainToCQ(cls, text):
        i = j = k = 0
        cqIndex = cls.__getCQIndex(text)
        while i < len(cqIndex):
            if i > 0:
                if i == 1:
                    k += 1
                else:
                    j += 1
            cqIndex = cls.__getCQIndex(text)
            if i > 0:
                l, r = cqIndex[j][k], cqIndex[j + 1][0]
            else:
                l, r = 0, cqIndex[0][0]
            source_text = text[l:r]
            if source_text != "":
                text = cls.__replaceChar(
                    text, f"[CQ:plain,text={cls.escape(source_text)}]", l, r)
            i += 1
        return text

    @classmethod
    def getAttributeList(cls, text):
        text_array = text.split(",")
        text_array.pop(0)
        attribute_list = {}
        for _ in text_array:
            regex_result = re.search(r"^(.*?)=([\s\S]+)", _)
            k = regex_result.group(1)
            if k == "type":
                k = "_type"
            v = cls.escape(regex_result.group(2), isEscape=False)
            attribute_list[k] = v
        return attribute_list

    @classmethod
    def parseChain(cls, text):
        text = cls.plainToCQ(text)
        cqcode_list = re.findall(r'(\[CQ:([\s\S]+?)])', text)
        chain = []
        for x in cqcode_list:
            message_type = re.search(r"^\[CQ\:(.*?)\,", x[0]).group(1)
            try:
                chain.append(ComponentTypes[message_type].parse_obj(
                    cls.getAttributeList(x[1])))
            except Exception as e:
                chain.append(ComponentTypes["unknown"].parse_obj(
                    {"text": message_type}))
                logging.error(
                    f"Protocol: Cannot convert message type: {message_type}\nerror: {e}")
        return chain
