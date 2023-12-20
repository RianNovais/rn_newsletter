from scraper import NewsScraper
from mail.mail import Email

if __name__ == "__main__":
    ns = NewsScraper()
    e = Email(ns.EXCELPATH)
