#!/usr/local/bin/python2.7
# -*- coding: UTF-8 -*-

import cgi, cgitb
import sys, os, lucene 
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer 
from org.apache.lucene.analysis.standard import StandardAnalyzer 
from org.apache.lucene.document import Document, Field, FieldType 
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions 
from org.apache.lucene.store import SimpleFSDirectory 
from pymongo import MongoClient


form = cgi.FieldStorage()
words = form.getvalue('input_query')
INDEX_DIR = "./IndexFiles.index"
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
storeDir = './IndexFiles.index'
analyzer = StandardAnalyzer()
if not os.path.exists(storeDir): 
	os.mkdir(storeDir) 
	store = SimpleFSDirectory(Paths.get(storeDir)) 
	analyzer = LimitTokenCountAnalyzer(analyzer, 1000) 
	config = IndexWriterConfig(analyzer) 
	config.setOpenMode(IndexWriterConfig.OpenMode.CREATE) 
	writer = IndexWriter(store, config) 
	t1 = FieldType()  
	t1.setStored(True) 
	t1.setTokenized(False)
	t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)  
	t2 = FieldType() 
	t2.setStored(True) 
	t2.setTokenized(True)
	t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)         
	connection = MongoClient("yourmongodb")
	db = connection['web-search-engine']
	collection = db.courses
	res = collection.find()
	for record in res:
    		name = record['name']
    		url = record['url']
    		contents = record['contents']
    		doc = Document() 
    		doc.add(Field('name', name, t1))
    		doc.add(Field('url', url, t1)) 
    		doc.add(Field('contents', contents, t2)) 
    		writer.addDocument(doc)
	writer.commit() 
	writer.close()

directory = SimpleFSDirectory(Paths.get(INDEX_DIR))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer()
query = QueryParser("contents", analyzer).parse(words)
scoreDocs = searcher.search(query, 50).scoreDocs
i = 1
seen = {}
for scoreDoc in scoreDocs:
	if i > 10:
		break
	doc = searcher.doc(scoreDoc.doc)
	name = doc.get("name")
	url = doc.get("url")
	if url not in seen.keys():
		i += 1
		seen[url] = name
	else: 
		continue

print "Content-type:text/html"
print
print "<html>"
print "<head>"
print "<meta charset=\"utf-8\">"
print "<title>query results</title>"
print "</head>"
print "<body>"
print "<h2>%s</h2>" % (words)
print "Search results:"
if any(seen):
	for key in seen.keys():
		print "<li><a href= %s>%s</a>" % (key, seen[key])
else:
	print "Sorry! We do not find courses that match your query"
	
print "</body>"
print "</html>"