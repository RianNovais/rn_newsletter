import yagmail
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime

load_dotenv()

#class that receives the excel file with the news, and does all the configuration to send the email, to the emails inserted in the "recipients.txt" file
#first the email and password are received from the .env file, set up by load_dotenv(), then a connection is made using yagmail
#then the emails read from the .txt file by the load_recipients function are added to the list of recipients, then the sendEmail method is called
#where we pass the excel file and the list of recipients
class Email():
    def __init__(self, excelFile):
        self.currentDate = datetime.now().strftime("%d/%m/%Y")
        self.excelFile = excelFile
        self.recipientsFilePath = Path.cwd() / 'mail' / 'recipients.txt'
        self.recipients = []
        self.user = os.getenv('EMAIL_SENDER')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.conn = yagmail.SMTP(user=self.user, password=self.password)

        self.load_recipients()

        self.send_mail(self.excelFile, self.recipients)

    def load_recipients(self):
         with open(self.recipientsFilePath, 'r') as file:
            recipients = file.read().splitlines()
            for recipient in recipients:
                self.recipients.append(recipient)
    
    def send_mail(self, file, recipients):
        subject = f'Webscrapping {self.currentDate}'
        content = f'Noticias do dia, extraidas automaticamente dos sites G1, UOL, CNN, TERRA'
        try:
            self.conn.send(to=recipients, subject=subject, contents=content, attachments=file)
            print('Email send sucessfully')
        except:
            print('ERROR: UNABLE TO SEND EMAIL')


    


