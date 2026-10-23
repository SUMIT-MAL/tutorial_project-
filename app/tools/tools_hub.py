import serpapi
from loguru import logger
from app.config.settings import seetings_manager
from langchain.tools import tool
import asyncio


def _client():
    if not seetings_manager.SERPAPI_API:
        logger.warning("agent tools are not available")
        return None
    return serpapi.Client(api_key=seetings_manager.SERPAPI_API, timeout=60)


async def image_search(query: str):
    """Find a product image for a PC part. Returns image URL and title."""
    try:
        client = _client()
        if client is None:
            return "error: search tool not configured"
        results = client.search({
            "engine": "google_images",
            "q": query,
            "gl": "in",
        })
        items = results.get("images_results") or []
        items = [i for i in items if isinstance(i, dict)][:1]
        if not items:
            return "No image found, skip this part's image."
        i = items[0]
        return [{
            "title": (i.get("title") or "")[:150],
            "image": i.get("original") or i.get("thumbnail", ""),
            "source": i.get("source", ""),
        }]
    except Exception as error:
        logger.error(f"Error in image search: {error}")
        return "error: image search failed, skip this part's image."


async def description_search(query: str):
    """Get a short description / specs snippet for a PC part."""
    try:
        client = _client()
        if client is None:
            return "error: search tool not configured"
        results = client.search({
            "engine": "google",
            "q": query,
            "gl": "in",
            "hl": "en",
        })
        return results
    except Exception as error:
        logger.error(f"Error in description search: {error}")
        return "error: description search failed."


async def shoping_serach_link(query: str):
    """Get price (INR), shopping link and image for a PC part."""
    try:
        client = _client()
        if client is None:
            return "error: search tool not configured"
        results = client.search({
            "engine": "google_shopping",
            "q": query,
            "gl": "in",
            "hl": "en",
        })
        return results
    except Exception as error:
        logger.error(f"Error in shopping search: {error}")
        return "error: shopping search failed."


@tool
async def image_search_thread(query):
    """
    This function is a wrapper for the image_search function that runs it in a separate thread.
    It uses asyncio.to_thread to run the image_search function in a separate thread and returns the result.
    Args:
        query (str): The query string to search for.
    Returns:
        The result of the image_search function.
    """
    image_result = await asyncio.to_thread(
        image_search,
        query
    )
    return image_result


@tool
async def shoping_link_search_thread(query):
    """
    This function is a wrapper for the shoping_serach_link function that runs it in a separate thread.
    It uses asyncio.to_thread to run the shoping_serach_link function in a separate thread and returns the result.
    Args:
        query (str): The query string to search for.
    Returns:
        The result of the shoping_serach_link function.
    """
    shoping_result = await asyncio.to_thread(
        shoping_serach_link,
        query
    )
    return shoping_result


@tool
async def description_search_thread(query):
    """
    This function is a wrapper for the description_search function that runs it in a separate thread.
    It uses asyncio.to_thread to run the description_search function in a separate thread and returns the result.
    Args:
        query (str): The query string to search for.
    Returns:
        The result of the description_search function.
    """
    description_result = await asyncio.to_thread(
        description_search,
        query
    )
    return description_result
