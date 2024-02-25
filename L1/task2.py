import requests

department_url = "https://knu.ua/ua/departments/geography/"

response = requests.get(department_url)

if response.status_code == 200:
    print(response.text)
else:
    print("Не вдалося отримати доступ до сторінки.")
