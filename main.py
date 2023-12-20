from scraper import NewsScraper
from mail.mail import Email

#MAIN FILE
if __name__ == "__main__":
    ns = NewsScraper()
    e = Email(ns.dfAllNews, ns.EXCELPATH)
