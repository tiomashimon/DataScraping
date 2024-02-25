import requests
from bs4 import BeautifulSoup


def get_links_list(url, faculty_name):
    # Виконуємо запит на сторінку
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        li_elements = soup.find_all('li')

        unnecessary_texts = [
            "Інформація", "Підрозділи університету", "Абітурієнтам",
            "Наука", "Студентам", "Ресурси", "Новини", "Пошук", "en"
        ]

        if li_elements:
            with open('faculty_li_elements.txt', 'a', encoding='utf-8') as f:
                for li in li_elements:
                    if li.text.strip() not in unnecessary_texts:
                        f.write(faculty_name + ": " + li.text.strip() + '\n')
            print("Елементи <li> знайдено та додано до файлу faculty_li_elements.txt")
        else:
            print("Не вдалося знайти жодного елемента <li> на сторінці:", url)
    else:
        print("Не вдалося отримати доступ до сторінки:", url)


main_url = "https://knu.ua/ua/departments"

response_main = requests.get(main_url)

if response_main.status_code == 200:
    soup_main = BeautifulSoup(response_main.text, 'html.parser')

    department_list = soup_main.find('ul', class_='b-references__holder').find_all('li')

    for department in department_list:
        department_url = "https://knu.ua" + department.a['href']
        department_name = department.a.text.strip()

        get_links_list(department_url, department_name)
else:
    print("Не вдалося отримати доступ до сторінки.")
