import asyncio
import aiohttp
import logging

from src.config import settings


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def fetch_weather(city_name):
    """
    Получает данные о погоде для указанного города посредством API OpenWeatherMap.

    :param city_name: Название города
    :return: Словарь с данными о погоде или None в случае ошибки
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={settings.weather_api_key}&units=metric&lang=ru"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                weather_data = await response.json()
                logger.info(f'Successfully fetched weather data for {city_name}')
                return weather_data
    except aiohttp.ClientResponseError as e:
        logger.error(f"Client response error: {e.status}")
        return None
    except aiohttp.ClientConnectionError:
        logger.error("Connection error")
        return None
    except aiohttp.ClientError as e:
        logger.error(f"Client error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return

