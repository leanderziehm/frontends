# Base image
FROM python:3.14-slim AS base

# Set working directory
WORKDIR /app

COPY pyproject.toml .
RUN pip install .

COPY src src
COPY static static

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8100"]