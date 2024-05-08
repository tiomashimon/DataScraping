import requests
from bs4 import BeautifulSoup
import csv

def extract_data_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    items = []
    
    ads = soup.find_all('a', class_='css-z3gu2d')[:50]
    for ad in ads:
        ad_url = 'https://www.olx.ua/' + ad['href']
        ad_response = requests.get(ad_url)
        ad_soup = BeautifulSoup(ad_response.text, 'html.parser')
        
        title = ad_soup.find('h4', class_='css-1juynto').text.strip()
        price = ad_soup.find('h3', class_='css-12vqlj3').text.strip()
        location = ad_soup.find_all('p', class_='er34gjf0')[1].text.strip()
        date = ad_soup.find('span', class_='css-19yf5ek').text.strip()
        
        items.append({
            'Title': title,
            'Price': price,
            'Location': location,
            'Date': date
        })
    
    return items

def save_to_csv(data, filename='output.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Price', 'Location', 'Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in data:
            writer.writerow(item)

# Приклад використання:
url = 'https://www.olx.ua/uk/hobbi-otdyh-i-sport/velo/?currency=UAH'
data = extract_data_from_page(url)
save_to_csv(data, 'bikes_data.csv')
