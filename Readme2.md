#Background/Goal
Search sandiego.craigslist.org for apartment listings.  Craigslist San Diego allows you to search the entire county, or break it up into 4 different geographical areas.  They are:

- **Entire County** https://sandiego.craigslist.org/search/apa?housing_type=1
- **North County**	https://sandiego.craigslist.org/search/nsd/apa?housing_type=1
- **East County**		https://sandiego.craigslist.org/search/esd/apa?housing_type=1
- **South County**	https://sandiego.craigslist.org/search/ssd/apa?housing_type=1
- **City of San Diego**  https://sandiego.craigslist.org/search/csd/apa?housing_type=1

`housing_type=1` filters out non-apartment listings

#Process

We used MongoDB and Python.  We chose Mongo because we were unsure how structured CL postings were.  It turns out SQL would have worked, because when you create a CL ad, many of the fields are constrained by pop-ups.  
![CL Posting](resources/images/cl_create_posting.png)

`cl_parsery.py` is used to set up the database and holds all the functions used to scrape the site, clean up the data, and insert results into the database.

Listings were not added to the database if they did not include all of the following:

- Listing Title
- Listing Price
- Listing datetime
- Listing Creation datetime
- Data ID (the number at the end of the Listing URL)

If a listing had all of the above items, we then extracted the following items

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

