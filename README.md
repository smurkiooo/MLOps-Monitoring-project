# MLOps Monitoring Project

Сервис оценивает стоимость квартиры в рублях по 15 признакам. FastAPI принимает характеристики квартиры и передаёт их обученному пайплайну с CatBoost. Prometheus опрашивает сервис по адресу `/metrics`, а Grafana строит графики по собранным данным.

## Быстрый запуск

Нужен Docker с плагином Compose. Перейдите в каталог `services` из корня репозитория.

```bash
cd services
```

В каталоге `services` создайте файл `.env`. Если файл уже есть, проверьте значения в нём. Пароль из примера предназначен для локального запуска.

```dotenv
APP_PORT=1702
GRAFANA_USER=admin
GRAFANA_PASS=local-dev-password
```

Запустите контейнеры из каталога `services`.

```bash
docker compose up --build -d
docker compose ps
```

| Компонент | Адрес |
| --- | --- |
| FastAPI и форма для пробных запросов | [localhost:1702/docs](http://localhost:1702/docs) |
| Метрики FastAPI | [localhost:1702/metrics](http://localhost:1702/metrics) |
| Статус сбора метрик в Prometheus | [localhost:9090/targets](http://localhost:9090/targets) |
| Grafana | [localhost:3000](http://localhost:3000) |

Отправьте [пример запроса](Instructions.md#запрос-на-оценку-квартиры), затем проверьте, что цель Prometheus имеет статус `UP`. После первого сбора метрик выполните в Prometheus запрос `prediction_requests_total{status="success"}`. Цель опрашивается каждые 15 секунд.

[Инструкции по запуску](Instructions.md) содержат пример `curl`, команды запуска API отдельно и параметры генератора нагрузки. [Руководство по мониторингу](Monitoring.md) описывает настройку Grafana, метрики и запросы PromQL.

## Где что лежит

| Путь | Назначение |
| --- | --- |
| [services/ml_service/](services/ml_service/) | Маршруты FastAPI, обработчик запроса и модель `baseline.pkl`, которую загружает сервис |
| [services/docker-compose.yaml](services/docker-compose.yaml) | Конфигурация FastAPI, Prometheus и Grafana |
| [services/prometheus/prometheus.yml](services/prometheus/prometheus.yml) | Цель и интервал сбора метрик |
| [services/fake_load.py](services/fake_load.py) | Генератор запросов с синтетическими признаками |
| [dashboard.json](dashboard.json), [dashboard.jpg](dashboard.jpg) | Экспорт дашборда Grafana и его снимок |
| [load_model.ipynb](load_model.ipynb) | Пример экспорта ранее обученного пайплайна в `baseline.pkl` и просмотра его признаков |

Для запуска достаточно модели из `services/ml_service/`. Ноутбук загружает модель по абсолютному пути из исходного окружения. Если нужно повторить экспорт, укажите свой путь к обученному пайплайну в `MODEL_PATH`.
