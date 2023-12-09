from pydantic import BaseModel
import typing as T

class Friend(BaseModel):
    user_id: int
    nickname: str
    """昵称"""
    remark: T.Optional[str] = ""
    """备注"""
    sex: T.Optional[str] = ""
    age: T.Optional[int] = 0
    source: T.Optional[str] = ""