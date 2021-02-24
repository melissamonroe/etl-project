from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

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

# Scrape the pages
my_parser.scrape_cl(urls)


