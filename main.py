from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from lxml import html
import csv
import requests
import os
import concurrent.futures

class Crawler:
    def __init__(self):
        self.url = 'https://dermnetnz.org/image-library/'
        self.current_path = os.path.dirname(os.path.abspath(__file__))+'/'

    def get_response(self):
        try:
            print('Hitting url')
            bro = webdriver.Chrome('./chromedriver')
            bro.get(self.url)

            WebDriverWait(bro,15).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@class="imageList__group__item"]')))
            source = bro.page_source
            bro.close()
            return str(source)
        except Exception as e:
            print(e)
            return None

    def get_data(self):
        tree = html.fromstring(self.get_response())

        # Getting Title , Url & Image
        Url = ['https://dermnetnz.org'+i for i in tree.xpath('//*[@class="imageList__group__item"]/@href')]
        Titles = tree.xpath('//*[@class="imageList__group__item__copy"]/h6/text()')
        Images = tree.xpath('//*[@class="imageList__group__item__image"]/img/@src')

        all = zip(Titles,Url)
        print('Storing data into CSV file')
        for m, i in enumerate(all,1):
            with open('Output.csv','a',encoding='utf-8',newline='') as f:
                write = csv.writer(f)
                if m == 1:
                    write.writerow(['Sr. No.','name of Dieases','Respective url'])
                    write.writerow([m,i[0],i[1]])
                else:
                    write.writerow([m, i[0], i[1]])

        os.mkdir(self.current_path+'images')
        print('Saving images')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for url in zip(Titles,Images):
                executor.submit(self.Download_images, url)
            print('Download completed.')

    #Dowload images using threading
    def Download_images(self,list):
        response = requests.get(list[1])
        with open(os.path.join(self.current_path+'images',f'{list[0]}.png'.replace(' ','_').replace('/','_')),'wb+') as f:
            f.write(response.content)

#Initiating class
initiate = Crawler()
initiate.get_data()