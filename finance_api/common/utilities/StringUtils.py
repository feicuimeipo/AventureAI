# -*- coding: utf-8 -*-
import uuid

def lastIndexOf(string: str, substr: str) -> int:
    if string is None or substr is None:
        raise ValueError("string and substr could not be None.")
    elif not (isinstance(string, str) and isinstance(substr, str)):
        raise TypeError("string and substr must be str type.")
    elif not (len(string) > 0 and 0 < len(substr) <= len(string)):
        raise TypeError("string and substr value must be non empty, "
                        "and string's length must more over than substr's length.")
    last_index = -1
    idx = 0
    while True:
        try:
            index = string.index(substr, idx)
            last_index = index
            idx = index + len(substr)
        except ValueError:
            # 遍历直到substr在string中不存在，
            # 那么直接返回索引last_index
            return last_index

def generate_user_id():
    return str(uuid.uuid4())