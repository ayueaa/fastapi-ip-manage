from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from loguru import logger

from app.core.config import get_app_settings


class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    async def send(self, from_email: str, to_email: str, subject: str, body: str):
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        try:
            # server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            # server.starttls()
            # server.login(self.smtp_username, self.smtp_password)
            # server.sendmail(self.smtp_username, to_email, msg.as_string())
            await aiosmtplib.send(
                msg,
                hostname=self.smtp_server,
                port=self.smtp_port,
                username=self.smtp_username,
                password=self.smtp_password,
                use_tls=True,
            )
            logger.info(f"邮件发送成功,To {to_email}")
        except Exception as e:
            logger.error(f"邮件发送{to_email}失败,error: {e}")


settings = get_app_settings()


aio_email_sender = EmailSender(
    settings.smtp_server, settings.smtp_port, settings.smtp_username, settings.smtp_password)

# 使用示例
if __name__ == "__main__":
    import asyncio

    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "username"
    smtp_password = "password"

    sender = EmailSender(smtp_server, smtp_port, smtp_username, smtp_password)

    from_email = smtp_username
    to_email = "xx@gmail.com"
    subject = "test"
    body = "test content"

    asyncio.run(sender.send(from_email, to_email, subject, body))
