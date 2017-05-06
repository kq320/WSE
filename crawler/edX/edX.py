import json
from urllib2 import urlopen
from pymongo import MongoClient

pre_url = 'https://www.edx.org/api/v1/catalog/search?page=1&page_size=1440&partner=edx'
post_url = '&content_type[]=courserun&content_type[]=program&featured_course_ids=course-v1%3AUQx+IELTSx+3T2016%2Ccourse-v1%3AMicrosoft+DAT101x+2T2017%2Ccourse-v1%3AGTx+CS1301x+1T2017%2Ccourse-v1%3ABUx+QD501x+2T2017%2Ccourse-v1%3AUSMx+CC605x+2T2017%2Ccourse-v1%3AColumbiaX+BAMM.101x+2T2017&featured_programs_uuids=8ac6657e-a06a-4a47-aba7-5c86b5811fa1%2Ca015ce08-a727-46c8-92d1-679b23338bc1%2C25fbab7b-2dff-4d83-a2d1-bf9a56a5d7a6%2Ca78e76d2-7e0b-4865-8013-0e037ebdc0f9%2C482dee71-e4b9-4b42-a47b-3e16bb69e8f2%2Cee57513c-8aee-48c8-bd0e-091a7bc3f5d2'
url = pre_url + post_url

j = urlopen(url)
data = json.load(j)
size = len(data['objects']['results'])
connection = MongoClient("yourmongodbconnectionstring")
db = connection['web-search-engine'].courses
for i in range(0, size):
    contents = ""
    name = data['objects']['results'][i]['title']
    contents = contents + name + " "
    if 'short_description' in data['objects']['results'][i].keys():
        content = data['objects']['results'][i]['short_description']
        if content is None:
            continue
        print i
        contents = contents + content
    link = data['objects']['results'][i]['marketing_url']
    course = {"name": name,
                "url": link,
                "contents": contents}
    post_id = db.insert_one(course).inserted_id