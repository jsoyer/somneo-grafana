#!/usr/bin/env python3
import json
import sys
import requests
import urllib3

urllib3.disable_warnings()  # Somneo utilise souvent un cert auto-signé

DEFAULT_HOST = "192.168.1.180"
DEFAULT_PORT = 443
ENDPOINT = "/di/v1/products/1/wusrd"

def fetch_somneo(host: str, port: int, verify_ssl: bool = False) -> dict:
    url = f"https://{host}:{port}{ENDPOINT}"
    resp = requests.get(url, verify=verify_ssl, timeout=30, stream=True)
    resp.raise_for_status()
    return resp.json()

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT

    data = fetch_somneo(host, port)
    readings = {
        "temperature": data.get("mstmp"),
        "humidity": data.get("msrhu"),
        "light": data.get("mslux"),
        "noise": data.get("mssnd"),
        # valeurs moyennes dispo si besoin : avtmp, avhum, avlux, avsnd
    }
    print(json.dumps(readings, indent=2))

if __name__ == "__main__":
    main()
