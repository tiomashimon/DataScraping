import scrapy
import json
import psycopg2

class DepartmentsSpider(scrapy.Spider):
    name = 'departments'
    start_urls = ['https://knu.ua/ua/departments']

    # Список непотрібних текстів
    unnecessary_texts = [
        "Інформація", "Підрозділи університету", "Абітурієнтам", 
        "Наука", "Студентам", "Ресурси", "Новини", "Пошук", "en"
    ]

    def parse(self, response):
        # Знаходимо всі посилання на факультети
        faculty_links = response.css('ul.b-references__holder li a.b-references__link')
        
        # Переходимо на сторінки кожного факультету та збираємо дані
        for link in faculty_links:
            faculty_url = link.attrib['href']
            faculty_name = link.css('::text').get().strip()

            # Перевіряємо, чи посилання не містить непотрібних текстів
            if all(text not in faculty_name for text in self.unnecessary_texts):
                yield response.follow(faculty_url, callback=self.parse_faculty, meta={'faculty_name': faculty_name})

    def parse_faculty(self, response):
        # Отримуємо назву факультету
        faculty_name = response.meta['faculty_name']

        # Знаходимо всі теги <li> на сторінці факультету
        li_elements = response.css('ul.b-references__holder li')

        # Перебираємо кожен тег <li>
        for li in li_elements:
            # Отримуємо текст тегу <li>
            department_name = li.css('::text').get().strip()

            # Перевіряємо, чи текст не належить до непотрібних
            if department_name not in self.unnecessary_texts:
                yield {'faculty': faculty_name, 'department': department_name}

    def closed(self, reason):
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
        with open('departments_data.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            for item in data:
                cursor.execute("INSERT INTO departments (faculty, department) VALUES (%s, %s)", (item['faculty'], item['department']))
        connection.commit()

        cursor.close()
        connection.close()
