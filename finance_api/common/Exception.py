# -*- coding: utf-8 -*-

class EmailExistException(Exception):
    pass

class DatabaseRowNotFoundException(Exception):
    pass


class AccessTokenLogoutException(Exception):
    pass

class ElasticSearchErrorException(Exception):
    pass