# -*- coding: utf-8 -*-
from typing import Dict, Any

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class BaseModel(DeclarativeBase):
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        # # 遍历类属性 (排除特殊方法和属性)
        # for key, value in self.__class__.__dict__.items():
        #     if not key.startswith('__') and not callable(value):
        #         result[key] = value

        # 遍历实例属性
        for key, value in self.__dict__.items():
            if key == '_sa_instance_state':
                continue
            if hasattr(value, 'to_dict') and callable(getattr(value, 'to_dict')):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result