import csv
import requests
from bs4 import BeautifulSoup

def scrape_url(company):
    # Mapping of companies to their news or announcement pages
    url_map = {
        "Meta": "https://about.meta.com/news/",
        "Amperity": "https://amperity.com/newsroom/",
        "Microsoft": "https://news.microsoft.com/",
        "Google": "https://blog.google/technology/",
        "Amazon": "https://aws.amazon.com/blogs/",
        "IBM": "https://www.ibm.com/watson-health/news/",
        "Adobe": "https://www.adobe.com/news/",
        "Salesforce": "https://www.salesforce.com/news/",
        "Oracle": "https://www.oracle.com/news/",
        "NVIDIA": "https://nvidia.com/en-us/news/",
        "Intel": "https://newsroom.intel.com/",
        "Tesla": "https://www.tesla.com/blog/",
        "Apple": "https://www.apple.com/newsroom/",
        "Samsung": "https://news.samsung.com/",
        "Huawei": "https://consumer.huawei.com/",
        "SAP": "https://news.sap.com/",
        "Accenture": "https://www.accenture.com/news/",
        "Deloitte": "https://www2.deloitte.com/",
        "PwC": "https://www.pwc.com/",
        "EY": "https://www.ey.com/",
        "KPMG": "https://home.kpmg/",
        "Cisco": "https://newsroom.cisco.com/",
        "Qualcomm": "https://www.qualcomm.com/news/",
        "Broadcom": "https://www.broadcom.com/news/",
        "Pfizer": "https://www.pfizer.com/news/",
        "GSK": "https://www.gsk.com/en-gb/media/",
        "JPMorgan": "https://www.jpmorganchase.com/news/",
        "Goldman Sachs": "https://www.goldmansachs.com/insights/",
        "Bank of America": "https://newsroom.bankofamerica.com/"
    }
    url = url_map.get(company, "#")
    if url != "#":
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            link = soup.find('a', href=True, string=lambda text: 'ai' in text.lower() or 'claims' in text.lower() if text else False)
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
