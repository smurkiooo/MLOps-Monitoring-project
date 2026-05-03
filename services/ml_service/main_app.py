from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi_handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
import numpy as np
from prometheus_client import Histogram, Counter, Gauge
import time

'''

uvicorn main_app:app --reload --port 8081 --host 0.0.0.0



curl -X 'POST' \
  'http://localhost:8081/api/price/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "user_123",
  "model_params": {
    "age": 15,
    "building_type_int": 2,
    "latitude": 55.7558,
    "longitude": 37.6173,
    "ceiling_height": 2.9,
    "flats_count": 85,
    "floors_total": 9,
    "has_elevator": true,
    "floor": 4,
    "kitchen_area": 12.5,
    "living_area": 42.3,
    "rooms": 3,
    "is_apartment": true,
    "studio": false,
    "total_area": 65.8
  }
}'

'''


app = FastAPI()
app.handler = FastApiHandler()
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

class ModelParams(BaseModel):
    age: float
    building_type_int: float
    latitude: float
    longitude: float
    ceiling_height: float
    flats_count: float
    floors_total: float
    has_elevator: bool
    floor: float
    kitchen_area: float
    living_area: float
    rooms: float
    is_apartment: bool
    studio: bool
    total_area: float


class PredictRequest(BaseModel):
    user_id: str
    model_params: ModelParams



# общее число предсказаний с разбивкой по статусу (success / error)
prediction_requests_total = Counter(
    "prediction_requests_total",
    "общее кол-во запросов на предсказание",
    ["status"],
)

# распределение предсказанных цен 
prediction_value_rubles = Histogram(
    "prediction_value",
    "распределение предсказанных цен в рублях",
    buckets=[1e6, 3e6, 5e6, 8e6, 12e6, 20e6, 35e6, 60e6, 100e6],
)

# время обработки последнего запроса в секундах
last_prediction_latency_seconds = Gauge(
    "last_prediction_latency_seconds",
    "время обработки последнего запроса в секундах",
)

@app.post("/api/price/")
def price_prediction(request: PredictRequest):
    all_params = {
        "user_id": request.user_id,
        "model_params": request.model_params.model_dump(),
    }
    t0 = time.perf_counter()                        
    result = app.handler.handle(all_params)
    t1 = time.perf_counter() - t0              

    last_prediction_latency_seconds.set(t1)    

    if "prediction" in result:
        prediction_requests_total.labels(status="success").inc()  
        prediction_value_rubles.observe(result["prediction"])     
    else:
        prediction_requests_total.labels(status="error").inc()    

    return result
