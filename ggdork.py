import urllib3
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time

urllib3.disable_warnings()

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
#USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12"

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
}

DEBUG = True

def google_search(query=None, num=10, start=0, proxies=None):
    if query == None:
        return 1

    query = urllib.parse.quote(query)
    headers = {'User-Agent': USER_AGENT}

    if start == 0:
        url = f'https://www.google.com/search?q={query}&num={num}&hl=en'
    else:
        url = f'https://www.google.com/search?q={query}&num={num}&start={start}&hl=en'

    if DEBUG:
        print(f'GET: {url}')

    if proxies:
        resp = requests.get(url, headers=headers, proxies=proxies, verify=False)
    else:
        resp = requests.get(url, headers=headers)
    results = []
    max_nav = 0
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, 'html.parser')
        for g in soup.find_all('div', attrs={'class':'r'}):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                        'title': title,
                        'link': link
                }
                results.append(item)
        # Get number page navigation
        page_nav = soup.find('div', attrs={'id':'foot'})
        nav = page_nav.find_all('td')
        len_nav = len(nav)
        if 'Next' in nav[len_nav-1].a.text:
            max_nav = nav[len_nav-2].a.text
        else:
            max_nav = nav[len_nav-1].a.text
    else:
        print(f'Error: {resp.status_code}')

    return results, max_nav

def search(query=None, num=10, start=0, stop=None, pause=0.0, proxies=None):
    if stop == None:
        results = []
        nav = 1
        result, max_nav = google_search(query, num=num, start=start, proxies=proxies)
        results.extend(result)
        while nav != max_nav:
            if max_nav != 0:
                nav += 1
                start = (nav-1)*num
            result, max_niav = google_search(query, num=num, start=start, proxies=proxies)
            if result:
                results.extend(result)
            time.sleep(pause)
        
        return results

def main():
    query = "site:*.backblaze.com filetype:pdf"
    results = search(query, pause=2.0, proxies=proxies)
    for result in results:
        print(result['linnk'])

if __name__ == '__main__':
    main()
