from pathlib import Path

from mako.template import Template
from sqlalchemy import create_engine, inspect

from database import db_conn

ignored_fields = []

def get_column_mapped_type(fieldType="",nullable=True):
    result = ""
    python_type = ""
    pgvector_type = ""

    if fieldType.upper() == "INTEGER" or fieldType.upper() == "SMALLINT" or fieldType.upper() == "BIGINT":
        result = 'int'
    elif (fieldType.upper().startswith("VARCHAR") or fieldType.upper().startswith("CHAR")
          or fieldType.upper().startswith("LONGTEXT") or fieldType.upper().startswith("TEXT"))\
          or fieldType.upper().startswith("INET") :
        result = 'str'
    elif fieldType.upper().startswith("JSONB") or fieldType.upper().startswith("'JSONB"):
        result = 'dict'
    elif fieldType.upper().startswith("DATE") or fieldType.upper().startswith('DATE'):
        result = 'datetime.date'
        python_type = 'datetime'
    elif fieldType.upper().startswith("DATETIME") or fieldType.upper().startswith('TIMESTAMP'):
        result = 'datetime.datetime'
        python_type = 'datetime'
    elif fieldType.upper().startswith("UUID"):
        result = 'uuid.UUID'
        python_type = 'uuid'
    elif fieldType.upper().startswith("FLOAT"):
        result = 'float'
    elif fieldType.upper().startswith("BOOLEAN") or fieldType.upper().startswith("BOOL"):
        result = 'bool'
    elif fieldType.upper().startswith("DECIMAL") or fieldType.upper().startswith("NUMERIC"):
        result = 'decimal.Decimal'
        python_type = 'decimal'
    elif fieldType.upper().startswith("ARRAY"):
        result = 'list'
    elif fieldType.upper().startswith("VECTOR"):
        result = 'list'
    if nullable:
        result = f"Optional[{result}]"

    return result,python_type


def get_table_info_v2(db_url, table_name):
    """
    获取表字段
    :param db_url:
    :param dburl:
    :param table_name: 表名
    :return: 字段列表
    """
    print("db_url="+db_url)
    engine = create_engine(db_url)
    insp = inspect(engine)
    primary_keys = insp.get_pk_constraint(table_name)["constrained_columns"]
    table_info = insp.get_columns(table_name)
    columns = []

    # 包名
    columns_type_package = []
    python_type_package = []
    pgvector_type_package = []
    postgresql_type_package = []
    for table in table_info:
        field_name = str(table.pop('name'))
        if ignored_fields.__contains__(field_name):
            continue

        # print("name={}".format(field_name))
        column_type = table.get('type').__visit_name__  # 获取类型名称
        if column_type.upper() == "USER_DEFINED" or column_type.upper()== "NULL":
            pass
        elif  column_type.upper() == "INET" or column_type.upper() == "JSONB" :
            postgresql_type_package.append(column_type)
        else:
            columns_type_package.append("TEXT" if column_type=="LONGTEXT" else column_type)

        nullable = False
        mapped_column = ''
        for k, v in table.items():
            if (k == "autoincrement" and not v) or (k == "default") or (k == "identity") or (k =='comment' and not v):
                continue
            if k == 'nullable': nullable = bool(v)
            if k == 'comment': v = f'"""{v if v else '' }"""'

            if k != 'type' and k!= 'nullable':  # 获取类型
                mapped_column += k + '=' + str(v) + ', '  # 字符串拼接
            elif k == 'type':
                str_v = v.__class__.__name__
                if hasattr(v,'item_type') and v.item_type:
                    str_v = f'{str_v}({v.item_type})'
                    columns_type_package.append(str(v.item_type))

                elif hasattr(v, 'length') and v.length and hasattr(v,'decimal') and v.decimal:
                    str_v = f'{str_v}({v.length},{v.decimal})'
                elif hasattr(v, 'length') and v.length:
                    str_v = f'{str_v}({v.length})'

                if (str_v.upper().startswith("NULL") and
                        (field_name.lower().__contains__("embedding") or field_name.lower().__contains__("vector"))):
                            str_v = "VECTOR"
                            column_type = "VECTOR"
                            pgvector_type_package.append("VECTOR")

                mapped_column += ("TEXT, " if str_v == "LONGTEXT" else str_v)  + ', '

        mapped_python,python_type = get_column_mapped_type(column_type, nullable)
        mapped_sqlalchemy = mapped_column + 'primary_key=True' if field_name in primary_keys else mapped_column[:-2]  # 去掉最后的逗号，加上括号
        if python_type: python_type_package.append(python_type)

        column = f"{field_name}: Mapped[{mapped_python}] = mapped_column({mapped_sqlalchemy})"
        columns.append(column)
    # 去重
    columns_package = list(set(columns_type_package))
    python_package =  list(set(python_type_package))
    pgvector_package = list(set(pgvector_type_package))
    postgresql_type_package = list(set(postgresql_type_package))

    packages = {"sqlalchemy": columns_package,
                "python": python_package,
                "pgvector": pgvector_package,
                "postgresql": postgresql_type_package
                }

    return columns, packages

def getEntityName(table_name):
    entityName = "";
    components = table_name.split('_')
    for component in components:
        entityName += component.capitalize()
    return entityName;

def check_and_create_folder(folder_path):
    path_obj = Path(folder_path)
    # 检查路径是否已经存在
    try:
        if path_obj.exists() or folder_path == ".":
            if path_obj.is_dir():
                pass
            else:
                raise Exception(f"[ERROR] 路径 '{folder_path}' 存在但不是文件夹")
        else:
            path_obj.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise Exception(f"[ERROR] 权限不足，无法创建文件夹 '{folder_path}'")
    except Exception as e:
        raise Exception(f"[ERROR] 创建文件夹时发生未知错误: {e}")


def generate_by_moke(db_url, tables=[], out_path="."):
    check_and_create_folder(out_path)

    for table_name in tables:
        entityName = getEntityName(table_name)
        template = Template(filename='entity.txt')
        columns, packages = get_table_info_v2(db_url, table_name)

        rendered = template.render(table_name=table_name, entity_name=entityName, columns=columns, package=packages)
        output_file = out_path + "/" + getEntityName(table_name) + ".py"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print(f"实体类已生成至 {output_file}")


# -------------------------- 示例调用 --------------------------
if __name__ == "__main__":
    # 替换为你的数据库连接信息
    # DB_URL = "mysql+pymysql://root:123654@47.99.219.51:3306/python_study"
    generate_by_moke(db_conn.db_url(), ["Platform_celery_task_log"], "../entity")
