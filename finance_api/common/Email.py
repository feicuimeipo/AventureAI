import base64
import os
import smtplib
import ssl
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from app.config import EnvConfig
from common.Logger import getLogger

logger = getLogger((os.path.basename(__file__)))
class EmailClient(object):
    __smtp_server = EnvConfig.smtp_server  # 'smtp.qq.com'
    __smtp_port = EnvConfig.smtp_port  # 或者使用其他端口，例如465（SSL）
    __sender = EnvConfig.email_sender
    __passwd = EnvConfig.email_passwd

    """
    初始化数据
    """
    def __init__(self):
        self.__smtp_server = EnvConfig.smtp_server # 'smtp.qq.com'
        self.__smtp_port =  EnvConfig.smtp_port  # 或者使用其他端口，例如465（SSL）
        self.__sender = EnvConfig.email_sender
        self.__passwd = EnvConfig.email_passwd

    def send_email(self, receiver,title,content):
        encode = base64.b64encode(title.encode('utf-8')).decode('utf-8')

        # 创建 MIME 文本消息
        msg = MIMEMultipart()
        # msg['From'] = Header(f'发件人 <{sender}>', 'utf-8')
        msg['From'] = Header(f'"=?utf-8?B?{encode}=?=" <{self.__sender}>')
        msg['To'] = Header(receiver, 'utf-8')
        msg['Subject'] = Header(title, 'utf-8')
        msg.attach(MIMEText(content, 'html', 'utf-8'))

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.__smtp_server, self.__smtp_port) as server:
                # sserver.ehlo()  # EHLO 命令
                server.starttls(context=context)  # 使用 TLS（如果需要的话）
                server.ehlo()  # 再次 EHLO 命令以确认 TLS 生效
                server.login(self.__sender, self.__passwd)
                server.sendmail(self.__sender, receiver, msg.as_string())
                server.quit()  # 关闭连接
            logger.info("邮件发送成功")
        except smtplib.SMTPAuthenticationError as e:
            logger.error(e)

    def send_verification_code(self, receiver, code):
        content = """
            <div style="text-align: center; height: 500px; width: 100%;line_height: 500px;font-size:16px"> 您的验证码是<h1 style='color:red'>{}。</h1>
            
            
            感谢使用! <br/>
                        
            VentureAi
            </div>
        """.format(code)
        title = "Welcome to VentureAI"

        return self.send_email(receiver, title, content);


