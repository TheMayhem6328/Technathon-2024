from requests import get, ConnectionError, ConnectTimeout
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from os import chdir, mkdir
from os.path import exists, dirname
from urllib.parse import unquote

# Change path to script directory
chdir(dirname(__file__))

"""# Retrieve CSV with country codes and their names
try:
    with open("res\\country_codes.csv", encoding="utf-8") as file:
        countries = file.read()
except FileNotFoundError:
    print("WARN: Downloading prerequisites")

    # Retrieve file
    try:
        countries = get(
            "https://raw.githubusercontent.com/datasets/country-codes/master/data/country-codes.csv"
        )
        countries = countries.text
    except (ConnectionError, ConnectTimeout):
        print("ERROR: Unable to retrieve 'country-codes.csv'. Exiting...")
        exit()

    # Save to file
    try:
        # Here, we check whether the file can be opened or not,
        # then immediately close it if it exists
        open("res\\country_codes.csv").close()
    except FileNotFoundError:
        # Check whether the directory `res` exists
        # If not, just make one of the same name
        try:
            exists("res")
        except FileNotFoundError:
            mkdir("res")
    finally:
        with open("res\\country_codes.csv", "+wt", encoding="utf-8") as file:
            file.write(countries)"""

# Initialize a tuple of country codes and their names
countries = {
    ("US", "US"),
    ("CA", "Canada"),
    ("AU", "Australia"),
    ("GB", "UK"),
    ("NZ", "New Zealand"),
    ("AR", "Argentina"),
    ("AT", "Austria"),
    ("BE", "Belgium"),
    ("BR", "Brazil"),
    ("BG", "Bulgaria"),
    ("CL", "Chile"),
    ("HK", "Hong Kong"),
}

# Since we don't have a dictionary API at hand,
# let's retrieve trending search queries from Google
# then extract keywords from them queries

# Initialize `pytrends` object to retrieve Google Trends data
pytrends = TrendReq(hl="en-US", tz=360)

# Retrieve top searches
data = []
for iso, cldr in countries:
    print("Retrieving searches for", cldr)
    try:
        data += list(pytrends.today_searches(iso))
    except ResponseError:
        ...

# Cleanup data elements
# This is to extract just the query out of the whole URI
data = [
    unquote(str(uri).strip("/trends/explore?q=").split("&")[0]) for uri in data
]

# Extract keywords
keywords = set()
for query in data:
    for word in query.split('+'):
        if len(word) > 2:
            keywords.add(word)

print(keywords)