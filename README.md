# ETL-Project
## UCSD Data Bootcamp ETL Group Project
Ben Galde<br>
Melissa Monroe<br>
Tanlin Hung<br>
Kevin Mickey


## Intent
This group project will use [https://sandiego.craigslist.org/search/apa?housing_type=1] (https://sandiego.craigslist.org/search/apa?housing_type=1) to scrape apartment listings for San Diego to determine:

The average rental price by location (TBD whether zip code or descriptors like "UTC" or "North Park")

At a minimum we will match up 1 bed/1 bath with other 1/1's and 2 bed/2 baths with other 2/2's to avoid invalid comparisions.  Other combinations may be included depending on time.

Data will be stored in a MongoDB.

Items we should be able to get from each posting:

- Date datetime
- Post ID
- URL
- Price integer (clean) Price pulled from CL
- Bedrooms
- Baths
- Sqft
- Location (straight from CL)



Things we will also try to determine from the listing:

- Reserved Parking
- Pet Friendly (if possible determine either dog/cat or both)
- Smoking/nonsmoking
- Amenities
- - Washer/Dryer in unit?

## Data Sources
### Scraping Craigslist appartment and house rental pages
The pages for the San Diego appartment and house rental from [HERE](https://sandiego.craigslist.org/d/apartments-housing-for-rent/search/apa)
### Zip code data
The primary zip code data is from [HERE](http://federalgovernmentzipcodes.us/) and renamed the file to [zipc_codes.csv](./resources/data/zipcodes.csv). 
The data was loaded into the database as the following objects.
```json
[
	{
		"_id" : ObjectId("5995a09d60e205ec1b1000b8"),
		"Zipcode" : 76934,
		"ZipCodeType" : "STANDARD",
		"City" : "CARLSBAD",
		"State" : "TX",
		"LocationType" : "PRIMARY",
		"Lat" : 31.59,
		"Long" : -100.63,
		"Location" : "NA-US-TX-CARLSBAD",
		"Decommisioned" : "false",
		"TaxReturnsFiled" : 445,
		"EstimatedPopulation" : 818,
		"TotalWages" : 12675963
	}
]
```


## Analysis
- Amenities
- Determine average rental price by location
