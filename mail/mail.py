import yagmail
from dotenv import load_dotenv
import os

load_dotenv()


class Email():
    def __init__(self, xlsxFile = None):
        self.user = os.getenv('EMAIL_SENDER')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.conn = yagmail.SMTP(user=self.user, password=self.password)
        
        self.send_mail()
    
    def send_mail(self):
        self.conn.send(to='riannovais3@gmail.com', subject="Oi")
        


    


