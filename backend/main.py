import requests
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request
from models import PersonalBirthInfo
from processing import perfectmatch


load_dotenv()

app = FastAPI()

#def apiRequester(DAY,MONTH,YEAR,HOUR,MIN,LAT,LON,TZONE):
#    headers = {
#                    'Content-Type': 'application/x-www-form-urlencoded',
#                    'Authorization': f'Basic {os.getenv("AUTH")}'
#            }
#
#    url = f'{os.getenv("API")}'
#    payload = f"day={DAY}&month={MONTH}&year={YEAR}&hour={HOUR}&min={MIN}&lat={LAT}&lon={LON}&tzone={TZONE}"
#    response = requests.request("POST", url, headers=headers, data=payload)
#    return response


@app.post("/astroinfo", response_model=dict)
async def astroconnection(request: PersonalBirthInfo):
    features = {
        "DAY": request.day,
        "MONTH": request.month,
        "YEAR": request.year,
        "HOUR": request.hour,
        "MIN": request.min,
        "LAT": request.lat,
        "LON": request.lon,
        "TZONE": request.tzone
    }

    features2 = {
        "DAY": request.day2,
        "MONTH": request.month2,
        "YEAR": request.year2,
        "HOUR": request.hour2,
        "MIN": request.min2,
        "LAT": request.lat2,
        "LON": request.lon2,
        "TZONE": request.tzone2
    }

    percentage, ruh_esi_durum, ruh_ikizi_durum = perfectmatch(features,features2)

    response_data = {
        "percentage": percentage,
        "ruh_ikizi_durum": ruh_ikizi_durum,
        "ruh_esi_durum": ruh_esi_durum
    }
    """
    Bir ton fonksiyonlar eklenecek.
    """
    
    return response_data