from typing import Union


class OpenAiKeysManager:
    """api key管理类, 外部无需关心

    若需要更换配置请更换`session`中的字段

    此处配置为默认配置
    """

    def __init__(self, openai_config: dict, completion_api_params: dict):
        self.openai_config = {}
        """所有api配置字典
        ```python
        {
            "api_key": "sk-xxxxxxx",
            "params": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.8,
                "top_p": 1,
                ...
            },
            "http_proxy": None,
            "reverse_proxy": None,
            "is_plus": bool
        }
        ```"""

        self.index = 0
        """当前默认下标, 注意可能存在临时切换下一个api的情况, 使用tmp_api传参"""

        self.completion_api_params = completion_api_params
        """默认参数"""

        self.plus_openai_config = {}
        """plus api配置字典
        ```python
        {
            "api_key": "sk-xxxxxxx",
            "params": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.8,
                "top_p": 1,
                ...
            },
            "http_proxy": None,
            "reverse_proxy": None,
            "is_plus": True
        }
        ```"""

        self.plus_index = 0
        """plus api下标"""

        for key, value in openai_config.items():
            if isinstance(value, str):
                self.openai_config[key] = {"api_key": value}
            else:
                self.openai_config[key] = value
            if "params" not in self.openai_config[key]:
                self.openai_config[key]["params"] = completion_api_params
            if "http_proxy" not in self.openai_config[key]:
                self.openai_config[key]["http_proxy"] = None
            if "reverse_proxy" not in self.openai_config[key]:
                self.openai_config[key]["reverse_proxy"] = None
            if "is_plus" not in self.openai_config[key]:
                self.openai_config[key]["is_plus"] = False
            if self.openai_config[key]["is_plus"]:
                self.plus_openai_config[key] = self.openai_config[key]

    def has_openai_config(self, tmp_index=None, is_plus=False) -> bool:
        """是否还有可用的api"""
        if is_plus:
            if tmp_index is not None:
                return tmp_index < len(self.plus_openai_config)
            return self.plus_index < len(self.plus_openai_config)
        if tmp_index is not None:
            return tmp_index < len(self.openai_config)
        return self.index < len(self.openai_config)

    def get_index(self, is_plus=False):
        """获取当前api下标"""
        if is_plus:
            return self.plus_index
        return self.index

    def next_api(self, is_plus=False) -> bool:
        """切换到下一个api"""
        if is_plus:
            self.plus_index = self.plus_index + 1
        else:
            self.index = self.index + 1
        return self.has_openai_config(is_plus=is_plus)

    def get_openai_config_by_index(self, tmp_index=None, is_plus=False) -> Union[dict, bool]:
        """获取指定下标的api配置"""
        if tmp_index is None:
            tmp_index = self.index if not is_plus else self.plus_index
        if not self.has_openai_config(tmp_index, is_plus):
            return False
        if is_plus:
            return list(self.plus_openai_config.values())[tmp_index]
        return list(self.openai_config.values())[tmp_index]

    def get_openai_config_name_by_index(self, tmp_index=None, is_plus=False) -> Union[str, bool]:
        """获取指定下标的api名称"""
        if tmp_index is None:
            tmp_index = self.index if not is_plus else self.plus_index
        if not self.has_openai_config(tmp_index, is_plus):
            return False
        if is_plus:
            return list(self.plus_openai_config.keys())[tmp_index]
        return list(self.openai_config.keys())[tmp_index]

    def get_openai_config_by_name(self, name: str) -> Union[dict, bool]:
        """获取指定名称的api配置"""
        if name in self.openai_config:
            return self.openai_config[name]
        return False
