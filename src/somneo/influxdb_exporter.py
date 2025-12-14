import logging
from datetime import datetime
from typing import Dict

from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)


class InfluxDBExporter:
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        username: str | None = None,
        password: str | None = None,
    ):
        self.client = InfluxDBClient(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
        )
        self.database = database

        # Create database if it doesn't exist
        try:
            databases = self.client.get_list_database()
            if {"name": database} not in databases:
                self.client.create_database(database)
                logger.info(f"Created database: {database}")
        except Exception as e:
            logger.warning(f"Could not check/create database: {e}")

    def write_sensor_data(self, sensor_data: Dict, location: str = "bedroom"):
        json_body = [
            {
                "measurement": "somneo_sensors",
                "tags": {"location": location},
                "time": datetime.utcnow().isoformat(),
                "fields": {},
            }
        ]

        for key, value in sensor_data.items():
            if value is not None:
                json_body[0]["fields"][key] = float(value)

        if not json_body[0]["fields"]:
            logger.warning("No valid fields to write")
            return

        try:
            self.client.write_points(json_body)
            logger.info(f"Successfully wrote data to InfluxDB: {sensor_data}")
        except Exception as e:
            logger.error(f"Failed to write to InfluxDB: {e}")
            raise

    def close(self):
        self.client.close()
