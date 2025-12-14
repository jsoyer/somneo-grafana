FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy application code
COPY src/ ./

# Install dependencies using uv
RUN uv pip install --system requests influxdb urllib3

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "somneo/main.py"]
