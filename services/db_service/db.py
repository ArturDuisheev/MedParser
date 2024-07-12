import sqlite3
class ConnectorToSqlite3:
    def __init__(self, connector):
        self.connector = connector
        self.cursor = self.connector.cursor()

    def create_table(self):
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
        self.connector.commit()

    def add_data_in_table(self, record):
        self.cursor.execute('''
            INSERT INTO drugs (
                company_name, manufacturer_info, drug_name, active_ingredient,
                atc_code, form_dosage, registration_number, registration_date,
                price, price_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', record)
        self.connector.commit()

    def close(self):
        self.connector.close()