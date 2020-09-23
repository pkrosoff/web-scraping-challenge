import pymongo
import mars_scrape
#connect to mongo
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
#declare the database
db = client.mars_db
#declare the collection
mars_site = db.mars_db
#empty database for new scraped data
mars_site.drop()
#populate database with scraped data variable from mars_scrape
mars_site.insert_one(mars_biz)


results = mars_site.find()
for result in results:
    print(result)