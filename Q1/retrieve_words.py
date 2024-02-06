from requests import get
from requests.exceptions import ConnectionError, ConnectTimeout, SSLError
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from os import chdir, mkdir
from os.path import exists, dirname
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor

# Change path to script directory
chdir(dirname(__file__))

# Since we don't have a dictionary API at hand,
# let's retrieve trending search queries from Google
# then extract keywords from them queries


# Function to retrieve top searches of a particular region
def retrieve_search(country: tuple[str, str], verbose: bool = False) -> list[str]:
    """Retrieve trending search URIs for a particular region

    Args:
        `country` (`tuple[str,str]`):
            A tuple containing the region's
            ISO 3166-2 code and CLDR name

    Returns:
        `list[str]`:
            Contains a list of trending search URIs
    """

    # Notify user of country to be searched
    if verbose:
        print(f"Retrieving searches for {country[1]}\n", end="")

    # Initialize `pytrends` object to retrieve Google Trends data
    try:
        pytrends: TrendReq = TrendReq(hl="en-US", tz=360)
    except (ConnectionError, ConnectTimeout, SSLError):
        if verbose:
            print("ERROR: Unable to retrieve Google Trends data")
        return []

    # Retrieve URIs for today's trending search queries
    try:
        return list(pytrends.today_searches(country[0]))
    except ResponseError:
        return []


def search_to_keyword(*args: tuple[str, str]) -> set[str]:
    """Retrieves a set of keywords from trending searches given regions

    Args:
        `*args` (*args: tuple[str, str]):
            An arbitrary amount of tuples containing a region's
            ISO 3166-2 codes and their CLDR names
    Returns:
        `set[str]`: Contains extracted keywords
    """

    # Concurrently lookup
    thread_results = []
    with ThreadPoolExecutor(15) as thread:
        thread_results = thread.map(retrieve_search, args)

    # Unload the thread results to a singular list of URIs
    data: list[str] = []
    for result in thread_results:
        data += list(result)

    # Cleanup data elements
    # This is to extract just the query out of the whole URI
    data = [unquote(str(uri).strip("/trends/explore?q=").split("&")[0]) for uri in data]

    # Extract keywords
    keywords: set[str] = set()
    for query in data:
        for word in query.split("+"):
            if len(word) > 2:
                keywords.add(word)

    return keywords


kw = search_to_keyword(
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
)

print(kw)


def ensured_file(url: str, verbose: bool = False) -> bool:
    # Extract filename from URL
    name = url.split("/")[-1]

    # Try to open file, or download if file does not exist
    if exists("res\\" + name):
        return True
    else:
        # Notify user that we're downloading a file
        if verbose:
            print("WARN: Downloading file " + name)

        # Retrieve file
        try:
            contents: str = get(url).text
        except (ConnectionError, ConnectTimeout, SSLError):
            print("ERROR: Unable to retrieve " + name)
            return False

        # Save to file
        if not exists("res\\" + name):
            if not exists("res"):
                mkdir("res")
        with open("res\\" + name, "+wt", encoding="utf-8") as file:
            file.write(contents)
            return True


print(
    ensured_file(
        "https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/english.txt"
    )
)
