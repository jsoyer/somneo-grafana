from typing import Dict

import requests
import urllib3

urllib3.disable_warnings()

ENDPOINT = "/di/v1/products/1/wusrd"

def fetch_somneo(host: str, port: int = 443, verify_ssl: bool = False) -> Dict:
    url = f"https://{host}:{port}{ENDPOINT}"
    resp = requests.get(url, verify=verify_ssl, timeout=30)
    resp.raise_for_status()
    return resp.json()

    return resp.json()

def parse_sensor_data(data: Dict) -> Dict:
    return {
        "temperature": data.get("mstmp"),
        "humidity": data.get("msrhu"),
        "light": data.get("mslux"),
        "noise": data.get("mssnd"),
        "avg_temperature": data.get("avtmp"),
        "avg_humidity": data.get("avhum"),
        "avg_light": data.get("avlux"),
        "avg_noise": data.get("avsnd"),
    }
