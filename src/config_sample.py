# IF USING ATLAS (CLOUD) THE CONNECTION STRING IS AS FOLLOWS
# THIS CAN BE FOUND WHEN YOU LOGIN TO YOUR ATLAS ACCOUNT
mongo_conn="mongodb+srv://<YOUR MONGO DB USERNAME>:<YOUR MONGO DB PASSWORD>@<YOUR CONNECTION STRING>"
# IF USING LOCAL HOST THE CONNECTION STRING WILL BE AS FOLLOWS
# mongo_conn="mongodb://localhost:27017/<DATABASE_NAME>"
pg_username="<YOUR MONGO DB USERNAME>"
pg_password="<YOUR MONGO DB PASSWORD>"

# debug true will print extra output
debug=True

# For future development to allow for using local data files to test 
# before scraping website.
test=True

url="https://sandiego.craigslist.org/d/apartments-housing-for-rent/search/apa"

url_listings_northsd = "https://sandiego.craigslist.org/search/nsd/apa"
url_listings_eastsd = "https://sandiego.craigslist.org/search/esd/apa"
url_lisings_cityofsd = "https://sandiego.craigslist.org/search/csd/apa"
url_lisings_southsd = "https://sandiego.craigslist.org/search/ssd/apa"