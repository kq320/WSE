from bs4 import BeautifulSoup
import urlparse
import re
from pymongo import MongoClient

class HtmlParser(object):

	def get_links(self, soup):
		new_urls = []
		tmp_links = soup.findAll("div", { "class" : "view-button" })
		for item in tmp_links:
			link = item.find('span').attrs['href']
			if 'specializations' in link:
				continue
			new_urls = new_urls + [link]
		return new_urls

	def parse(self, html_cont, url):
		if html_cont is None:
			return
		connection = MongoClient("yourmongodbconnectionstring")
		db = connection['web-search-engine'].courses
		soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
		new_urls = self.get_links(soup)
		contents = ''
		name = soup.title.string
		contents = contents + name + " "
		about_course = ''
		des = soup.findAll("p", {"class":"body-1-text course-description"})
		for item in des:
			contents = contents + item.text + " "
		modules = soup.findAll("div", {"class": "module-name headline-2-text"})
		for item in modules:
			contents = contents + item.text + " "
		self.storeDB(url, name, contents)
		course = {"name": name,
				"url": url,
				"contents": contents}
		post_id = db.insert_one(course).inserted_id
		return new_urls

	def storeDB(self, url, name, contents):
		print url
		


