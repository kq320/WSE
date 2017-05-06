from urllib2 import urlopen
from bs4 import BeautifulSoup
import urlparse
import robotparser
from pymongo import MongoClient

def BuildSearchEngine(domain):
	f = open('courses.txt', 'r')
	pagesToVisit = f.readlines()
	while pagesToVisit != []:
		url = pagesToVisit[0]
		pagesToVisit = pagesToVisit[1:]
		html = download(url)
		parse(html, url)

def download(url):
	response = urlopen(url)
	html = response.read()
	return html

def parse(html_cont, url):
		if html_cont is None:
			return
		connection = MongoClient("yourmongodbconnectionstring")
		db = connection['web-search-engine'].courses
		soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
		contents = ''
		name = soup.title.string
		print name
		contents = contents + name + " "
		des = soup.findAll("p")
		des2 = soup.findAll('li')
		for item in des:
			contents = contents + item.text + " "
		for item in des2:
			contents = contents + item.text + " "
		#print contents
		course = {"name": name,
				"url": url,
				"contents": contents}
		post_id = db.insert_one(course).inserted_id

if __name__ == '__main__':
	domain = 'https://www.coursera.org'
	BuildSearchEngine(domain)