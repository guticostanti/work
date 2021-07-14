from bs4 import BeautifulSoup
import concurrent.futures
import requests



prefix = 'https://www.montebravo.com.br/categoria/podcasts/page/'
urls = []
for i in range(1, 20):
    url = prefix + str(i)
    urls.append(url)

links_podcasts = []

def getUrls(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
        webpage = requests.get(url, headers=headers).content

        soup = BeautifulSoup(webpage, 'html.parser')

        first_page_divs = soup.find("div", {"class": "grid-items"})

        first_page_a = first_page_divs.find_all('a')


        count = 0
        for a in first_page_a:
            count += 1
            if count % 2 != 0:
                single_link = a['href']
                links_podcasts.append(single_link)
    except:
        print('')

podcasts = []
def getPodcasts(link):
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    webpage = requests.get(link, headers=headers).content
    soup = BeautifulSoup(webpage, 'html.parser')
    iframe = soup.find("iframe")
    pod = iframe.get('src')
    podcasts.append(pod)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(getUrls, urls)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(getPodcasts, links_podcasts)

print(len(podcasts))