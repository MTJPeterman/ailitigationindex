import csv
import requests
from bs4 import BeautifulSoup

def scrape_url(company):
    # Generic scraping logic using a default news search approach
    # Replace with company-specific URLs or a search API if needed
    base_url = "https://news.google.com/search?q={}+site:*.com+ai+claims"
    search_url = base_url.format(company.replace(" ", "+"))
    try:
        response = requests.get(search_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find('a', href=True, string=lambda text: 'ai' in text.lower() or 'claims' in text.lower() if text else False)
        return link['href'] if link else '#'
    except Exception:
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
