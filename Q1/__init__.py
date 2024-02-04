from requests import get, ConnectionError, ConnectTimeout
from pyarrow.csv import read_csv, ParseOptions
# from pytrends.request import TrendReq
from sys import exit
from os import mkdir, chdir
from os.path import dirname, exists

# Change path to script directory
chdir(dirname(__file__))

# Retrieve CSV with country codes and their names
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
            file.write(countries)


# Process it into a `pyarrow.Table` object
countries = read_csv(
    input_file="res\\country_codes.csv",
    parse_options=ParseOptions(invalid_row_handler=lambda _: "skip"),
)

# Select specific fields
# This is to clean up data to make it easier to work with
countries = countries.select(["ISO3166-1-Alpha-3", "CLDR display name"])
countries_count = countries.num_rows

# Export data to `tuple(<ISO3166-1-Alpha-3>, <CLDR display name>)`
# Would've used a tuple comprehension, but that becomes very unreadable
countries = countries.to_pydict()
countries_temp = []
for i in range(countries_count):
    countries_temp.append(
        (countries["ISO3166-1-Alpha-3"][i], countries["CLDR display name"][i])
    )
countries_temp.remove(("", ""))  # Remove blank element
countries = tuple(countries_temp)  # Convert to tuple for faster processing

# TBA
# # Since we don't have a dictionary API at hand,
# # let's retrieve trending search queries from Google
# # then extract keywords from them
# 
# # Init pytrends object
# pytrends = TrendReq(hl='en-US', tz=360)
# 
# # dataframe_list = pytrends.top_charts(2023, hl='en-US', tz=-300, geo='GLOBAL')
