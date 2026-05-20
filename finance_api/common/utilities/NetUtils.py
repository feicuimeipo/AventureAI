from flask import request


def get_real_client_ip():
    """
    获取客户端真实IP地址
    优先从 X-Forwarded-For 头部获取，以处理代理服务器情况
    """
    # 1. 尝试从 X-Forwarded-For 获取
    # X-Forwarded-For 格式通常为: client, proxy1, proxy2
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if x_forwarded_for:
        # 取第一个IP，即客户端真实IP
        real_ip = x_forwarded_for.split(',')[0]
        return real_ip

    # 2. 如果没有 X-Forwarded-For，尝试 X-Real-IP (某些代理如Nginx配置)
    x_real_ip = request.headers.get('X-Real-IP')
    if x_real_ip:
        return x_real_ip.strip()

    # 3. 最后回退到远程地址 (直连情况或无代理头)
    return request.remote_addr