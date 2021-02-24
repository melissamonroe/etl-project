# MAIN SCRIPT TO RUN THE ETL FOR THE CRAIGSLIST PROPERTY RENTALsimport config
import config
import cl_parser

print('#' * 40)
print('Running Craigslist appartment ETL')
print('#' * 40)

# Create the craiglist parser
my_parser = cl_parser.Parser() 

# URLs to scrape
urls = []
urls.append(config.url_listings_northsd)
urls.append(config.url_listings_eastsd)
urls.append(config.url_lisings_cityofsd)
urls.append(config.url_lisings_southsd)

# Scrape the pages, clean, and load data in to database
my_parser.scrape_cl(urls)
my_parser.update_details()
