import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

entry_links = []

def clawl_entry_links(url):
    soup = BeautifulSoup(url, 'html.parser')
    entry_link_tags = soup.find_all('a','entry-title-link')

    for entry_link_tag in entry_link_tags:
        entry_links.append(entry_link_tag.get('href'))

    try:
        next_page = soup.find('a',{"rel":'next'}).get('href')
        next_page_url = urlopen(next_page)
        clawl_entry_links(next_page_url)
    except Exception as e:
        print(e)
        return entry_links

    return entry_links

def get_entry_oembed(entry_url):
    oembed_endpoint = 'http://hatenablog.com/oembed'
    params = {
        'url': entry_url,
        'format': 'json',
    }
    request = urllib.request.Request('{}?{}'.format(oembed_endpoint, urllib.parse.urlencode(params)))
    with urllib.request.urlopen(request) as res:
        body = res.read()
        data = json.loads(body)
        print(data)
    return

if __name__ == "__main__":
    blog_url = urlopen(input('input your hatenablog\'s uri >'))
    results = clawl_entry_links(blog_url)
    for entry_url in results:
        get_entry_oembed(entry_url)
