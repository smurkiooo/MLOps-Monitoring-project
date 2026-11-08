# Мониторинг предсказаний

## Проверка Prometheus

После [запуска Compose](README.md#быстрый-запуск) откройте [страницу Targets](http://localhost:9090/targets). Цель `scrapping-main-app` должна быть в состоянии `UP`. Встроенный сборщик опрашивает `http://fastapi_app:1702/metrics` каждые 15 секунд.

Если цель в состоянии `DOWN`, проверьте, отвечает ли [локальный адрес метрик](http://localhost:1702/metrics), и посмотрите журнал `docker compose logs main-app prometheus` из каталога `services`. При ошибке разрешения имени `fastapi_app` замените цель на `main-app:1702` в [prometheus.yml](services/prometheus/prometheus.yml) и выполните `docker compose restart prometheus`. Если меняете `APP_PORT`, укажите тот же порт в цели Prometheus.

## Настройка Grafana

1. Откройте [Grafana](http://localhost:3000) и войдите с учётными данными из `services/.env`.
2. В разделе **Connections → Data sources** добавьте Prometheus. В поле **Prometheus server URL** укажите `http://prometheus:9090` и нажмите **Save & test**. Этот адрес доступен из контейнера Grafana по имени сервиса Compose.
3. Откройте **Dashboards → New → Import** и загрузите [dashboard.json](dashboard.json). Файл использует схему V2 Resource. Если Grafana не принимает этот формат, создайте панели вручную по запросам ниже. [Импорт дашбордов в Grafana](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/import-dashboards/)
4. В редакторе каждой панели выберите созданный источник Prometheus. Экспорт содержит ссылку на источник из исходного окружения. Скрипт `fix_datasource_uid.py` ожидает поля `datasource.type` и `datasource.uid`, тогда как в текущем JSON используется `datasource.name`. Настройте источник через интерфейс Grafana.
5. Подставьте PromQL из таблицы. В экспортированном дашборде часть панелей показывает сырые счётчики или бакеты.

## Метрики

| Метрика | Что измеряет |
| --- | --- |
| `prediction_requests_total{status="success"}` и `prediction_requests_total{status="error"}` | Число вызовов обработчика с предсказанием или ошибкой. Запросы, отклонённые FastAPI до вызова обработчика, в эти счётчики не попадают. |
| `prediction_value_bucket`, `prediction_value_count`, `prediction_value_sum` | Гистограмма успешных предсказаний в рублях. Бакеты группируют цены по верхней границе `le`. Счётчик `_count` хранит число наблюдений, а `_sum` их сумму. |
| `last_prediction_latency_seconds` | Время работы обработчика для последнего запроса, в секундах. Между сборами значение может обновиться несколько раз. |
| `http_requests_total` | HTTP-запросы по маршруту, методу и группе статусов. Ошибка предсказания с HTTP `200` учитывается в группе `2xx`. |

## Запросы для панелей

| Панель | PromQL |
| --- | --- |
| Задержка последнего предсказания | `last_prediction_latency_seconds` |
| Успешные предсказания за последние 15 минут | `sum(increase(prediction_value_count[15m]))` |
| Оценка 95-го процентиля предсказанных цен за 5 минут | `histogram_quantile(0.95, sum by (le) (rate(prediction_value_bucket[5m])))` |
| HTTP-запросы с ответом `2xx` за 15 минут, по методу | `sum by (method) (increase(http_requests_total{method=~"GET\|POST",status="2xx"}[15m]))` |

Фильтр HTTP-статусов считает и запросы к служебным маршрутам. Для панели по одному API добавьте в селектор `handler="/api/price/"`. Для разбивки вызовов модели по результату используйте `sum by (status) (increase(prediction_requests_total[15m]))`.

Если график пуст, сначала проверьте состояние цели в Prometheus. Затем [создайте нагрузку](Instructions.md#генерация-нагрузки) и дождитесь нескольких сборов метрик. Для `rate` и `increase` нужны как минимум две точки в выбранном окне.
