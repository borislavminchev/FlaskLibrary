import smtplib, ssl
from email.message import EmailMessage

class EmailService:

    def __init__(self, sender: str, password: str):
        self.sender = sender
        self.password = password
        self.context = ssl.create_default_context()

    def construct_message(self, recipient: str, subject: str, content: str) -> EmailMessage:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipient
        msg.set_content(content)
        return msg
    
    def send_email(self, recipient: str, subject: str, content: str):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as server:
            server.login(self.sender, self.password)
            server.login("b2001bobby@gmail.com", "xntq sqrd ffns zple")
            msg = self.construct_message(recipient, subject, content)
            server.send_message(msg)