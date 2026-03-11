FROM python:3.12-slim AS base
WORKDIR /app
COPY .. /app
RUN pip install --no-cache-dir -r /app/requirements.txt
ENTRYPOINT ["python", "-m", "nexus_mcp_hub.hub"]
