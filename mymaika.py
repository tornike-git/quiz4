import requests
from bs4 import BeautifulSoup
from time import sleep
import random
import csv
import sqlite3

file = open('myMaika.csv', 'w', encoding='UTF-8_sig', newline='\n')
file_object = csv.writer(file)
file_object.writerow(['კატეგორია', 'წარწერა', 'ფასი'])

page = 1

while page <= 10:
    url = f'https://mymaika.ge/page/{page}/'

    r = requests.get(url)
    # print(r.status_code)
    # print(url)
    # print(r.headers)
    content = r.text

    soup = BeautifulSoup(content, 'html.parser')
    container = soup.find('div', class_='shop-container')
    product = container.find_all('div', class_='col-inner')

    for each in product:
        category = each.p.text.strip()
        category = category.replace('კატეგორიები', 'კატეგორიის გარეშე')

        comment = each.find('p', class_='name')
        title = comment.text

        dollar = each.find('span', class_='woocommerce-Price-amount')
        price = dollar.text

        print(category, title, price)
        file_object.writerow([category, title, price])

        connection = sqlite3.connect("my_maika_ge.sqlite")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO clothes (category, inscription, price) VALUES (?,?,?)", (category, title, price))
        connection.commit()

    page += 1
    # print(page)
    s = random.randint(1, 3)
    print(s)
    sleep(s)

file.close()

# cursor.execute('''CREATE TABLE IF NOT EXISTS clothes
#               (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                category VARCHAR(25),
#                inscription VARCHAR(25),
#                price FLOAT)
# ''')
