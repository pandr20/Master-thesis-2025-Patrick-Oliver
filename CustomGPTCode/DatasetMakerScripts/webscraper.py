import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

URL = "https://dr.dk"
parsed_url = urlparse(URL)
base_domain = parsed_url.netloc
links_to_scrape = [URL]
links_already_scraped = []
output_file = 'scraped_text.txt'

def find_all_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    text = []
    for paragraph in soup.find_all('p'):
        text.append(paragraph.get_text())
    return text

def find_all_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == base_domain and not href.startswith('mailto:'):
                links.append(full_url)
    return links

while links_to_scrape:
    current_url = links_to_scrape.pop(0)
    print(f"Scraping: {current_url}")
    text = find_all_text(current_url)
    links = find_all_links(current_url)
    for link in links:
        if link not in links_already_scraped:
            links_to_scrape.append(link)
            links_already_scraped.append(link)

    with open(output_file, 'a', encoding='utf-8') as outfile:
        outfile.write('\n'.join(text) + '\n')