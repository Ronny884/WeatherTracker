import asyncio
import logging
import pytest
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.config import settings
from src.presentation.routers import router

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """
    Настраивает логирование для приложения.

    :return: None
    """
    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '[%(asctime)s] %(levelname)s - %(filename)s'
            '[%(lineno)d]: %(message)s'
        )
    )


setup_logging()
app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )

    # запуск тестов
    # pytest.main(["-v", "tests/business_logic/services/test_weather_api.py"])
