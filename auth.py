import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import random

def gen_otp():
    otp=''
    for i in range(6):
        val= '1234567890'
        nums= list(val)
        otp += random.choice(nums)
    return otp


def mail(email_id, nm,otp):
    PORT = 587
    EMAIL_SERVER= "smtp-mail.outlook.com"

    sender_email= "yourmail@outlook.com"
    passwd_email= "yourpassword"


    def send_mail(subject, receiver_mail, name, otp):
        msg= EmailMessage()
        msg["Subject"]= subject
        msg["From"]= formataddr(("Cabs", f"{sender_email}"))
        msg["To"]= receiver_mail

        msg.set_content(
           f"""Hi {name},\nThe Generated One Time Password for your login request is \n{otp}
            \n If it wasn't you then please report back on the same email address\n\nRegards\nSupport Team
            """
        )
        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()
            server.login(sender_email, passwd_email)
            server.sendmail(sender_email, receiver_mail, msg.as_string())
    try:
        send_mail("Login Request", email_id, nm, otp)
        return 'Done'
    except:
        return "error" 
