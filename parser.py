from bs4 import BeautifulSoup
from selenium_web import ChromeSeleniumGetData


class Parser:
    

    def parser_data(self):
        driver_path = './drivers/chromedriver-win64/chromedriver.exe'
        web_service = ChromeSeleniumGetData(driver_path=driver_path)
        data = web_service.get_data()
        bs4 = BeautifulSoup(data.text, 'html.parser')
        
