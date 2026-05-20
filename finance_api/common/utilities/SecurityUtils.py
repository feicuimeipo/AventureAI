import hashlib


def encryption(pwd):
    if (pwd == '' or pwd is None):
        raise Exception("密码不能为空")
    return hashlib.md5(pwd.encode('utf-8')).hexdigest()
    #return hashlib.md5(pwd.encode()).hexdigest()
