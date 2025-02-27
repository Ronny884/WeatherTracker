import pytest
import aiohttp
from aioresponses import aioresponses
from src.config import settings
from src.business_logic.services.weather_api import fetch_weather


@pytest.fixture
def weather_url():
    return f"https://api.openweathermap.org/data/2.5/weather?q=Минск&appid={settings.weather_api_key}&units=metric&lang=ru"


@pytest.mark.asyncio
async def test_fetch_weather_success(weather_url):
    city_name = "Минск"
    expected_weather_data = {"weather": "sunny", "temperature": 20}

    with aioresponses() as m:
        m.get(weather_url, payload=expected_weather_data)

        weather_data = await fetch_weather(city_name)
        assert weather_data == expected_weather_data


@pytest.mark.asyncio
async def test_fetch_weather_client_response_error(weather_url):
    city_name = "Минск"

    with aioresponses() as m:
        m.get(weather_url, status=404)

        weather_data = await fetch_weather(city_name)
        assert weather_data is None


@pytest.mark.asyncio
async def test_fetch_weather_client_connection_error(weather_url):
    city_name = "Минск"

    with aioresponses() as m:
        m.get(weather_url, exception=aiohttp.ClientConnectionError)

        weather_data = await fetch_weather(city_name)
        assert weather_data is None


@pytest.mark.asyncio
async def test_fetch_weather_unexpected_error(mocker):
    city_name = "777"
    mocker.patch("src.business_logic.services.weather_api.fetch_weather", side_effect=Exception("Unexpected error"))

    weather_data = await fetch_weather(city_name)
    assert weather_data is None
