import requests
from datetime import datetime
from bs4 import BeautifulSoup

class NewsScraper():
    def __init__(self):
        self.currentDate = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        print(self.currentDate)
        self.g1_url = 'https://g1.globo.com/'
        self.uol_url = 'https://www.uol.com.br/'
        self.cnn_url = 'https://www.cnnbrasil.com.br/'
        self.terra_url = 'https://www.terra.com.br/noticias/'

        # data = self.scrape_g1(self.g1_url)
        data2 = self.scrape_uol(self.uol_url)
        
    #method that performs scraping on the "g1" website
    def scrape_g1(self, url):
        data = []
        response = requests.get(url)
        if response.status_code != 200:
            print('ERROR')
            return 
        
        response_content = response.text
        
        #creates an beautifulsoup element that will provide us with the scraping
        siteSoup = BeautifulSoup(response_content, 'html.parser')

        # finding the standard news card object, and bringing them all together, they will come in a list, and then we go through this list extracting elements from each news item
        newsList = siteSoup.findAll('div', attrs={'class': 'feed-post-body'})

        for i,news in enumerate(newsList, start=1):
            # mechanism to only get the first 3 news
            if i>3:
                print('G1 Scrapping sucessfully')
                return data
            # Within each news item, we go deeper and take an element from the body of the news, and from it we take the title and the link
            newsbody = news.find('a', attrs={'class': 'feed-post-link gui-color-primary gui-color-hover'})

            title = newsbody.find('p', attrs={'elementtiming' : 'text-ssr'}).text
            link = newsbody['href']

            #adding title and link in the list
            data.append([title, link])

    #method that performs scraping on the "uol" website
    def scrape_uol(self, url):
        data = []
        response = requests.get(url)
        if response.status_code != 200:
            print('ERROR')
            return
        
        response_content = response.text

        siteSoup = BeautifulSoup(response_content, 'html.parser')

        #select the part of the site where you have the news
        sectionNews = siteSoup.find('div', attrs={'class': 'sectionGrid'})

        #fetch all the news with findAll, each news has an "a" tag with the name "hyperlink headline sub", a list of 
        #these news is created, and for each news we will iterate capturing with find, the title and the link
        newsList = sectionNews.findAll('a', attrs={'hyperlink headlineSub__link'})

        # mechanism with "enumerate" to get only the first 3 news items
        for i, news in enumerate(newsList, start=1):
            if i>3:
                print('Scrapping Uol sucessfully')
                print(data)
                return data
            title = news.find('h3', attrs={'class': 'title__element headlineSub__content__title'})
            link = news['href']

            title = (title.text.strip())


            #get the title and link and add it to the data variable
            data.append([title, link])
        
    
        
    
if __name__ == "__main__":
    ns = NewsScraper()
