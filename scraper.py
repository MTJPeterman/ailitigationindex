import csv
import requests
from bs4 import BeautifulSoup

def scrape_url(company):
    url_map = {
        "Meta": "https://about.meta.com/news/",
        "Amperity": "https://amperity.com/newsroom/",
        "Microsoft": "https://news.microsoft.com/",
        "Google": "https://blog.google/technology/",
        "Amazon": "https://aws.amazon.com/blogs/",
        "IBM": "https://newsroom.ibm.com/",
        "Adobe": "https://news.adobe.com/",
        "Salesforce": "https://www.salesforce.com/news/",
        "Oracle": "https://www.oracle.com/news/",
        "NVIDIA": "https://nvidia.com/en-us/news/",
        "Intel": "https://www.intel.com/content/www/us/en/newsroom/home.html",
        "Tesla": "https://www.tesla.com/blog/",
        "Apple": "https://www.apple.com/newsroom/",
        "Samsung": "https://news.samsung.com/global",
        "Huawei": "https://consumer.huawei.com/en/press/news/",
        "SAP": "https://news.sap.com/",
        "Accenture": "https://www.accenture.com/us-en/about/newsroom-index",
        "Deloitte": "https://www2.deloitte.com/us/en/pages/about-deloitte/articles/press-releases.html",
        "PwC": "https://www.pwc.com/gx/en/news-room.html",
        "EY": "https://www.ey.com/en_gl/news",
        "KPMG": "https://home.kpmg/xx/en/home/media/press-releases.html",
        "Cisco": "https://newsroom.cisco.com/",
        "Qualcomm": "https://www.qualcomm.com/news/releases",
        "Broadcom": "https://www.broadcom.com/company/newsroom/press-releases",
        "Pfizer": "https://www.pfizer.com/news/press-release",
        "GSK": "https://www.gsk.com/en-gb/media/press-releases/",
        "JPMorgan": "https://www.jpmorganchase.com/news-stories",
        "Goldman Sachs": "https://www.goldmansachs.com/media-relations/press-releases/current/",
        "Bank of America": "https://newsroom.bankofamerica.com/"
    }
    url = url_map.get(company)
    if not url:
        return "#"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find first link mentioning "AI" or "claims"
        link = soup.find('a', href=True, string=lambda text: text and ('ai' in text.lower() or 'claims' in text.lower()))
        if link:
            return link['href'] if link['href'].startswith('http') else url + link['href']
    except Exception:
        return "#"

    return "#"

def update_csv():
    with open('risk_data.csv', 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    headers = rows[0]
    try:
        url_index = headers.index('Announcement URL')
    except ValueError:
        print("No 'Announcement URL' column found.")
        return

    updated = False

    for row in rows[1:]:
        if row[url_index] == "#" or row[url_index].strip() == "":
            company = row[0]
            print(f"Scraping {company}...")
            new_url = scrape_url(company)
            if new_url != "#":
                print(f"Found: {new_url}")
                row[url_index] = new_url
                updated = True
            else:
                print(f"No AI/claims news found for {company}")

    if updated:
        with open('risk_data.csv', 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(rows)
        print("CSV updated successfully!")
    else:
        print("No updates found.")

if __name__ == "__main__":
    update_csv()
