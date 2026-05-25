# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# 邮箱包导入
import base64
import random
import smtplib
import ssl
import uuid
from email.mime.text import MIMEText
from email.header import Header
# 格式化文件内容
from email.mime.multipart import MIMEMultipart


from common.Logger import getLogger

smtp_server = 'smtp.qq.com'
smtp_port = 587  # 或者使用其他端口，例如465（SSL）
sender = '7844153@qq.com'
passwd = 'djljuwpghjkjbhci'  # 发送邮件的授权码

logger = getLogger()
# content = """
# 您的验证码是: <h1 style='color:red'>{}</h1>
# """.format(random.randint(10000, 99999))
def send_email(receiver, subject, content):
    # receiver = 'xlnian@163.com'
    # text = "来自QQ邮箱的测试邮件"
    encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    # 创建 MIME 文本消息
    msg = MIMEMultipart()
    msg['From'] = Header(f'"=?utf-8?B?{encoded}=?=" <{sender}>')
    msg['To'] = Header('收件人', 'utf-8')
    msg['Subject'] = Header('邮件主题', 'utf-8')
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # sserver.ehlo()  # EHLO 命令
            server.starttls(context=context)  # 使用 TLS（如果需要的话）
            server.ehlo()  # 再次 EHLO 命令以确认 TLS 生效
            server.login(sender, passwd)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()  # 关闭连接
        return True
    except smtplib.SMTPException as e:
        logger.info(f"邮件发送失败: {e}")
        return False


def send_code(receiver):
    code = random.randint(10000, 99999)
    subject = '发送验证码'
    content = """
        您的验证码是: <h1 style='color:red'>{}</h1>
    """.format({code})
    ret = send_email(receiver, subject, content)
    if ret:
        return code
    else:
        return 0