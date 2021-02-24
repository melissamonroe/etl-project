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

        # Define database and collection
        db = client.craigslist_db
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
        listing_price = result.a.span.text
        listing_url = result.a['href']
        listing_datetime = result.time['datetime']
        created_datetime = datetime.datetime.utcnow()
        modified_datetime = datetime.datetime.utcnow()
            
        # Print results
        #if config.debug:
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
        # Examine the results, then determine element that contains sought info
        # results are returned as an iterable list
        # result_details = cl_result_details.find_all('div', class_='mapAndAttrs')
        
        viewposting = cl_result_details.find_all('div', class_='viewposting')
        listing_latitude = viewposting[0]['data-latitude']
        listing_longitude = viewposting[0]['data-longitude']
        
        # mapaddress = cl_result_details.find_all('div', class_='mapaddress')
        # listing_address = mapaddress[0].text
        
        attrgroups = cl_result_details.find_all('p', class_='attrgroup')
        
        listing_availability = ''
        listing_sqft = ''

        for attrgroup in attrgroups:
            listing_attributes = []
            attrspan = attrgroup.find_all('span')
            for span in attrspan:
                if ((span.text.lower().find('br') != -1) & (span.text.lower().find('ba') != -1)):
                    listing_bedbath = span.text                
                elif span.text.lower().find('ft2') != -1:
                    listing_sqft = span.text
                elif span.text.lower().find('available') != -1:
                    listing_availability = span.text
                else: 
                    listing_attributes.append(span.text)

        listing_type = ''
        listing_bed = ''
        listing_bath = ''
        listing_petsallowed = ''
        listing_smokingallowed = ''

        listing_addrcountry = ''
        listing_addrlocality = ''
        listing_addrregion = ''
        listing_addrregion = ''
        listing_addrzip = ''
        listing_addrstreet = ''
            
        soup_scripts = cl_result_details.find_all('script',id='ld_posting_data')

        # Getting dictionary
        scripts_dict = json.loads(soup_scripts[0].contents[0].strip())

        # Pretty Printing JSON string back
        # print(json.dumps(scripts_dict, indent = 4, sort_keys=True))
            
        if '@type' in scripts_dict:
            listing_type = scripts_dict['@type']
        if 'numberOfBedrooms' in scripts_dict:
            listing_bed = scripts_dict['numberOfBedrooms']
        if 'numberOfBathroomsTotal' in scripts_dict:
            listing_bath = scripts_dict['numberOfBathroomsTotal']
        if 'petsAllowed' in scripts_dict:
            listing_petsallowed = str(scripts_dict['petsAllowed'])
        if 'smokingAllowed' in scripts_dict:
            listing_smokingallowed = str(scripts_dict['smokingAllowed'])
        

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
