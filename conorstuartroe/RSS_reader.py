import feedparser
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import lxml

def get_feed():
    npr = feedparser.parse('https://www.npr.org/rss/rss.php?id=1001')
    atl = feedparser.parse('https://www.theatlantic.com/feed/all/')
    titles = []
    for i in range(min(len(npr),len(atl))):
        npr_story = npr['items'][i]
        titles.append(('NPR: ' + summary(npr_story['title']),npr_story['link'],summary(npr_story['summary'])))
        atl_story = atl['items'][i]
        titles.append(('The Atlantic: ' + summary(atl_story['title']),atl_story['link'],summary(atl_story['content'][0]['value'])))
    return titles

def first_image(url):
    html = ur.urlopen(url)
    return bs(html).img

def summary(html):
    text = bs(html,'lxml').text
    return text[:300] + '...' if len(text)>300 else text
