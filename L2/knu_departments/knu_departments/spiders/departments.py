import scrapy
import json
import xml.etree.ElementTree as ET
import csv

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

        # Створюємо списки для збереження даних у різних форматах
        data_json = []
        data_xml = ET.Element('departments')
        data_csv = []

        # Перебираємо кожен тег <li>
        for li in li_elements:
            # Отримуємо текст тегу <li>
            department_name = li.css('::text').get().strip()

            # Перевіряємо, чи текст не належить до непотрібних
            if department_name not in self.unnecessary_texts:
                # Додаємо дані до списків
                data_json.append({'faculty': faculty_name, 'department': department_name})
                department_xml = ET.SubElement(data_xml, 'department')
                department_xml.text = department_name
                data_csv.append([faculty_name, department_name])

        # Зберігаємо дані у файли різних форматів
        with open('departments_data.json', 'a', encoding='utf-8') as json_file:
            json.dump(data_json, json_file, ensure_ascii=False, indent=4)
        
        ET.ElementTree(data_xml).write('departments_data.xml', encoding='utf-8', xml_declaration=True)

        with open('departments_data.csv', 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(data_csv)

        self.log(f'Дані факультету {faculty_name} успішно зібрано та збережено у файлах JSON, XML та CSV.')
