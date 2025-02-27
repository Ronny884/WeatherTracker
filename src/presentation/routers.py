import json
import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.presentation.models import GetWeatherData
from src.business_logic.services.weather_api import fetch_weather
from src.data_access.orm import get_last_10_weather_records, add_weather_record


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/",
            response_class=HTMLResponse,
            summary='Main page')
async def index(request: Request):
    """
    Отображает главную страницу.
    """
    return templates.TemplateResponse("index.html", {'request': request})


@router.post("/get_weather/",
             summary='Get and show weather data by city name')
async def get_weather(data: GetWeatherData) -> JSONResponse:
    """
    Получает и отображает данные о погоде по названию города.
    Добавляет данные в БД.

    :param data: Данные о городе
    :return: JSON-ответ с данными о погоде
    """
    weather_info = await fetch_weather(city_name=data.city)
    if weather_info:
        await add_weather_record(city=data.city, json_data=weather_info)
    return JSONResponse(content=weather_info)


@router.get("/show_history/",
            summary='Show history data')
async def get_history() -> JSONResponse:
    """
    Отображает историю данных о погоде, что берётся из БД.

    :return: JSON-ответ с записями о погоде
    """
    last_10_weather_records = await get_last_10_weather_records()
    return JSONResponse(content=last_10_weather_records)