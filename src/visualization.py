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

        # @TODO Make sure database is connected

        # Define database and collection
        db = client[config.db_name]
        self.listings_collection = db.listings

    def get_raw_data(self):
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
        df = pd.DataFrame(list(cursor))
        return df

    def get_clean_data(self):
        df = self.get_raw_data()
        df.dropna(how ='any', inplace=True) 

        # Remove any rows that contain no sqft
        for data_id in df.loc[df['listing_sqft'] == '']['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True) 

        # Remove any rows that contain no zip code
        for data_id in df.loc[df['listing_addrzip'] == '']['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True)
            
        # Remove any rows that contain no listing price
        for data_id in df.loc[df['listing_price'] == 0]['data_id']:
            df.drop(df.index[df['data_id'] == data_id], inplace = True)
        
        return df

