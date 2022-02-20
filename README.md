# Airbnb Scraper
Goal: Scrape the Airbnb website for useful information about a property including:
- Property type
- Property name
- Number of bedrooms
- Number of bathrooms
- Property amenities

## Properties in question
- https://www.airbnb.co.uk/rooms/33571268
- https://www.airbnb.co.uk/rooms/33090114
- https://www.airbnb.co.uk/rooms/50633275

## Running the project
### Requirements
- Python 3.9

### Main program
From the project root enter in the terminal:
```
python airbnb_scraper
```
Or from within `airbnb_scraper`:
```
python .
```

This will run the scraper against the 3 properties in question

### Tests
From within the folder `airbnb_scraper` enter in the terminal:
```
python -m unittest
```