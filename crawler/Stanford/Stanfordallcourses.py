import json
from urllib2 import urlopen
from requests.exceptions import HTTPError
import urllib2
from bs4 import BeautifulSoup

url = 'http://online.stanford.edu/courses/allcourses'
urls = []
response = urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
links = soup.findAll("td", {"class":"views-field views-field-title active"})
for item in links:
            link = item.find('a').attrs['href']
            link = 'http://online.stanford.edu' + link
            urls = urls + [link]
thefile = open('courses.txt', 'w')
for item in urls:
    thefile.write("%s\n" % item)