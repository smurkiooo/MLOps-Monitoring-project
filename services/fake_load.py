import argparse
import random
import time
import requests

URL = "http://localhost:1702/api/price/"

def random_params() -> dict:
    total_area = round(random.uniform(20, 200), 1)
    living_area = round(total_area * random.uniform(0.4, 0.7), 1)
    kitchen_area = round(total_area * random.uniform(0.1, 0.25), 1)
    floors_total = random.randint(3, 25)
    floor = random.randint(1, floors_total)
    return {
        "age": random.randint(0, 80),
        "building_type_int": random.randint(0, 5),
        "latitude": round(random.uniform(55.5, 56.0), 4),
        "longitude": round(random.uniform(37.2, 37.9), 4),
        "ceiling_height": round(random.uniform(2.5, 3.5), 1),
        "flats_count": random.randint(10, 500),
        "floors_total": floors_total,
        "has_elevator": random.choice([True, False]),
        "floor": floor,
        "kitchen_area": kitchen_area,
        "living_area": living_area,
        "rooms": random.randint(1, 5),
        "is_apartment": random.choice([True, False]),
        "studio": False,
        "total_area": total_area,
    }


def run(url:str, n_requests : int, delay: float) -> None:
    ok = err = 0
    for i in range(1, n_requests + 1):
        payload = {"user_id": f"load_user_{i}", "model_params": random_params()}
        try:
            resp = requests.post(url, json=payload, timeout=5)
            if resp.status_code == 200 and "prediction" in resp.json():
                ok += 1
            else:
                err += 1
        except requests.RequestException as e:
            err += 1
        if i % 50 == 0:
            print(f"  {i}/{n_requests} sent  |  ok={ok}  err={err}")

        time.sleep(delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="симуляция нагрузки")
    parser.add_argument("--requests", type=int, default=67, dest="n_requests")
    parser.add_argument("--delay", type=float, default=0.4)
    args = parser.parse_args()

    print(f" {args.n_requests} запросов с паузой {args.delay} сек")
    run(URL, args.n_requests, args.delay)
