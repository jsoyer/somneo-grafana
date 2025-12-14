# Somneo to Grafana

Export sensor data from your Philips Somneo to InfluxDB for visualization in Grafana.

## Architecture

The project contains three main components:

1. **somneo-exporter**: Python application that periodically reads data from the Somneo
2. **InfluxDB**: Time-series database to store sensor data
3. **Grafana**: Visualization tool to create dashboards

## Available Sensors

The Somneo exposes the following data:
- `temperature`: Current temperature (°C)
- `humidity`: Relative humidity (%)
- `light`: Light level (lux)
- `noise`: Noise level
- `avg_temperature`, `avg_humidity`, `avg_light`, `avg_noise`: Averages

## Installation

### Prerequisites

- Docker and Docker Compose
- A Philips Somneo connected to the local network

### Configuration

1. Clone the repository
2. Copy `.env.example` to `.env` and adjust the values:

```bash
cp .env.example .env
```

3. Modify your Somneo's IP address in `.env`:

```env
SOMNEO_HOST=192.168.1.1  # Replace with your Somneo's IP
```

### Launch

```bash
docker-compose up -d
```

This command launches the three services:
- **InfluxDB**: http://localhost:8086
- **Grafana**: http://localhost:3000

## Grafana Access

1. Open http://localhost:3000
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. The "Somneo Sensors" dashboard is automatically provisioned

## Advanced Configuration

### Environment Variables

Edit `docker-compose.yml` or create a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `SOMNEO_HOST` | Somneo IP address | `192.168.1.1` |
| `SOMNEO_PORT` | Somneo HTTPS port | `443` |
| `SOMNEO_LOCATION` | Location tag | `bedroom` |
| `POLL_INTERVAL` | Read interval (seconds) | `1800` (30 min) |
| `INFLUXDB_HOST` | InfluxDB host | `influxdb` |
| `INFLUXDB_PORT` | InfluxDB port | `8086` |
| `INFLUXDB_DATABASE` | InfluxDB database | `sensors` |
| `INFLUXDB_USER` | InfluxDB user | `somneo` |
| `INFLUXDB_PASSWORD` | InfluxDB password | `somneopassword` |

### Local Development with uv

If you want to run the application outside of Docker:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -e .

# Run the application
export SOMNEO_HOST=192.168.1.1
export INFLUXDB_HOST=localhost
export INFLUXDB_PORT=8086
export INFLUXDB_DATABASE=sensors
export INFLUXDB_USER=somneo
export INFLUXDB_PASSWORD=somneopassword
python -m somneo.main
```

## Project Structure

```
somneo-grafana/
├── src/
│   └── somneo/
│       ├── __init__.py
│       ├── main.py                    # Main entry point
│       ├── somneo_fetch.py            # Somneo API client
│       └── influxdb_exporter.py       # InfluxDB export
├── grafana-datasource/
│   └── influxdb.yml                   # Datasource configuration
├── grafana-dashboard/
│   ├── dashboard.yml                  # Dashboard provider
│   └── somneo-sensors.json            # Sensor dashboard
├── Dockerfile                          # Docker image with uv
├── docker-compose.yml                  # Complete stack
├── pyproject.toml                      # Python/uv configuration
└── README.md
```

## InfluxQL Queries

Examples of queries to create your own visualizations:

### Temperature over 24h
```sql
SELECT mean("temperature") FROM "somneo_sensors" WHERE time > now() - 24h GROUP BY time(5m) fill(null)
```

### Average Humidity
```sql
SELECT mean("humidity") FROM "somneo_sensors" WHERE time > now() - 1h
```

### All Sensors
```sql
SELECT mean("temperature"), mean("humidity"), mean("light"), mean("noise") 
FROM "somneo_sensors" 
WHERE $timeFilter 
GROUP BY time($__interval) fill(null)
```

## Troubleshooting

### The somneo-exporter container doesn't start

Check the logs:
```bash
docker-compose logs somneo-exporter
```

### Cannot connect to the Somneo

1. Verify that the Somneo is on the same network
2. Test connectivity: `curl -k https://<SOMNEO_IP>/di/v1/products/1/wusrd`
3. Check the IP address in `docker-compose.yml`

### No data in Grafana

1. Verify that InfluxDB is receiving data:
   ```bash
   docker exec -it somneo-influxdb influx
   > use sensors
   > show measurements
   > select * from somneo_sensors limit 10
   ```

2. Check the datasource in Grafana:
   - Settings > Data Sources > InfluxDB-Somneo
   - Click "Save & Test"

### InfluxDB connection issues

If the exporter cannot connect to InfluxDB, make sure:
- InfluxDB container is running: `docker ps`
- Network is properly configured
- Credentials match in both `docker-compose.yml` and the exporter configuration

## License

MIT
