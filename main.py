import csv
import requests
import bs4 as bs

URL = 'https://data.uoi.ua/contest/uoi/2024/results'

CSV_OUTPUT_HEADER = ['#', 'Name', 'Region', 'Points', 'Grade']

source = requests.get(URL)
site = bs.BeautifulSoup(source.content, 'html.parser')
table_head = site.select('.table > thead > tr > th')
table_body = site.select('.table > tbody > tr')
TABLE = []

header = []
for td in table_head:
    header.append(td.text.lower())

for tr in table_body:
    row_body = []
    for td in tr.select('td'):
        td_text = td.text
        if td_text.isdigit():
            td_text = int(td_text)
        row_body.append(td_text)
    TABLE.append({header[i]: row_body[i] for i in range(len(header))})

places = {
    'I': [],
    'II': [],
    'III': [],
}

for row in TABLE:
    place = row['дип.']
    if place in places:
        places[place].append(row)

for place in places:
    with open(f'{place}.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(CSV_OUTPUT_HEADER)

        i = 1
        for row in places[place]:
            writer.writerow([i, row["ім'я"], row['команда'], row['сума'], row['клас']])
            i += 1
        
