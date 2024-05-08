import requests
from bs4 import BeautifulSoup

# Завантажуємо сторінку
url = "https://www.bbc.com/news"
response = requests.get(url)

# Парсимо HTML
soup = BeautifulSoup(response.text, "html.parser")

# Знаходимо всі елементи <h2> з атрибутом data-testid="card-headline"
headlines = soup.find_all("h2", {"data-testid": "card-headline"})

# Виводимо заголовки новин
print("Заголовки новин з BBC News:")
for headline in headlines:
    print(headline.get_text().strip())
