from abc import ABC, abstractmethod
from typing import List
from app.config import seetings_manager
import asyncio
from apify_client import ApifyClientAsync
from app.utils import WebsiteSrapperErrorHandeler
from loguru import logger
from pcpartpicker import API
from app.config import seetings_manager
from langchain.tools import tool


class ExcicutionFcutions(ABC):
    """
    Abstract base class for execution functions.
    This class defines the interface for execution functions that can be implemented by subclasses.
    ```async def tool_excute(input)```
    """
    @abstractmethod
    async def tool_excute(self, inputs: List[str]) -> str:
        pass


class ApifyPcPartPicker(ExcicutionFcutions):
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

    @tool
    async def tool_excute(self, parts: list[str]):
        """
        Searches for parts on the Apify platform using the provided list of part names.

        Args:
            parts (list[str]): A list of part names to search for.
        Returns:
            A list of search results from the Apify platform.
        """
        try:
            apifiy_actor = self.__client.actor(
                actor_id=seetings_manager.Actor_id
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


#################################
# pcpartpicker
#################################

def __tool_excute(self, inputs: list[str]):
    """
    Searches for parts on the PCPartPicker website using the provided list of part names.

    Args:
        parts (list[str]): A list of part names to search for.
    Returns:
        A list of search results from the PCPartPicker website
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    api = API(region="us")
    results = []

    for part in inputs:
        logger.info(f"Searching for part: {part}")
        try:
            # Inside this thread, api.retrieve can now safely hook into the loop we just set up
            cpu_data = api.retrieve(part, force_refresh=True)
            results.append(cpu_data.to_json())
        except Exception as e:
            logger.error(f"Error retrieving part '{part}': {e}")
            continue

    return results


@tool
async def tool_excute(self, inputs: list[str]):
    """
    Searches for parts on the PCPartPicker website using the provided list of pc  part names.
    Args:
        parts (list[str]): A list of part names to search for.
    Returns:
        A list of search results from the PCPartPicker website.

    """

    try:
        result = await asyncio.to_thread(self.__tool_excute, inputs)
        return result

    except Exception as error:
        logger.error(
            "there is an error to parse pc parts please try again later ")
        raise WebsiteSrapperErrorHandeler(messages=error)
