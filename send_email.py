import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_email(to, content, subtype=None):
    user = os.getenv("USER_EMAIL")
    passkey = os.getenv("USER_KEY")

    msg = EmailMessage()

    msg["Subject"] = "Invoice for your shopping at ABC"

    msg["From"] = "ABC Billing Systems <rohanyeluru@gmail.com>"

    msg["To"] = to

    if subtype:
        msg.set_content(content, subtype="html")
    else:
        msg.set_content(content)
    
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(user, passkey)
    server.send_message(msg)
    server.quit()