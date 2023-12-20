import requests
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd


class NewsScraper():
    def __init__(self):
        self.currentDate = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.g1_url = 'https://g1.globo.com/'
        self.uol_url = 'https://www.uol.com.br/'
        self.cnn_url = 'https://www.cnnbrasil.com.br/ultimas-noticias/'
        self.terra_url = 'https://www.terra.com.br/noticias/'

        # these functions perform the scrapping, and return dataframes with the data in columns "Site, Title, Link and Date of extraction". 
        newsDataG1 = self.scrape_g1(self.g1_url)
        newsDataUol = self.scrape_uol(self.uol_url)
        newsDataTerra = self.scrape_terra(self.terra_url)
        newsDataCNN = self.scrape_cnn(self.cnn_url)
        
        # this function takes each dataframe returned by the functions and concatenates them all into a single dataframe, 
        # which will be the final dataframe with all the data tabulated into columns
        self.dfAllNews = self.concat_dataframes(newsDataG1, newsDataUol, newsDataTerra, newsDataCNN)


    def concat_dataframes(self, g1Data, uolData, terraData, cnnData):
        frames = [g1Data, uolData, terraData, cnnData]
        allNewsDF = pd.concat(frames, ignore_index=True)

        return allNewsDF
        
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
                dfDataG1 = pd.DataFrame(data=data)
                # print(data)
                return dfDataG1
            # Within each news item, we go deeper and take an element from the body of the news, and from it we take the title and the link
            newsbody = news.find('a', attrs={'class': 'feed-post-link gui-color-primary gui-color-hover'})

            title = newsbody.find('p', attrs={'elementtiming' : 'text-ssr'}).text
            link = newsbody['href']

            #adding title and link dict, in the data list, this variable data will be transformed into a dataframe
            data.append({'Site': 'G1', 'Title': title, 'Link': link, 'Extraction Date': self.currentDate})


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
                dfDataUol = pd.DataFrame(data=data)
                # print(data)
                return dfDataUol
            title = news.find('h3', attrs={'class': 'title__element headlineSub__content__title'})
            link = news['href']

            title = (title.text.strip())


            # taking the title and link and adding it to the date variable, like a dictionary, also passing the name of the site and the date of extraction
            data.append({'Site': 'UOL', 'Title': title, 'Link': link, 'Extraction Date': self.currentDate})

    
    #method that performs scraping on the "terra" website
    def scrape_terra(self, url):
        data = []
        response = requests.get(url)
        if response.status_code != 200:
            print('ERROR')
            return
        
        response_content = response.text

        siteSoup = BeautifulSoup(response_content, 'html.parser')
        #filtering by the container with the news
        containerNews = siteSoup.find('div', attrs={'class': 'table-range-grid-step app-t360-subject-table__rect--grid'})

        #in this container we take the element that every news item has, and we do a findAll to get all the news items

        newsList = containerNews.findAll('div', attrs={'class': 'card-news__image'})
        
        #for each news item in the list of news items that we took from theNews container using findAll on the specific element, we will now take
        #the title and link of each news item
        #put an enumerate to get only the first 3 news items
        for i, news in enumerate(newsList, start=1):
            if i>3:

                print('Terra scrapping sucessfully')
                dfDataTerra = pd.DataFrame(data=data)
                return dfDataTerra
            
            title = news.find('img')['alt']
            link = news.find('a', attrs={'class': 'card-news__url'})['href']

            #add the title and link of the news item to the date variable
            data.append({'Site': 'TERRA', 'Title': title, 'Link': link, 'Extraction Date': self.currentDate})


    #method that performs scraping on the "cnn" website
    def scrape_cnn(self, url):
        data = []
        response = requests.get(url)

        if response.status_code != 200:
            print('ERROR')
            return 
        
        response_content = response.text

        siteSoup = BeautifulSoup(response_content, 'html.parser')

        #pegando from beautifulSoup on our website, the container that has the news
        containerNews = siteSoup.find('div', attrs={'class': 'posts col__list'})
        
        # fetching each news item from the container, and from this list that will come from findAll, we will iterate and get the link and title of each news item
        newsList = containerNews.findAll('li', attrs={'class': 'home__list__item'})

        #mechanism with enumerate to pick up only the first 3 news items
        for i, news in enumerate(newsList, start=1):
            if i>3:
                print('CNN scrapping sucessfully')
                dfDataCnn = pd.DataFrame(data=data)
                return dfDataCnn

            link = news.find('a', attrs={'class': 'home__list__tag'})['href']
            title = news.find('h3', attrs={'class': 'news-item-header__title market__new__title'}).text

            data.append({'Site': 'CNN', 'Title': title, 'Link': link, 'Extraction Date': self.currentDate})

