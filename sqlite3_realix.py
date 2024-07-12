import json
import sqlite3
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from services.db_service.db import ConnectorToSqlite3
from services.bs4_service.parser import Parser


class ChromeSeleniumGetData:

    def __init__(self, driver_path: str):
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service)
        self.parser = Parser()

        self.db = ConnectorToSqlite3(connector=sqlite3.connect('data/parsed_data.db'))
        self.db.create_table()

    def get_data(self):
        self.driver.get('https://www.rceth.by/Refbank/reestr_drurregprice/results')

        input_tag = self.driver.find_element(By.ID, 'FProps_0__CritElems_0__Val')
        input_tag.send_keys('Сиафор')

        radio_buttons = [
            'FProps[0].CritElems[0].Excl', 'FProps[1].CritElems[0].Excl',
            'FProps[2].CritElems[0].Excl', 'FProps[3].CritElems[0].Excl',
            'FProps[4].CritElems[0].Excl', 'FProps[5].CritElems[0].Excl'
        ]
        for radio_name in radio_buttons:
            radio = self.driver.find_element(By.NAME, radio_name)
            radio.click()

        input_search = self.driver.find_element(By.XPATH, '//input[@type="submit"]')
        input_search.click()
        a_href_count_data = self.driver.find_element(By.XPATH, '//a[@propval="100"]')
        a_href_count_data.click()

    def paginate_and_parse(self):
        all_data = []

        for page_number in range(1, 8):
            page_link = self.driver.find_element(By.XPATH, f'//a[@propval="{page_number}"]')
            page_link.click()
            time.sleep(2)
            html_content = self.driver.page_source
            parsed_data = self.parser.parse_html(html_content)
            all_data.extend(parsed_data)

        return all_data

    def save_to_json(self, data, filename='data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def run(self):
        self.get_data()
        parsed_data = self.paginate_and_parse()
        self.driver.quit()
        print(f"Total records parsed: {len(parsed_data)}")
        self.save_to_json(parsed_data, filename='data/parsed_data.json')

        # Close SQLite connection
        self.db.connector.close()


if __name__ == '__main__':
    chrome_driver = ChromeSeleniumGetData(driver_path='./drivers/chromedriver-mac-arm64/chromedriver')
    chrome_driver.run()
