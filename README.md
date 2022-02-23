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
- [python](https://www.python.org/downloads/) 3.9.10 (or via Homebrew `brew install python`)
- pip 22.0.3 (installed with Python)

To install all python packages you should run the command:
```
pip install -r requirements.txt
```

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

## Unimplemented

### Scraping the first property
- The plan after some research was to attempt to login as a user with the highest security and privacy protections (phone number and other account info) + verified (supplying a photo id). Although it worked for some not others based on what I read.
- Using the official API required a key but the request wasn't guaranteed to be granted.
- Requesting the URL with an authorised header.

### Scraping property amenities
- Using selenium to open/click certain buttons on the page to produce output that could then be stored.

### General changes
- Using the `json` response from the site request as `json` is much easier to manipulate and extract data from.
- Create an interface (Factory) that could be implemented by any site (Airbnb, Booking.com, etc) that needs to be requested from. This would allow for similar methods that need to be managed to be extracted as well as enforce correctness.
- Remove some getters/setters. These are redundant for private variables and defeats encapsulation if:
    - They can be manipulated directly
    - Applied to all private variables
- Implement the Builder pattern for constructing properties (see previous point). Complex objects without allowing external access.
