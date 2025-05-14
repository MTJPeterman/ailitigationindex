import csv
import requests
from bs4 import BeautifulSoup

def scrape_url(company):
    # Replace with real search API or scraping logic
    if company == "UnitedHealth":
        url = "https://www.unitedhealthgroup.com/newsroom.html"
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            link = soup.find('a', href=True, string=lambda text: 'claims' in text.lower() if text else False)
            return link['href'] if link else '#'
        except Exception:
            return '#'
    return '#'

def update_csv():
    with open('risk_data.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    headers = rows[0]
    url_index = headers.index('Announcement URL')
    updated = False

    for row in rows[1:]:
        if row[url_index] == '#':
            company = row[0]
            new_url = scrape_url(company)
            if new_url != '#':
                row[url_index] = new_url
                updated = True

    if updated:
        with open('risk_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

if __name__ == "__main__":
    update_csv()
            writer.writerows(rows)

if __name__ == "__main__":
    update_csv()
