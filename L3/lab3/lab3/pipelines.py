import json
import psycopg2
import re


class PostgreSQLPipeline:
    def open_spider(self, spider):
        self.file = open('departments_data.json', 'w', encoding='utf-8')
        self.data = []

    def close_spider(self, spider):
        self.file.write(json.dumps(self.data, ensure_ascii=False, indent=4))
        self.file.close()

        # Підключення до бази даних PostgreSQL
        connection = psycopg2.connect(
            dbname='labthird', user='your_username', password='your_password', host='localhost', port='5432'
        )
        cursor = connection.cursor()

        # Створення таблиці для збереження даних
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
                faculty VARCHAR(255),
                department VARCHAR(255)
            )
        """)
        connection.commit()

        # Збереження даних у базу даних
        for item in self.data:
            cursor.execute("INSERT INTO departments (faculty, department) VALUES (%s, %s)", (item['faculty'], item['department']))
        connection.commit()

        cursor.close()
        connection.close()

    def process_item(self, item, spider):
        # Очищення даних від зайвих символів та пробілів
        item['faculty'] = re.sub(r'\s+', ' ', item['faculty']).strip()
        item['department'] = re.sub(r'\s+', ' ', item['department']).strip()
        return item
