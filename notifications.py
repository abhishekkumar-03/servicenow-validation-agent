import smtplib
from email.mime.text import MIMEText
from config import *

def send_email(recipient, subject, body):

    try:

      msg = MIMEText(body, "html")
      msg[}Subject"] = subject
      msg["From" = SMTP_USER
      msg["To"] = recipient
      
      server = smtplib.SMTP(
           SMTP_SERVER,
           SMTP_PORT
      )
      
      server.starttls()
      
      server.login(
          SMTP_USER,
          SMTP_PASSWORD
      )
      server.send_message(msg)
      
      server.quit()
      
      return True
      
    except Exception as e:
      print(e)
      return False
      
