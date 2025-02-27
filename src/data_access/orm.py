from __future__ import annotations
import json
from typing import TYPE_CHECKING
from logging import getLogger, INFO, ERROR
from sqlalchemy.future import select

from src.data_access.models import Weather
from src.data_access.db_connector import db_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


logger = getLogger(__name__)
logger.setLevel(ERROR)


async def add_weather_record(
        city: str,
        json_data,
        session: AsyncSession = db_session) -> None:
    """
    Добавление новой записи о погоде в базу данных.

    :param city: Город
    :param json_data: Данные о погоде в формате JSON
    :param session: Сессия базы данных
    :return: None
    """
    try:
        new_record = Weather(
            city=city,
            json_data=json_data
        )
        async with session.begin():
            session.add(new_record)
            await session.commit()
        logger.info(f"Запись о погоде для города {city} успешно добавлена.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении записи о погоде: {str(e)}")
        raise


async def get_last_10_weather_records(session: AsyncSession = db_session) -> list[dict]:
    """
    Получение последних 10 записей о погоде из базы данных (если записей меньше, чем 10,
    то возвращаются все).

    :param session: Сессия базы данных
    :return: Список словарей с данными о погоде
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(Weather).order_by(Weather.query_id.desc()).limit(10)
            )
            records = result.scalars().all()

        logger.info("Успешно получена история запросов.")
        return [
            {
                'city': record.city,
                'date_time': record.date_time.strftime("%d.%m.%Y %H:%M"),
                'temp': record.json_data['main']['temp'],
                'description': record.json_data['weather'][0]['description']
            }
            for record in records
        ]
    except Exception as e:
        logger.error(f"Ошибка при получении записей о погоде: {str(e)}")
        raise


