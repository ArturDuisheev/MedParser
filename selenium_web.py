from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

class ChromeSeleniumGetData:

    def __init__(self, driver_path: str) -> str:
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service)

    def get_data(self):
        self.driver.get('https://www.rceth.by/Refbank/reestr_drurregprice/results')

        input_tag = self.driver.find_element(By.ID, 'FProps_0__CritElems_0__Val')
        input_tag.send_keys('Сиафор')

        radio = self.driver.find_element(By.NAME, 'FProps[0].CritElems[0].Excl')
        radio_2 = self.driver.find_element(By.NAME, 'FProps[1].CritElems[0].Excl')
        radio_3 = self.driver.find_element(By.NAME, 'FProps[2].CritElems[0].Excl')
        radio_4 = self.driver.find_element(By.NAME, 'FProps[3].CritElems[0].Excl')
        radio_5 = self.driver.find_element(By.NAME, 'FProps[4].CritElems[0].Excl')
        radio_6 = self.driver.find_element(By.NAME, 'FProps[5].CritElems[0].Excl')
        
        radio.click()
        radio_2.click()
        radio_3.click()
        radio_4.click()
        radio_5.click()
        radio_6.click()

        input_search = self.driver.find_element(By.XPATH, '//input[@type="submit"]')
        input_search.click()



        
