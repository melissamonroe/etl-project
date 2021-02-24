#Background/Goal
Search sandiego.craigslist.org for apartment listings.  Craigslist San Diego allows you to search the entire county, or break it up into 4 different geographical areas.  They are:

- **Entire County** https://sandiego.craigslist.org/search/apa?housing_type=1
- **North County**	https://sandiego.craigslist.org/search/nsd/apa?housing_type=1
- **East County**		https://sandiego.craigslist.org/search/esd/apa?housing_type=1
- **South County**	https://sandiego.craigslist.org/search/ssd/apa?housing_type=1
- **City of San Diego**  https://sandiego.craigslist.org/search/csd/apa?housing_type=1

`housing_type=1` filters out non-apartment listings

#Process

We used MongoDB and Python.  We chose Mongo because we were unsure how structured CL postings were, however, it turns out SQL would have worked, because when you create a CL ad, many of the fields are constrained by pop-ups.  
![CL Posting](resources/images/cl_create_posting.png)

`cl_parsery.py` is used to set up the database and holds all the functions used to scrape the site, clean up the data, and insert results into the database.

Listings were not added to the database if they did not include all of the following:

- Listing Title
- Listing Price
- Listing datetime
- Listing Creation datetime
- Data ID (the number at the end of the Listing URL)

When run this morning (2/24) it took 73 minutes and we went from 7608 to 8635 valid records.

If a listing had all of the above items, we then extracted the detail items:

- listing_latitude
- listing_longitude    
- listing_bedbath
- listing_sqft
- listing_availability
- listing_attributes
- listing_addrcountry
- listing_addrlocality
- listing_addrregion
- listing_addrzip
- listing_addrstreet
- listing_type
- listing_bed
- listing_bath
- listing_petsallowed
- listing_smokingallowed

We cleaned up the data before inserting it in Mongo - removing the $ and thousands separator from the price and "ft2" so that those results could be used as numbers instead of strings. We also made assumptions regarding bed/bathrooms if no number was provided.  A blank bedroom = studio apartment, blank bathroom = 1/2 bath

##Results
At the time of writing this report, the most popular types of apartments were (unsurprisingly) 1br/1ba and 2br/2ba with 3437 and 1951 units respectively. 

| Bed/Bath | Count|
| :--- | ---:|
| 1BR / 1Ba | 3437 |
| 2BR / 2Ba | 1951 |
| 2BR / 1Ba | 965 |
| 0BR / 1Ba | 589 |
| 3BR / 2Ba | 415 |
| 2BR / 1.5Ba | 117 |
| 2BR / 2.5Ba | 91 |

###Average Rental Price by Zip Code

![AVG Rental by Zip](resources/images/Average_rentalprice_all _zip.png)

92091 is Rancho Santa Fe, and at that price and location is more than likely to be a house miscategorized as an apartment.

92155 is Coronado.

67340 is in rural southern Kansas, and must be a typo.

91987 is in Tecate (Far East San Diego County near the border).

###20 Highest Zip Codes Average Listing Price

![AVG Rental by Zip chart](resources/images/fig01_top20averageprice.png)

###20 Lowest Zip Codes Average Listing Price

![AVG Rental by Zip chart](resources/images/fig02_bottom20averageprice.png)

###Top 10 Zip Code Listing count

![AVG Rental by Zip chart](resources/images/plot_most_listing_by_zip.png)


- Escondido
- UTC
- 3x3 block area of downtown between A and C streets and Front and Third, (SD city offices, Golden Hall etc)
- PO Box zip code in Vista
- PO Box zip code in San Marcos
- San Marcos
- West Chula Vista
- PO Box zip code in Chula Vista
- East Carlsbad/Oceanside
- PO Box zip code in La Mesa
