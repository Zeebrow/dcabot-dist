import smtplib, ssl
#from email import message, policy.SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dca_config import config
from dca_config import SecretsManager as sm
#import config
#import SecretsManager as sm
import logging

logger = logging.getLogger(__name__)

class SendEmailNotification(object):
    def __init__(self, msg, subject, email_to, email_from):
        self.msg = msg
        self.subject = subject
        self.email_to = email_to
        self.email_from = email_from
    
    def get_message_text_file(self):
        pass

    def get_message_html_file(self):
        pass

    def create_message(self):
        email_message = MIMEMultipart("alternative")
        email_message['Subject'] = self.subject
        email_message['From'] = self.email_from
        email_message['To'] = self.email_to
        email_message['Bcc'] = self.email_to
        text = """\
        test message from dcabot
        """
        html = """\
        "<html>
    <body>
        <h1>DCAbot notification</h1>
        <p>This is a test page. And also a reminder to set up https you lazy bum you've even got the proxy figured out.</p>
    </body>
</html>"""
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        email_message.attach(part1)
        email_message.attach(part2)
        return email_message

    def send(self):
        logger.debug(f"Attempting to send email from (self.email_from) to (email_to): Subject: {subject}, Message:{msg}")
        smtp_host = config.smtp_host
        smtp_port = config.smtp_port
        #email_headers = f"From: {email_from} \r\nTo: {email_to}\r\nSubject: {subject}\r\n\r\n"
        #msg = email_headers + msg

        try:
            _smtp_secrets = sm.SecretsManager()
            _context = ssl.create_default_context()
            _server = smtplib.SMTP(smtp_host, smtp_port)
            _server.ehlo()
            _server.starttls(context=_context)
            _server.ehlo()
            _server.login(_smtp_secrets.smtp_username, _smtp_secrets.smtp_password)
            _server.sendmail(self.email_from, self.email_to, self.create_message().as_string())
        except Exception as e:
            logger.error("Something went wrong trying to send email notification.")
            logger.error(f"smtp_host: {smtp_host} smtp_port: {smtp_port} email_to: {self.email_to} email_from: {self.email_from} subject: {self.subject} message: {self.msg}")
            raise e
        finally:
            _server.quit()
            logger.debug("Server connection closed.")


if __name__ == '__main__':
    import sys
    logger.setLevel(logging.DEBUG)
    if len(sys.argv) == 2:
        msg = sys.argv[1]
    elif len(sys.argv) > 2:
        print('Too many args, try putting your message in quotes.')
        exit(1)
    else:
        msg = """
Subject: yello

This is a test message from homelab python script.
"""

    
    send_email_notifications = True
    # AWS SES
    EMAIL_FROM = config.email_from
    EMAIL_TO = config.email_to
    SMTP_HOST = config.smtp_host
    SMTP_PORT = config.smtp_port

    subject = "Test message"
    message = "Test message from homelab"
    s = SendEmailNotification(message, subject, EMAIL_TO, EMAIL_FROM)
    s.send()
