import json
import logging
import uuid
from datetime import datetime
import base64



def class_to_json(obj, exclude_private=True, exclude_methods=True):
    """
    将类的实例属性转换为JSON字符串

    Args:
        obj: 类的实例对象
        exclude_private: 是否排除以_开头的私有属性
        exclude_methods: 是否排除方法

    Returns:
        str: JSON格式的字符串
    """
    if not hasattr(obj, '__dict__'):
        raise TypeError("Input object is not a class instance")

    # if isinstance(value, (list, tuple))

    # 获取对象的所有属性
    attributes = {}

    for key, value in obj.__dict__.items():
        # 排除私有属性
        if exclude_private and key.startswith('_'):
            continue

        # 排除方法
        if exclude_methods and callable(value):
            continue

        # 处理嵌套对象
        if hasattr(value, '__dict__'):
            # 递归处理嵌套的类实例
            attributes[key] = json.loads(class_to_json(value, exclude_private, exclude_methods))
        elif isinstance(value, (list, tuple)):
            # 处理列表或元组中的嵌套对象
            processed_list = []
            for item in value:
                if hasattr(item, '__dict__'):
                    processed_list.append(json.loads(class_to_json(item, exclude_private, exclude_methods)))
                else:
                    processed_list.append(item)
                # processed_list.append(class_to_json(item, exclude_private, exclude_methods))
            attributes[key] = processed_list
        elif isinstance(value, dict):
            # 处理字典中的嵌套对象
            processed_dict = {}
            for k, v in value.items():
                if hasattr(v, '__dict__'):
                    processed_dict[k] = class_to_json(v,exclude_private, exclude_methods)
                    #processed_dict[k] = json.loads(class_to_json(v, exclude_private, exclude_methods))
                elif isinstance(v, bytes):
                    try:
                        processed_dict[k] = v.decode('utf-8')
                    except UnicodeDecodeError:
                        processed_dict[k] = base64.b64encode(key).decode('ascii')
                elif isinstance(v, datetime):
                    processed_dict[k] = v.isoformat()
                else:
                    processed_dict[k] = v
            attributes[key] = processed_dict
        elif isinstance(value, bytes):
            try:
                attributes[key] = value.decode('utf-8')
            except UnicodeDecodeError:
                attributes[key] = base64.b64encode(key).decode('ascii')
        elif isinstance(value, datetime):
            attributes[key] = value.isoformat()
        elif isinstance(value, uuid.UUID):
            attributes[key]  = str(value)
        else:
            # 基本数据类型直接添加
            attributes[key] = value

    # 转换为JSON字符串
    try:
        #json_str = json.dumps(attributes, ensure_ascii=False, indent=2)
        json_str = json.dumps(attributes, ensure_ascii=False,  indent=2)
        return json_str
    except TypeError as e:
        logging.error(e,exc_info=True)
        raise TypeError(f"Failed to serialize object to JSON: {str(e)}")

