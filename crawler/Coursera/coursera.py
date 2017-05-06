from urllib2 import urlopen
from bs4 import BeautifulSoup
import urlparse
import robotparser
import HTMLParse 
import lucene 
from pymongo import MongoClient
def BuildSearchEngine(start, number, domain):
	user_agent='wswp'  
	pagesToVisit = [start]
	numberVisited = 0
	rp = get_robots(domain)
	seen = {start: 0}
	while numberVisited < number and pagesToVisit != []:
		url = pagesToVisit[0]
		pagesToVisit = pagesToVisit[1:]
		if rp.can_fetch(user_agent, url):
			numberVisited = numberVisited +1
			print(numberVisited, "Visiting:", url)
			html = download(url)
			parser = HTMLParse.HtmlParser()
			links = parser.parse(html, url)
			for link in links:
				link = normalize(domain, link) 
				if link not in seen:
					seen[link] = numberVisited
					if same_domain(domain, link):
						pagesToVisit = pagesToVisit + [link]
	

def normalize(seed_url, link):
	"""Normalize this URL by removing hash and adding domain
	"""
	link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
	return urlparse.urljoin(seed_url, link)

def download(url):
	response = urlopen(url)
	html = response.read()
	return html

def get_robots(url):
	"""Initialize robots parser for this domain
	"""
	rp = robotparser.RobotFileParser()
	rp.set_url(urlparse.urljoin(url, '/robots.txt'))
	rp.read()
	return rp
def same_domain(url1, url2):
	"""Return True if both URL's belong to same domain
	"""
	return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc

if __name__ == '__main__':
	start = 'https://www.coursera.org'
	number = 1000
	domain = 'https://www.coursera.org'
	BuildSearchEngine(start, number, domain)