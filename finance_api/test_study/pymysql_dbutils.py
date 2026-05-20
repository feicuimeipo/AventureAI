# 建立链接
# cursorclass 游标的类
# pymysql.cursors.DictCursor：以字曲的方式
import pymysql


class MyORM:
    table_name = ""

    def __init__(self, table_name, **kwargs):
        self.columns = None
        if len(table_name) == 0:
            raise Exception("表名不能为空！")
        self.table_name = table_name
        self.conn = pymysql.connect(host="47.99.219.51",
                                    user="root",
                                    password="123654",
                                    database="python_study",
                                    cursorclass=pymysql.cursors.DictCursor,
                                    charset="utf8",
                                    # autocommit=True
                                    )
        self.cursor = self.conn.cursor()
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def query(self, select_param, where_params):
        sql = ""
        if select_param is not None and select_param is list:
            sql = "select %s from %s" % (",".join(select_param), self.table_name)
        else:
            sql = "select * from %s" % self.table_name

        if where_params is not None:
            sql += " where 1=1 "
            for k, v in where_params.items():
                sql += " and %s='%s'" % (k, v)

        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def queryOne(self, select_param=None, **where_params):
        sql = "select"

        if select_param is not None and type(select_param) is list:
            for i in select_param:
                sql += " {},".format(i)
            sql = sql[:-1] + " from %s" % self.table_name
        else:
            sql += "* from %s" % self.table_name

        if where_params is not None:
            sql += " where 1=1 "
            for k, v in where_params.items():
                sql += " and %s='%s'" % (k, v)

        # print(sql)
        self.orm.cursor.execute(sql)
        return self.cursor.fetchone()

    def insert(self, **kwargs):
        if kwargs is None:
            raise Exception("字段与值不能为空")

        keys = []
        values = []
        for k, v in kwargs.items():
            keys.append(k)
            values.append("'{}'".format(v))

        sql = "insert into %s(%s) values(%s)" % (self.table_name, ",".join(keys), ",".join(values))
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()


class Model:
    columns = None

    # table_name = ""

    def __init__(self):
        self.table_name = self.__getattribute__("table_name")
        self.orm = MyORM(table_name=self.table_name)

    # 通过链试操作，指定查询的列，就是一顿点，然后调用各种操作方法
    def field(self, select_param):
        self.columns = select_param
        return self

    def query(self, **where_params):
        if where_params is not None:
            return self.orm.query(self.columns, where_params)
        else:
            return self.orm.query(self.columns)

    # def queryAll(self):
    #     return MyORM().query()
    #
    # def queryOne(self, **where_params):
    #     return MyORM().queryOne(where_params)

    def insert(self, ):
        pass


class User(Model):
    table_name = "sys_user"

    # def insert(self):
    #     return self.orm.insert(sys_user_id=214, username="a", real_name="b")


if __name__ == '__main__':
    user = User()
    # user.field(["sys_user_id", "username", "real_name"])
    re = user.field(["sys_user_id", "user_name", "real_name"]).query(sys_user_id="1633833655917559809")
    print(re)
