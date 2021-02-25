# Dependencies
import pymongo
import dns
import datetime
from time import sleep
import random
import json
import pandas as pd
import numpy as np

import config

class Visualizer:
        
    # init method or constructor
    def __init__(self):
        self.name = config.pg_username
        self.listings_collection = None

        conn = config.mongo_conn
        client = pymongo.MongoClient(conn)

        client.server_info() # Will throw an exception if DB is not connected. @TODO Add better handling of this

        # Define database and collection
        db = client[config.db_name]
        self.listings_collection = db.listings

    def get_raw_data(self):

        # This is only pulling certain fields that are going to be used
        cursor = self.listings_collection.find({},{ 'data_id': 1, 
                            'listing_title': 1, 
                            'listing_bedbath': 1,
                            'listing_bed': 1,
                            'listing_bath': 1,
                            'listing_price': 1, 
                            'listing_addrzip': 1,
                            'listing_addrlocality': 1,
                            'listing_latitude': 1, 
                            'listing_longitude': 1, 
                            'listing_sqft': 1, 
                            '_id': 0 })   

        # Create the Dataframe                    
        df = pd.DataFrame(list(cursor))

        return df

    def get_clean_data(self):

        # Get the raw data from database
        df = self.get_raw_data()

        ##################################
        #           CLEAN DATA           #
        ##################################

        # Drop any rows that have NaN fields
        df.dropna(how ='any', inplace=True) 

        # Remove outliers for sqft
        for data_id in df.loc[df['listing_sqft'] == '']['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True) 

        for data_id in df.loc[df['listing_sqft'] < config.low_sqft]['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True) 

        for data_id in df.loc[df['listing_sqft'] > config.high_sqft]['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True) 

        # Remove any rows that contain no zip code
        for data_id in df.loc[df['listing_addrzip'] == '']['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True)
            
        # Remove outliers for listing price
        for data_id in df.loc[df['listing_price'] == 0]['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True)

        for data_id in df.loc[df['listing_price'] < config.low_price]['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True)

        for data_id in df.loc[df['listing_price'] > config.high_price]['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True)

        # Drop any duplicates
        df.drop_duplicates(subset=[ 'listing_title',
                                    'listing_bedbath',
                                    'listing_price',
                                    'listing_addrzip',
                                    'listing_sqft'], 
                                    inplace=True,
                                    keep='last')
        
        ##################################
        #         END CLEAN DATA         #
        ##################################

        return df

        
""" 
visuals = Visualizer()
base_df = visuals.get_clean_data()
#print(base_df.head(5))

base_df = base_df.sort_values(by=['listing_price'], ascending=True).head(5)
print(base_df.head(5)) """