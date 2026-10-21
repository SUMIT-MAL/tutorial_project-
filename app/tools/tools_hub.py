import serpapi
from loguru import logger
from app.utils import ToolsHubErrorHandeler
from app.config.settings import seetings_manager


def image_search(query):
    """
    This method performs an image search using the SerpApi client.
    :param query: The search query for the image search.
    """
    try:
        if seetings_manager.SERPAPI_API:
            serpapi_client = serpapi.Client(
                api_key=seetings_manager.SERPAPI_API,
                timeout=60
            )
        else:
            logger.warning("agent tools are not avalabile")
            return seetings_manager.SERPAPI_API
        results = serpapi_client.search({
            "engine": "google_images",
            "q": f"{query}",
            "async": "true",
            "tbm": "isch"
        })
        logger.info("image search excuted succesfully")
        image_results = results.get("images_results", [])
        output = [
            {
                "title": item.get("title", "")[:150],
                "thumbnail": item.get("thumbnail", ""),
                "source": item.get("source", ""),
            }
            for item in image_results[:5]
        ]
        logger.info("Image search returned {} results", len(output))
        return output

    except Exception as error:
        logger.error(f"Error in image search: {error}")
        return ToolsHubErrorHandeler(messages="there is an error in image search api call")


def description_search(query):
    """
    This method performs a description search using the SerpApi client.
    :param query: The search query for the description search.
    """
    try:
        if seetings_manager.SERPAPI_API:
            serpapi_client = serpapi.Client(
                api_key=seetings_manager.SERPAPI_API,
                timeout=60
            )
        else:
            logger.warning("agent tools are not avalabile")
            return seetings_manager.SERPAPI_API
        results = serpapi_client.search({
            "engine": "google",
            "q": f"{query}",
            "async": "true"
        })
        logger.info("description search excuted sauccesfully")
        description_results = results.get("organic_results", [])
        output = [
            {
                "title": item.get("title", "")[:150],
                "thumbnail": item.get("thumbnail", ""),
                "source": item.get("source", ""),
            }
            for item in description_results[:5]
        ]

        logger.info("description search returned {} results", len(output))
        return output

    except Exception as error:
        logger.error(f"Error in description search: {error}")
        return ToolsHubErrorHandeler(messages="there is an error in description search api call")


def shoping_serach_link(query):
    """
    This method performs a shoping link search using the SerpApi client.
    :param query: The search query for the shoping link search.    
    """
    try:
        if seetings_manager.SERPAPI_API:
            serpapi_client = serpapi.Client(
                api_key=seetings_manager.SERPAPI_API,
                timeout=60
            )
        else:
            logger.warning("agent tools are not avalabile")
            return seetings_manager.SERPAPI_API

        results = serpapi_client.search({
            "engine": "amazon_product",
            "async": "true",
            "k": f"{query}",
        })
        logger.info("shoping link search search excuted sauccesfully")
        shoping_serach_link = results.get("organic_results", [])
        output = [
            {
                "title": item.get("title", "")[:150],
                "thumbnail": item.get("thumbnail", ""),
                "source": item.get("source", ""),
            }
            for item in shoping_serach_link[:5]
        ]

        logger.info("Image search returned {} results", len(output))
        return output

    except Exception as error:
        logger.error(f"Error in description search: {error}")
        return ToolsHubErrorHandeler(messages="there is an error in description search api call")
