# Запуск и проверка API

[Быстрый запуск через Docker Compose](README.md#быстрый-запуск) поднимает API вместе с Prometheus и Grafana. Для отдельной проверки предсказания можно запустить только API.

## Запрос на оценку квартиры

Отправьте `POST /api/price/` с JSON. Поле `user_id` содержит строковый идентификатор, который сервис возвращает вместе с оценкой. В `model_params` обязательны все 15 полей из примера. `has_elevator`, `is_apartment` и `studio` принимают логические значения. Остальные признаки числовые.

```bash
curl -sS http://localhost:1702/api/price/ \
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
```

Успешный ответ содержит `user_id` и числовое поле `prediction` с оценкой в рублях.

```json
{"user_id":"user_123","prediction":32105205.888474908}
```

Если в теле запроса отсутствует обязательное поле или его значение не проходит проверку типа, FastAPI возвращает HTTP `422`. Если обработчик перехватил исключение при предсказании, сервис возвращает HTTP `200` с полем `ошибка`. При проверке результата ищите поле `prediction`.

## Запуск в Python

Используйте Python 3.11, как в Docker-образе. Выполните команды из корня репозитория.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r services/requirements.txt

cd services/ml_service
python -m uvicorn main_app:app --host 127.0.0.1 --port 1702
```

Запускайте Uvicorn из `services/ml_service`, поскольку обработчик ищет `baseline.pkl` в рабочем каталоге. Для остановки нажмите `Ctrl+C`.

## Запуск одного контейнера

Выполните команды из корня репозитория.

```bash
cd services
docker build -f Dockerfile_ml_service -t ml_service:local .
docker run --rm --name ml_service -p 127.0.0.1:1702:1702 ml_service:local
```

Для остановки нажмите `Ctrl+C` или выполните `docker stop ml_service` в другом терминале.

## Генерация нагрузки

После запуска API откройте второй терминал в корне репозитория.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install requests
python services/fake_load.py --requests 500 --delay 0.05
```

Если окружение уже создано для запуска API, активируйте его и начните с установки `requests`. Без аргументов скрипт отправляет 67 последовательных запросов с паузой 0,4 секунды после каждого. Адрес `http://localhost:1702/api/price/` задан в константе `URL`. Скрипт печатает прогресс каждые 50 запросов и считает запрос успешным, когда получает HTTP `200` и поле `prediction`.

## Остановка Compose

Выполните команды из корня репозитория.

```bash
cd services
docker compose down
```

В Compose у Grafana нет постоянного тома для данных. Экспортируйте настроенный дашборд перед удалением контейнера, если хотите сохранить изменения.
