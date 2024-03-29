import yagmail
from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime
import string
import re

load_dotenv()

#class that receives the excel file with the news, and does all the configuration to send the email, to the emails inserted in the "recipients.txt" file
#first the email and password are received from the .env file, set up by load_dotenv(), then a connection is made using yagmail
#then the emails read from the .txt file by the load_recipients function are added to the list of recipients, then the sendEmail method is called
#where we pass the excel file and the list of recipients
class Email():
    def __init__(self, data, excelFile):
        self.currentDate = datetime.now().strftime("%d/%m/%Y")
        self.data = data
        self.excelFile = excelFile
        self.recipientsFilePath = Path.cwd() / 'mail' / 'recipients.txt'
        self.recipients = []
        self.contentHtmlPath = Path.cwd() / 'mail' / 'content.html'
        self.user = os.getenv('EMAIL_SENDER')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.conn = yagmail.SMTP(user=self.user, password=self.password)
        self.regExValidateEmail = re.compile(r'^(?:[0-9a-z_]+)@(?:(?:[0-9a-z]+)\.(?:[a-z]+)\.?(?:[a-z]+))$', flags=re.M)


        self.load_recipients()
        self.formattedHtml = self.format_message()

        self.send_mail(self.recipients, self.formattedHtml, self.excelFile)

    # this method takes the scrapping dataframe, transforms it into a dictionary and takes the names of the sites, the titles of the news 
    # items and the links, and then iterates over these lists, adding to the string news_content an information item for each news item, 
    # this string will have information about all the strings at the end of the iteration. then we open the .html file and using the template 
    # from the string library, we modify it by the respective variable, thus creating a personalized html that will go to the send email method.
    def format_message(self):
        news_content = ''
        
        dataDict = self.data.to_dict()
        sites = (dataDict['Site'].values())
        titles = (dataDict['Title'].values())
        links = (dataDict['Link'].values())


        for site, title, link in zip(sites, titles, links):
            # print(site, title, link, extractionDate)
            news_content += f'Site: {site}\nTitle: {title}\nLink: {link}\n\n'



        with open(self.contentHtmlPath, 'r', encoding='utf-8') as file:
            html_content = file.read()
            template = string.Template(html_content)
            html_formatted = template.substitute(news_content = news_content, currentDate = self.currentDate)
            html_formatted = html_formatted.strip()
            return html_formatted
            
     
    # this method reads the recipients.txt file that should contain the emails that will be sent, 
    # and assigns the addresses of the emails that will be sent to the self.recipients attribute.
    def load_recipients(self):
         with open(self.recipientsFilePath, 'r') as file:
            recipients = file.read()
            validatedRecipientes = self.regExValidateEmail.findall(recipients)
            print(validatedRecipientes)
            
            self.recipients = validatedRecipientes

    
    # method that receives the addresses that will be sent (recipients), the content 
    # (content that was generated by the format message function, which created a custom html) and the file 
    # (which was generated by the NewsScraper function, which is the spreadsheet with the news information).
    def send_mail(self, recipients, content, file):
        subject = f'News: {self.currentDate}'
        try:
            self.conn.send(to=recipients, subject=subject, contents=content, attachments=file)
            print('Email send sucessfully')
        except Exception as e:
            print(f'ERROR: UNABLE TO SEND EMAIL: {type(e).__name__} ')


    


