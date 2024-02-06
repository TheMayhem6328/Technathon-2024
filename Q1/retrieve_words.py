from requests import get
from requests.exceptions import ConnectionError, ConnectTimeout, SSLError
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError
from os import chdir, mkdir, listdir
from os.path import exists, dirname
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
from threading import Lock


class wordlist:
    """This encapsulates every tool necessary for wordlist generation

    Encapsulating it into a Python class makes sense
    because of how many of these elements may be reused
    over and over again on the same dataset
    """

    def __init__(self, urls: set[str] = set()):
        """Initialize a wordlist object with relevant methods.

        Args:
            `urls` (`set[str]`, optional):
                List of URLs of wordlists. Defaults to `set()`.
        """

        self.keywords: set[str] = self.search_to_keyword(
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

        # Construct a list of URLs if it's empty
        if urls == set():
            urls = {
                f"https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/{lang}.txt"
                for lang in {
                    "arabic",
                    "croatian",
                    "czech",
                    "danish",
                    "dutch",
                    "english",
                    "french",
                    "georgian",
                    "german",
                    "hebrew",
                    "italian",
                    "norwegian",
                    "polish",
                    "portuguese",
                    "russian",
                    "serbian",
                    "spanish",
                    "swedish",
                    "turkish",
                    "ukrainian",
                }
            }

        # Concurrently download given URLs
        lock = Lock()
        with ThreadPoolExecutor(10) as tpe:
            for url in urls:
                tpe.submit(self.ensure_file, url, "wordlist", lock)

        # Generate complete wordlist
        for wordlist in {"res\\wordlist\\" + file for file in listdir("res\\wordlist")}:
            with open(wordlist, encoding="utf-8") as file:
                self.keywords.update(set(file.read().split("\n")))

    # Function to retrieve top searches of a particular region
    def retrieve_search(
        self, country: tuple[str, str], verbose: bool = False
    ) -> list[str]:
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

    def search_to_keyword(self, *args: tuple[str, str]) -> set[str]:
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
        with ThreadPoolExecutor(15) as tpe:
            thread_results = tpe.map(self.retrieve_search, args)

        # Unload the thread results to a singular list of URIs
        data: list[str] = []
        for result in thread_results:
            data += list(result)

        # Cleanup data elements
        # This is to extract just the query out of the whole URI
        data = [
            unquote(str(uri).strip("/trends/explore?q=").split("&")[0]) for uri in data
        ]

        # Extract keywords
        keywords: set[str] = set()
        for query in data:
            for word in query.split("+"):
                if len(word) > 2:
                    keywords.add(word)

        return keywords

    def ensure_file(
        self, url: str, dir: str = "", lock: Lock = Lock(), verbose: bool = False
    ) -> bool:
        """Checks whether a given file exists. If it doesn't,
        save it to a `res` folder

        Args:
            `url` (`str`):
                URL of the file to be ensured. Designed with
                `raw.githubusercontent.com` links in mind
            `dir` (`str`):
                Subdirectory to store it in
            `lock` (`Lock`):
                A `threading.Lock` object which can be used
                to ensure thread safety
            `verbose` (`bool`, optional):
                Whether to print out certain content for
                debugging purposes. Defaults to False.

        Returns:
            `bool`:
                Returns whether file presence was
                successfully ensured or not
        """
        # Change path to script directory
        chdir(dirname(__file__))

        # Adjust `dir` parameter if non-empty
        if dir != "":
            dir += "\\"

        # Extract filename from URL
        name = url.split("/")[-1]

        # Try to open file, or download if file does not exist
        if exists("res\\" + dir + name):
            return True
        else:
            # Notify user that we're downloading a file
            if verbose:
                print("WARN: Downloading file " + name + "\n", end="")

            # Retrieve file
            try:
                contents: str = get(url).text
            except (ConnectionError, ConnectTimeout, SSLError):
                if verbose:
                    print("ERROR: Unable to retrieve " + name + "\n", end="")
                return False

            # Make directory if it doesn't exist
            with lock:
                if not exists("res\\" + dir + name):
                    if not exists("res"):
                        mkdir("res")
                    if not exists("res\\" + dir.strip("\\")):
                        mkdir("res\\" + dir.strip("\\"))

            # Save to file
            with open("res\\" + dir + name, "+wt", encoding="utf-8") as file:
                file.write(contents)
                if verbose:
                    print("WARN: Successfully downloaded file " + name + "\n", end="")
                return True

    def __str__(self) -> str:
        return f"wordlist(len={len(self.keywords)})"

    def __len__(self) -> int:
        return len(self.keywords)
