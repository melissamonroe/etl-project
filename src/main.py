# MAIN SCRIPT TO RUN THE ETL FOR THE CRAIGSLIST PROPERTY RENTALS
import config
import cl_parser
import visualization
import datetime as dt

start_time = dt.datetime.now()

print('#' * 40)
print('Running Craigslist Rental ETL')
print('#' * 40)

############################
#        EXTRACTION        #
############################

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

############################
#         VISUALS          #
############################

# Create the visualizer
my_visualizer = visualization.Visualizer() 

# Run the visuals
my_visualizer.create_visuals()

# Show the execution time
end_time = dt.datetime.now()
total_execute_time = (end_time-start_time).total_seconds()
print(f'Total time to execute: {total_execute_time} seconds')
