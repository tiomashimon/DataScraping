from bs4 import BeautifulSoup
import requests

url = "https://knu.ua/ua/departments"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    department_list = soup.find('ul', class_='b-references__holder').find_all('li')

    departments = []

    for department in department_list:
        department_url = "https://knu.ua" + department.a['href']
        department_name = department.a.text.strip()

        departments.append((department_name, department_url))

    for name, url in departments:
        print(name + ":", url)
else:
    print("Не вдалося отримати доступ до сторінки.")
