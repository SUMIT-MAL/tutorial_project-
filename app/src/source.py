from app.config import seetings_manager
from apify_client import ApifyClientAsync
from utils import WebsiteSrapperErrorHandeler
from abc import abstractmethod, ABC
from loguru import logger
from pcpartpicker import API


class SracperClient(ABC):
    """
    Abstract base class for scraper clients.
    This class defines the interface for scraper clients and enforces the implementation of the search_for_parts method.
    """

    @abstractmethod
    async def search_for_parts(self, parts: list[str]):
        """
        Abstract method to search for parts.
        Subclasses must implement this method to provide specific functionality.

        Args:
            parts (list[str]): A list of part names to search for.
        """
        pass


class ApifyPcPartPicker(SracperClient):
    """
    This class provides an interface to interact with the Apify API for PCPartPicker data.
    It uses the ApifyClientAsync to perform asynchronous operations.
    """

    def __init__(self):
        """
        Initializes the PcPartPicker class with an instance of ApifyClientAsync using the API key from settings.
        """
        self.__client = ApifyClientAsync(
            token=seetings_manager.APIFY_CLIENT_API
        )

    async def search_for_parts(self, parts: list[str]):
        """
        Searches for parts on the Apify platform using the provided list of part names.

        Args:
            parts (list[str]): A list of part names to search for.
        Returns:
            A list of search results from the Apify platform.
        """
        try:
            apifiy_actor = self.__client.actor(
                actor_id="Shovan_Saha/matyascimbulka/pcpartpicker-scraper"
            )
            inputs = {
                "part_names": parts
            }

            call_results = await apifiy_actor.call(run_input=inputs.get("part_names"))
            logger.info("pc parts has been parse sucessflyy")
            yield call_results

        except Exception as error:
            logger.error(
                "there is an error to parse pc parts please try again later ")
            raise WebsiteSrapperErrorHandeler(messages=error)


class PcPartsPicker(SracperClient):
    """
    This class provides an interface to interact with the PCPartPicker website for searching parts.
    It uses web scraping techniques to retrieve data from the website.
    """

    async def search_for_parts(self, parts: list[str]):
        """
        Searches for parts on the PCPartPicker website using the provided list of part names.

        Args:
            parts (list[str]): A list of part names to search for.
        Returns:
            A list of search results from the PCPartPicker website
        """
        try:
            for part in parts:
                api = API(region="us")

                # Supported categories include 'cpu', 'motherboard', 'video-card', etc.
                cpu_data = await api.retrieve(part)
            # Data is returned as a structured object that converts easily to JSON
                logger.info(f"Searching for part: {part}")
                return cpu_data.to_json()

        except Exception as error:
            logger.error(
                "there is an error to parse pc parts please try again later ")
            raise WebsiteSrapperErrorHandeler(messages=error)
