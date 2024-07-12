import json
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

class ChromeSeleniumGetData:

    def __init__(self, driver_path: str):
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service)

        # Connect to SQLite database
        self.conn = sqlite3.connect('parsed_data.db')
        self.cursor = self.conn.cursor()

        # Create table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                manufacturer_info TEXT,
                drug_name TEXT,
                active_ingredient TEXT,
                atc_code TEXT,
                form_dosage TEXT,
                registration_number TEXT,
                registration_date TEXT,
                price TEXT,
                price_date TEXT
            )
        ''')
        self.conn.commit()

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
            parsed_data = self.parse_html(html_content)
            all_data.extend(parsed_data)

        return all_data

    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        data = []
        rows = soup.find_all('tr', class_='')

        for row in rows:
            cells = row.find_all('td')

            if len(cells) == 11:
                record = (
                    cells[1].text.strip(),
                    cells[2].text.strip(),
                    cells[3].find('a').text.strip() if cells[3].find('a') else '',
                    cells[4].text.strip(),
                    cells[5].text.strip(),
                    cells[6].text.strip(),
                    cells[7].find('a').text.strip() if cells[7].find('a') else '',
                    cells[8].text.strip(),
                    cells[9].text.strip(),
                    cells[10].text.strip()
                )

                # Insert record into SQLite database
                self.cursor.execute('''
                    INSERT INTO drugs (
                        company_name, manufacturer_info, drug_name, active_ingredient,
                        atc_code, form_dosage, registration_number, registration_date,
                        price, price_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', record)

        self.conn.commit()
        return data

    def save_to_json(self, data, filename='data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def run(self):
        self.get_data()
        parsed_data = self.paginate_and_parse()
        self.driver.quit()
        print(f"Total records parsed: {len(parsed_data)}")
        self.save_to_json(parsed_data, filename='parsed_data.json')

        # Close SQLite connection
        self.conn.close()

if __name__ == '__main__':
    chrome_driver = ChromeSeleniumGetData(driver_path='./drivers/chromedriver-mac-arm64/chromedriver')
    chrome_driver.run()
