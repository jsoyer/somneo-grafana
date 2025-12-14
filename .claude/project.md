# Somneo to Grafana Project

## Project Overview

This project exports sensor data from a Philips Somneo device to InfluxDB 1.12 for visualization in Grafana. It's a Python application containerized with Docker, using uv for dependency management.

## Architecture

The stack consists of three Docker containers:
- **somneo-exporter**: Python app that polls the Somneo API and writes to InfluxDB
- **influxdb**: InfluxDB 1.12 time-series database
- **grafana**: Grafana for data visualization with pre-configured dashboards

## Project Structure

```
somneo-grafana/
├── src/somneo/              # Python application source code
│   ├── main.py              # Entry point - polling loop and configuration
│   ├── somneo_fetch.py      # Somneo API client
│   └── influxdb_exporter.py # InfluxDB writer using influxdb client
├── grafana-datasource/      # Grafana datasource provisioning
│   └── influxdb.yml         # InfluxDB datasource config
├── grafana-dashboard/       # Grafana dashboard provisioning
│   ├── dashboard.yml        # Dashboard provider config
│   └── somneo-sensors.json  # Pre-built dashboard with 4 panels
├── Dockerfile               # Multi-stage build with uv
├── docker-compose.yml       # Full stack orchestration
└── pyproject.toml          # Python dependencies
```

## Key Technologies

- **Python 3.12**: Application runtime
- **uv**: Fast Python package installer
- **InfluxDB 1.12**: Time-series database (using InfluxQL, not Flux)
- **influxdb Python client 5.3.x**: InfluxDB 1.x compatible client
- **Grafana**: Dashboard and visualization
- **Docker & Docker Compose**: Containerization

## Somneo API

The Somneo exposes sensor data via HTTPS endpoint:
- **Endpoint**: `https://<IP>:443/di/v1/products/1/wusrd`
- **Authentication**: None (local network)
- **SSL**: Self-signed certificate (verify=False)

Available sensors:
- `mstmp`: Current temperature (°C)
- `msrhu`: Current humidity (%)
- `mslux`: Current light level (lux)
- `mssnd`: Current noise level
- `avtmp`, `avhum`, `avlux`, `avsnd`: Average values

## InfluxDB Schema

- **Database**: `sensors`
- **Measurement**: `somneo_sensors`
- **Tags**: `location` (e.g., "bedroom")
- **Fields**: temperature, humidity, light, noise, avg_temperature, avg_humidity, avg_light, avg_noise

## Environment Variables

### Somneo Configuration
- `SOMNEO_HOST`: IP address of Somneo (default: 192.168.1.180)
- `SOMNEO_PORT`: HTTPS port (default: 443)
- `SOMNEO_LOCATION`: Tag for data location (default: bedroom)
- `POLL_INTERVAL`: Polling interval in seconds (default: 60)

### InfluxDB Configuration
- `INFLUXDB_HOST`: InfluxDB hostname (default: influxdb)
- `INFLUXDB_PORT`: InfluxDB port (default: 8086)
- `INFLUXDB_DATABASE`: Database name (default: sensors)
- `INFLUXDB_USER`: Username (default: somneo)
- `INFLUXDB_PASSWORD`: Password (default: somneopassword)

## Development Notes

### Docker Build
The Dockerfile uses the official uv Docker image and installs dependencies system-wide. The application code is copied to `/app/somneo/` and run directly with relative imports.

### Python Module Structure
The application uses **relative imports** in main.py because it's executed directly (not as a package):
```python
from influxdb_exporter import InfluxDBExporter
from somneo_fetch import fetch_somneo, parse_sensor_data
```

### InfluxDB 1.x vs 2.x
This project uses **InfluxDB 1.12** with the `influxdb` Python client (not `influxdb-client`). Key differences:
- Uses username/password authentication (not tokens/orgs)
- Uses databases (not buckets)
- Grafana queries use **InfluxQL** (not Flux)

## Common Commands

```bash
# Build and start all services
docker-compose up -d

# Rebuild specific service
docker-compose build somneo-exporter

# View logs
docker-compose logs -f somneo-exporter

# Stop all services
docker-compose down

# View InfluxDB data
docker exec -it somneo-influxdb influx
> use sensors
> show measurements
> select * from somneo_sensors limit 10
```

## Troubleshooting

### Import errors in container
Ensure relative imports are used in main.py since it's run directly, not as a module.

### No data in Grafana
1. Check exporter logs: `docker-compose logs somneo-exporter`
2. Verify InfluxDB has data: `docker exec -it somneo-influxdb influx`
3. Test Somneo connectivity: `curl -k https://<IP>/di/v1/products/1/wusrd`

### InfluxDB connection refused
Wait 10-15 seconds after starting InfluxDB for it to be ready. The exporter will retry on errors.
