# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import dns
import datetime
from time import sleep
import random
import json

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

import config 

class Parser:

    # init method or constructor
    def __init__(self):
        self.name = config.pg_username
        self.listings_collection = None

        conn = config.mongo_conn
        client = pymongo.MongoClient(conn)

        # @TODO Make sure database is connected

        # Define database and collection
        db = client[config.db_name]
        self.listings_collection = db.listings

    def get_listing_details(self,listing_url):
        # URL of page to be scraped
        url = listing_url

        sleep(random.randint(1,3))
        # Retrieve page with the requests module
        response = requests.get(url)
        # Create BeautifulSoup object; parse with 'lxml'
        soup = BeautifulSoup(response.text,'lxml')    
        return soup

    def insert_listing(self,result):

        # Get the data from the results
        data_id = result.h3.a['data-id']
        listing_title = result.find('a', class_='result-title').text
        listing_price = int(result.a.span.text.replace('$', '').replace(',',''))
        listing_url = result.a['href']
        listing_datetime = datetime.datetime.strptime(result.time['datetime'], '%Y-%m-%d %H:%M')
        created_datetime = datetime.datetime.utcnow()
        modified_datetime = datetime.datetime.utcnow()
            
        # Print results
        if config.debug:
            print('-' * 40)
            print('Inserting new listing')
            print(data_id)
            print(listing_title)
            print(listing_price)
            print(listing_url)
            print(listing_datetime)        
            print(created_datetime)

        # Dictionary to be inserted as a MongoDB document
        post = {
            'data_id': data_id,
            'created_datetime': created_datetime,
            'listing_title': listing_title,
            'listing_price': listing_price,
            'listing_url': listing_url,
            'listing_datetime': listing_datetime            
        }

        # Insert only if the data_id does not exist in the database
        # otherwise update the information
        if self.listings_collection.find({'data_id': data_id}).count() == 0:
            print("Insert new listing! ")
            # Run only if all fields are available
            if (listing_title and listing_price and listing_url and listing_datetime and data_id and created_datetime):
                self.listings_collection.insert_one(post)                
        else: 
            print(f"Listing {data_id} already exists, update existing listing!")
            doc = self.listings_collection.find_one_and_update(
                {'data_id' : data_id},
                {'$set':
                    {
                        'modified_datetime': modified_datetime,
                        'listing_title': listing_title,                
                        'listing_price': listing_price,
                        'listing_url': listing_url,
                        'listing_datetime': listing_datetime
                    }
                    
                },upsert=True
            )

            if config.debug:
                print(doc)

    def insert_listing_details(self, cl_result_details,data_id):   
            # Initialize fields. @TODO May want to create a class to hold all the info
            listing_sqft = ''
            listing_attributes = []
            listing_bedbath = ''
            listing_sqft = ''
            listing_availability = ''
            listing_type = ''
            listing_bed = 0                     # Default to a studio if nothing is given
            listing_bath = 0.5                  # Default to a half bath if nothing is given
            listing_petsallowed = False         # Default to False if not given
            listing_smokingallowed = False      # Default to False if not given
            listing_addrcountry = ''
            listing_addrlocality = ''
            listing_addrregion = ''
            listing_addrregion = ''
            listing_addrzip = ''
            listing_addrstreet = ''
            listing_latitude = ''
            listing_longitude = ''    

            # Examine the results, then determine element that contains sought info
            # results are returned as an iterable list                   
            attrgroups = cl_result_details.find_all('p', class_='attrgroup')
            
            # Update fields from attribute group
            for attrgroup in attrgroups:
                listing_attributes = []
                attrspan = attrgroup.find_all('span')
                for span in attrspan:
                    if ((span.text.lower().find('br') != -1) & (span.text.lower().find('ba') != -1)):
                        listing_bedbath = span.text                
                    elif span.text.lower().find('ft2') != -1:
                        listing_sqft = int(span.text.lower().replace('ft2',''))
                    elif span.text.lower().find('available') != -1:
                        listing_availability = span.text
                    else: 
                        listing_attributes.append(span.text)


            soup_scripts = cl_result_details.find_all('script',id='ld_posting_data')
            # Getting dictionary
            scripts_dict = json.loads(soup_scripts[0].contents[0].strip())

            # Pretty Printing JSON string back
            if config.debug:
                print(json.dumps(scripts_dict, indent = 4, sort_keys=True))

            # Update fields from JSON dump    
            if '@type' in scripts_dict:
                listing_type = scripts_dict['@type']
            if 'numberOfBedrooms' in scripts_dict:
                listing_bed = int(scripts_dict['numberOfBedrooms'])
            if 'numberOfBathroomsTotal' in scripts_dict:
                try:
                    listing_bath = float(scripts_dict['numberOfBathroomsTotal'])
                except ValueError:
                    listing_bath = 0.5
            if 'petsAllowed' in scripts_dict:
                listing_petsallowed = bool(scripts_dict['petsAllowed'])
            if 'smokingAllowed' in scripts_dict:
                listing_smokingallowed = bool(scripts_dict['smokingAllowed'])
            if 'latitude' in scripts_dict:
                listing_latitude = float(scripts_dict['latitude'])
            if 'longitude' in scripts_dict:
                listing_longitude = float(scripts_dict['longitude'])
            if 'address' in scripts_dict:
                address_dict = scripts_dict['address']
                if 'addressCountry' in address_dict:
                    listing_addrcountry = address_dict['addressCountry']
                if 'addressLocality' in address_dict:
                    listing_addrlocality = address_dict['addressLocality']
                if 'addressRegion' in address_dict:
                    listing_addrregion = address_dict['addressRegion']
                if 'postalCode' in address_dict:
                    listing_addrzip = address_dict['postalCode']
                if 'streetAddress' in address_dict:
                    listing_addrstreet = address_dict['streetAddress']

            if config.debug:    
                print(data_id)
                print(listing_latitude)
                print(listing_longitude)    
                print(listing_bedbath)
                print(listing_sqft)
                print(listing_availability)
                print(listing_attributes)
                print(listing_addrcountry)
                print(listing_addrlocality)
                print(listing_addrregion)
                print(listing_addrzip)
                print(listing_addrstreet)
                print(listing_type)
                print(listing_bed)
                print(listing_bath)
                print(listing_petsallowed)
                print(listing_smokingallowed)
                print('------------------------------')

            doc = self.listings_collection.find_one_and_update(
                {'data_id' : data_id},
                {'$set':
                    {
                        'listing_latitude': listing_latitude,
                        'listing_longitude': listing_longitude,                
                        'listing_bedbath':listing_bedbath,
                        'listing_sqft':listing_sqft,
                        'listing_availability':listing_availability,
                        'listing_attributes':listing_attributes,
                        'listing_addrcountry':listing_addrcountry,
                        'listing_addrlocality':listing_addrlocality,
                        'listing_addrregion':listing_addrregion,
                        'listing_addrzip':listing_addrzip,
                        'listing_addrstreet':listing_addrstreet,
                        'listing_type':listing_type,
                        'listing_bed':listing_bed,
                        'listing_bath':listing_bath,
                        'listing_petsallowed':listing_petsallowed,
                        'listing_smokingallowed':listing_smokingallowed                
                    }
                    
                },upsert=True
            )
            
            if config.debug:
                print(doc)

    def scrape_cl(self, urls):
        # Create browser
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)

        # Scrape data for every url
        for url in urls:
            browser.visit(url)

            # Iterate through all pages
            for x in range(config.url_page_range):
                # HTML object
                html_listings = browser.html
                # Parse HTML with Beautiful Soup
                soup_listings = BeautifulSoup(html_listings, 'html.parser')
                # Retrieve all elements that contain book information
                soup_listings = BeautifulSoup(html_listings)
                # Return all the list items of the result_row class
                results = soup_listings.find_all('li', class_='result-row')

                # Loop through returned results
                if config.debug:
                    print(f'Scraping page {x}')
                for result in results:
                    try:
                        self.insert_listing(result)                                                                  
                    except Exception as e:
                        print(e)        
                try:
                    browser.links.find_by_partial_text('next').click()          
                except:
                    print("Scraping Complete")
                    break

    def update_details(self):
        # Create browser
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)

        cursor = self.listings_collection.find({'listing_addrzip':{"$exists":False}})
        print(f'{cursor.count()} documents are in the cursor')
        x = cursor.count()
        
        for listing in cursor:
            data_id = listing['data_id']
            url_details = listing['listing_url']
            
            print('Index ' + str(x) + ' Updating listing details data_id ' + data_id)

            if (url_details != ''):
                sleep(random.randint(1,3))
                browser.visit(url_details)
                html_details = browser.html

                soup_details = BeautifulSoup(html_details)
                
                try:
                    self.insert_listing_details(soup_details, data_id)
                except Exception as e:               
                    print(e)  
                                
            x = x - 1
            if x <= 0:            
                print('Scrape Completed')
                break
