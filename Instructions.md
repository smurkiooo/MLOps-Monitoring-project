# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-sprint3-completed
Если необходимо перейти в поддиректорию, напишите соотвесвтующую команду

## 1. FastAPI микросервис в виртуальном окружение
```python
# команды создания виртуального окружения
# и установки необходимых библиотек в него
python3 -m venv .spr3_venv
source .spr3_venv/bin/activate


# команда перехода в директорию
cd services
cd ml_service


# команда запуска сервиса с помощью uvicorn
```
uvicorn main_app:app --reload --port 8081 --host 0.0.0.0
```



### Пример curl-запроса к микросервису

```bash

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

```

Возвращает:

```
{
  "user_id": "user_123",
  "prediction": 32105205.888474908
}
```


## 2. FastAPI микросервис в Docker-контейнере

(все команды выполняются из поддиректории services)
в условии указано запускать без Docker Compose

```bash
cd services

export $(grep -v '^#' .env | xargs)

docker image build \
  --build-arg AUTHOR=${AUTHOR} \
  --build-arg APP_PORT=${APP_PORT} \
  --tag ml_service:latest \
  -f Dockerfile_ml_service \
  .

docker container run \
  --name ml_service \
  --env APP_PORT=${APP_PORT} \
  --publish ${APP_PORT}:${APP_PORT} \
  --detach \
  ml_service:latest
```

### Пример curl-запроса к микросервису

```bash

curl -X POST \
  'http://localhost:1702/api/price/' \
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
      "total_area": 65.8}
    }'
```

Ответ сервиса : {"user_id":"user_123","prediction":32105205.888474908}(.spr3_venv)

P.S. Dockerfile находится внутри папки services под названием 'Dockerfile_ml_service'

## 3. Docker compose для микросервиса и системы моониторинга

```bash
#(из корневой папки проекта)
cd services
docker compose up --build


```

микросервис находится по адресу: localhost:1702
Prometheus : localhost:9090
Grafana : localhost:3000

P.S. для Прометея и Графаны нужно вручную перенаправить порты




### Пример curl-запроса к микросервису

```bash
curl -X POST \
  'http://localhost:1702/api/price/' \
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
      "total_area": 65.8}
    }'
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует <...> запросов в течение <...> секунд ...

```
# команды необходимые для запуска скрипта
...
```

Адреса сервисов:
- микросервис: http://localhost:<port>
- Prometheus: ...
- Grafana: ...