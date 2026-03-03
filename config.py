import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self) -> None:

        # Tavily
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        self.TAVILY_SEARCH_MAX_RESULT = 3
        self.TAVILY_CHUNK_SIZE = 4
        self.TAVILY_SEARCH_CONTENT_RELEVANCE_SCORE = 0.6
        self.TAVILY_ASYNC_RATE_LIMIT = 3

        # SerpAPI
        self.SERP_API_URL = "https://www.searchapi.io/api/v1/search"
        self.SERP_API_KEY = os.getenv("SERP_API_KEY")

        # OpenAI
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.LLM_MAX_RETRIES = 2


# initialize config
cfg = Config()
