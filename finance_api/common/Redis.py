# -*- coding: utf-8 -*-
import json
import redis
from app.config import EnvConfig


class RedisClient:

    """
    Redis公共操作类，封装常用的Redis操作方法。
    """
    def __init__(self):
        host = EnvConfig.redis_host
        port = EnvConfig.redis_port
        password = EnvConfig.redis_password
        decode_responses = True
        """
        初始化Redis连接。
        :param host: Redis服务器地址
        :param port: Redis端口
        :param db: 数据库编号
        :param password: 密码
        :param decode_responses: 是否自动解码响应为字符串
        """
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=int(EnvConfig.redis_db),
            password=password,
            max_connections=50,
            decode_responses=decode_responses
        )
        self.r = redis.Redis(connection_pool=self.pool)
        try:
            ping = self.r.ping()
            print("Redis 连接成功！%s" % ping)
        except redis.ConnectionError as e:
            print("Redis连接失败，请检查服务器是否启动",e)


    def set(self, key, value, ex=None):
        """
        设置键值对。
        :param key: 键
        :param value: 值
        :param ex: 过期时间（秒）
        """
        return self.r.set(key, value, ex=ex)

    def setExpire(self,key,ex):
        return self.r.expire(key, ex)

    def expire(self,key,ex):
        return self.r.expire(key, ex)

    def setex(self, key, value, ex):
        """
        设置键值对。
        :param key: 键
        :param value: 值
        :param ex: 过期时间（秒）
        """
        return self.r.setex(key, ex, value)

    def get(self, key):
        """
        获取键对应的值。
        :param key: 键
        :return: 值
        """
        return self.r.get(key)


    def getWithDefault(self, key, defaultValue):
        """
        获取键对应的值。
        :param key: 键
        :return: 值
        """
        value = self.r.get(key)
        if not value:
            return defaultValue
        else:
            return value

    def delete(self, key):
        """
        删除键。
        :param key: 键
        :return: 删除的键数量
        """
        return self.r.delete(key)

    def bulk_delete(self, keys:list[str]):
        """
        删除键。
        :param key: 键
        :return: 删除的键数量
        """
        return self.r.delete(*keys)

    def exists(self, key):
        """
        判断键是否存在。
        :param key: 键
        :return: 存在返回True，否则返回False
        """
        return self.r.exists(key)

    def mset(self, mapping):
        """
        批量设置键值对。
        :param mapping: 键值对字典
        """
        return self.r.mset(mapping)

    def mget(self, keys):
        """
        批量获取键对应的值。
        :param keys: 键列表
        :return: 值列表
        """
        return self.r.mget(keys)

    def incr(self, key, amount=1):
        """
        对键对应的数值进行自增。
        :param key: 键
        :param amount: 自增值
        :return: 自增后的值
        """
        return self.r.incr(key, amount)

    def decr(self, key, amount=1):
        """
        对键对应的数值进行自减。
        :param key: 键
        :param amount: 自减值
        :return: 自减后的值
        """
        return self.r.decr(key, amount)

    def hset(self, name, key, value):
        """
        设置哈希表中的键值对。
        :param name: 哈希表名
        :param key: 字段名
        :param value: 值
        """
        return self.r.hset(name, key, value)


    def hincrby(self,name,key,amount):
        """
        哈希自增
        """
        self.r.hincrby(name,key,amount)

    def hget(self, name, key):
        """
        获取哈希表中字段的值。
        :param name: 哈希表名
        :param key: 字段名
        :return: 值
        """
        return self.r.hget(name, key)

    def hgetall(self, name):
        """
        获取哈希表中所有字段和值。
        :param name: 哈希表名
        :return: 字典形式的字段和值
        """
        return self.r.hgetall(name)

    def lpush(self, name, *values):
        """
        向列表左边插入元素。
        :param name: 列表名
        :param values: 插入的值
        :return: 列表长度
        """
        return self.r.lpush(name, *values)

    def rpush(self, name, *values):
        """
        向列表右边插入元素。
        :param name: 列表名
        :param values: 插入的值
        :return: 列表长度
        """
        return self.r.rpush(name, *values)

    def lrange(self, name, start, end):
        """
        获取列表中指定范围的元素。
        :param name: 列表名
        :param start: 开始索引
        :param end: 结束索引
        :return: 元素列表
        """
        return self.r.lrange(name, start, end)

    def sadd(self, name, *values):
        """
        向集合中添加元素。
        :param name: 集合名
        :param values: 添加的值
        :return: 添加的元素数量
        """
        return self.r.sadd(name, *values)

    def smembers(self, name):
        """
        获取集合中的所有元素。
        :param name: 集合名
        :return: 元素集合
        """
        return self.r.smembers(name)

    def sismember(self, name, value):
        """
        判断元素是否在集合中。
        :param name: 集合名
        :param value: 元素值
        :return: 存在返回True，否则返回False
        """
        return self.r.sismember(name, value)

    def ping(self):
        """
        测试连接是否正常。
        :return: 连接状态
        """
        return self.r.ping()

# if __name__ == '__main__':
#     RedisClient()

