import requests
from requests.adapters import Retry, HTTPAdapter
import re

NSFW_BLOCK_LIST = NSFW_KEYWORDS = [
    "hentai", "eroge", "nsfw", "xxx", "18+", "lewd", "porn", "sex", "sexual", "uncensored",
    "ecchi", "oppai", "lust", "futanari", "loli", "shota", "yuri", "yaoi", "otome", "nukige",
    "nude", "naked", "boobs", "breasts", "genitals", "vagina", "penis", "cum", "orgasm", "hardcore",
    "incest", "milf", "tentacle", "bdsm", "rape", "bestiality", "pegging", "impregnation", "hypnosis",
    "dlsite", "nutaku", "f95zone", "erogamescape", "hgames", "anime-sharing",
    "visual novel with adult content", "mature content", "contains sexual content",
]

class FitGirl:
    """
    A unofficial Api for **fitgirl repack**
    """
    BASE_URL: str = "https://fitgirl-repacks.site/"
    def __init__(
        self,
        retry: int = 2,
        status_forcelist: list[int] = None,
        backoff_factor: float = 2.4,
        backoff_max: int = 5,
    ):
        self.retry = Retry(
            retry,
            status_forcelist=status_forcelist or [502, 503, 504],
            backoff_factor=backoff_factor,
            backoff_max=backoff_max,
        )
        self.client = requests.Session()
        self.client.mount("https://", HTTPAdapter(max_retries=self.retry))
        self.client.mount("http://", HTTPAdapter(max_retries=self.retry))

    def new_posts(self):
        try:
            response = self.client.get(self.BASE_URL)

            results = re.findall(
                r'<h1 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h1>',
                response.text,
            )
            results = [i for i in results if "Upcoming Repacks" not in i]
            json_results = {"status": "Success", "results": []}

            for result in results:
                json_results["results"].append({"url": result[0], "title": result[1]})

            return json_results

        except (requests.RequestException, IndexError) as e:
            return {"status": "Error", "message": str(e)}

    @staticmethod
    def filter_query(query: str) -> bool:
        for i in NSFW_BLOCK_LIST:
            if i in query:
                return False
        return True
        
    def search(self, query: str):
        if not self.filter_query(query):
            return {"status": "Error", "message": "Nsfw query detected"}
        try:
            response = self.client.get(f"{self.BASE_URL}?s={query}")

            if (
                "Sorry, but nothing matched your search terms. Please try again with some different keywords."
                in response.text
            ):
                return {"status": "Error", "message": "No results found."}

            results = re.findall(
                r'<h1 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h1>',
                response.text,
            )
            json_results = {"status": "Success", "results": []}

            for result in results:
                if not self.filter_query(result[1]):
                    json_results["results"].append({"url": "******", "title": "NSFW GAME"})
                    continue
                json_results["results"].append({"url": result[0], "title": result[1]})

            return json_results

        except (requests.RequestException, IndexError) as e:
            return {"status": "Error", "message": str(e)}

    def download(self, query: str):
        if not self.filter_query(query):
            return {"status": "Error", "message": "Nsfw query detected"}
        try:
            response = self.client.get(f"{self.BASE_URL}?s={query}")

            if (
                "Sorry, but nothing matched your search terms. Please try again with some different keywords."
                in response.text
            ):
                return {"status": "Error", "message": "No results found."}

            results = re.findall(
                r'<h1 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h1>',
                response.text,
            )
            first_one = results[0][0]
            response = self.client.get(first_one)

            results = re.findall(
                r"<h3>Download Mirrors</h3>(.+?)</ul>", response.text, re.DOTALL
            )
            if not results:
                return {"status": "Error", "message": "No download mirrors found."}

            results = re.findall(
                r'<li><a href="(.+?)" target="_blank" rel="noopener">(.+?)</a>',
                results[0],
            )

            json_results = {"status": "Success", "results": []}
            for result in results:
                if not self.filter_query(result[1]):
                    json_results["results"].append({"url": "******", "title": "NSFW GAME"})
                    continue
                json_results["results"].append({"url": result[0], "title": result[1]})

            return json_results

        except (requests.RequestException, IndexError) as e:
            return {"status": "Error", "message": str(e)}
