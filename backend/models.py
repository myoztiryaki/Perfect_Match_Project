from pydantic import BaseModel

class PersonalBirthInfo(BaseModel):
    day: int
    month: int
    year: int
    hour: int
    min: int
    lat: float
    lon: float
    tzone: float
    day2: int
    month2: int
    year2: int
    hour2: int
    min2: int
    lat2: float
    lon2: float
    tzone2: float
    class Config:
        schema_extra = {
            "example": {
                "day": 11,
                "month": 8,
                "year": 1990,
                "hour": 14,
                "min": 10,
                "lat": 40.99,
                "lon": 29.02,
                "tzone": 3,
                "day2": 31,
                "month2": 12,
                "year2": 1993,
                "hour2": 13,
                "min2": 20,
                "lat2": 40.99,
                "lon2": 29.02,
                "tzone2": 2,
            }
        }
        
