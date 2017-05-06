import json
from urllib2 import urlopen
from requests.exceptions import HTTPError
import urllib2
from bs4 import BeautifulSoup

url = 'https://ocw.mit.edu/courses/'
urls = []
response = urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
courseList = soup.findAll("table", {'class':'courseList'})
seen = {}
for item in courseList:
            links = item.findAll('a')
            for link in links:
            	l = 'https://ocw.mit.edu' + link.attrs['href']
            	if l not in seen:
            		seen[l] = 1
            		urls = urls + [l]
print len(urls)
#thefile = open('mit.txt', 'w')
#for item in urls:
#    thefile.write("%s\n" % item)