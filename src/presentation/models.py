from pydantic import BaseModel


class GetWeatherData(BaseModel):
    city: str

    class Config:
        arbitrary_types_allowed = True