# Dependencies
import pymongo
import dns
import datetime
from time import sleep
import random
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import config

# @TODO Break the Visualizer class into separate classes. One that only handles the data
# and a second that only builds the plots or graphs.
class Visualizer:
        
    # init method or constructor
    def __init__(self):
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

        # Drop any duplicates. Dups can happen when a listing is duplicated by the user
        # in order to get their listing on the first page. They will have the same data 
        # except for the data_id 
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

    def create_visuals(self):
        # Generate the visualizations useful for the project
        self.create_top20()
        # @TODO Add additional visual creation

    def get_summary_stats(self):
        grouped_zip_df = self.get_raw_data().groupby(["listing_addrzip"])
        # mean, median, variance, standard deviation, and SEM of the listing_price 
        mean_listing_price = grouped_zip_df["listing_price"].mean()
        zip_count = grouped_zip_df["listing_addrzip"].count()

        # Assemble the resulting series into a single summary dataframe.
        summary_stats_df = pd.DataFrame(
            {"Average List Price": mean_listing_price,
            "Listing Count": zip_count,
            "Location": grouped_zip_df["listing_addrlocality"].unique(),
            "Zip Code": grouped_zip_df["listing_addrzip"].unique(),
            "Location (Zip)": grouped_zip_df["listing_addrlocality"].unique() + " " + grouped_zip_df["listing_addrzip"].unique()
            })
        return summary_stats_df

    def create_top20(self):
        summary_stats_df = self.get_summary_stats()
        summary_stats_highpricezips_df = summary_stats_df.sort_values(by=['Average List Price'], ascending=False).head(20)

        mean_highprices = []
        locations_highprices = []
        zipcodes_highprices = []

        for m in summary_stats_highpricezips_df['Average List Price']:
            mean_highprices.append(m)
        for l in summary_stats_highpricezips_df['Location (Zip)']:
            locations_highprices.append(l)        
        for z in summary_stats_highpricezips_df['Zip Code']:
            zipcodes_highprices.append(z)  
        
        x_axis = np.arange(0, len(locations_highprices))
        tick_locations = []
        for x in x_axis:
            tick_locations.append(x)
            
        fig, ax = plt.subplots(figsize=(12,8)) # set the size that you'd like 
        fig.subplots_adjust(bottom=0.4)
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                    ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(14)
        fig.suptitle('Top 20 Highest Average Rental Listing Price', fontsize=20)

        plt.xlabel("Zip Code")
        plt.ylabel("Average Rental Listing Price ($)")

        plt.xlim(-0.75, len(locations_highprices)-.25)
        plt.ylim(0, max(mean_highprices) + 1000)

        plt.bar(x_axis,mean_highprices, facecolor="#097392", alpha=0.75, align="center")
        plt.xticks(tick_locations, locations_highprices, rotation=90)
        # @TODO Move the file name out. Is depemdent on where it is run from. 
        plt.savefig("../images/fig01_top20averageprice.png")
        
