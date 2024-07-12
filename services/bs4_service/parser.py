import sqlite3

from bs4 import BeautifulSoup
from services.db_service.db import ConnectorToSqlite3


class Parser:
    def __init__(self):
        self.db = ConnectorToSqlite3(connector=sqlite3.connect('data/parsed_data.db'))

    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        data = []
        rows = soup.find_all('tr', class_='')

        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 11:
                record: tuple = (
                    cells[1].text.strip(),
                    '\n'.join(line.strip() for line in cells[2].text.splitlines() if line.strip()),
                    cells[3].find('a').text.strip() if cells[3].find('a') else '',
                    cells[4].text.strip(),
                    cells[5].text.strip(),
                    cells[6].text.strip(),
                    cells[7].find('a').text.strip() if cells[7].find('a') else '',
                    cells[8].text.strip(),
                    cells[9].text.strip(),
                    cells[10].text.strip()
                )

                #создание таблицы
                self.db.add_data_in_table(record)
        return data