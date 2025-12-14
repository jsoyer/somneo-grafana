#!/usr/bin/env python3
import logging
import os
import time

from influxdb_exporter import InfluxDBExporter
from somneo_fetch import fetch_somneo, parse_sensor_data

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    somneo_host = os.getenv("SOMNEO_HOST", "192.168.1.1")
    somneo_port = int(os.getenv("SOMNEO_PORT", "443"))

    influxdb_host = os.getenv("INFLUXDB_HOST", "influxdb")
    influxdb_port = int(os.getenv("INFLUXDB_PORT", "8086"))
    influxdb_database = os.getenv("INFLUXDB_DATABASE", "sensors")
    influxdb_user = os.getenv("INFLUXDB_USER", "somneo")
    influxdb_password = os.getenv("INFLUXDB_PASSWORD", "somneopassword")

    location = os.getenv("SOMNEO_LOCATION", "bedroom")
    interval = int(os.getenv("POLL_INTERVAL", "1800"))

    logger.info(f"Starting Somneo exporter for {somneo_host}:{somneo_port}")
    logger.info(
        f"Writing to InfluxDB at {influxdb_host}:{influxdb_port}, database: {influxdb_database}"
    )
    logger.info(f"Poll interval: {interval} seconds")

    exporter = InfluxDBExporter(
        host=influxdb_host,
        port=influxdb_port,
        database=influxdb_database,
        username=influxdb_user,
        password=influxdb_password,
    )

    try:
        while True:
            try:
                logger.info("Fetching Somneo sensor data...")
                raw_data = fetch_somneo(somneo_host, somneo_port)
                sensor_data = parse_sensor_data(raw_data)

                logger.info(f"Sensor data: {sensor_data}")
                exporter.write_sensor_data(sensor_data, location)

            except Exception as e:
                logger.error(f"Error during data collection: {e}")

            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        exporter.close()


if __name__ == "__main__":
    main()
