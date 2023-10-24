from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
from loguru import logger


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


smtp_server = "smtp.gmail.com"
smtp_port = 465
smtp_username = "woyue02@gmail.com"
smtp_password = "tfmttduwpqezmvjk"

aio_email_sender = EmailSender(smtp_server, smtp_port, smtp_username, smtp_password)

# 使用示例
if __name__ == "__main__":
    import asyncio

    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "woyue02@gmail.com"
    smtp_password = "tfmttduwpqezmvjk"

    sender = EmailSender(smtp_server, smtp_port, smtp_username, smtp_password)

    from_email = smtp_username
    to_email = "woyue02@gmail.com"
    subject = "转发备忘"
    body = "邮件备忘：闹钟提醒"

    asyncio.run(sender.send(from_email, to_email, subject, body))
