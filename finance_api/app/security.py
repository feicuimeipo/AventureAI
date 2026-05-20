# url白名单过滤芯
from common.utilities.StringUtils import lastIndexOf


def isUrlInWhite(url):
    # 拦截器白名单
    pass_path = ['/', '/login', 'register', '/index*', '/template/*']
    suffix = url.endswith(".png") or url.endswith(".jpg") or url.endswith(".css") or url.endswith(
        ".js") or url.endswith(".mp4") or url.endswith(".mp3") or url.endswith(".ico")

    allow = False
    if suffix or url in pass_path:
        return True
    else:
        for v in pass_path:
            if v.find("*") > -1:
                if v.startswith("/*") or v.startswith("*"):
                    fragment = v[lastIndexOf(v, "*"):]
                    allow = url.endswith(fragment)
                    break
                else:
                    fragment = v[0: v.index("*")]
                    allow = url.startswith(fragment[0])
                    break
        return allow
