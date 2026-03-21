FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime

COPY src/ src/
COPY policies/ policies/
COPY prompt_packages/ prompt_packages/
COPY schemas/ schemas/

ENV PYTHONPATH=/app/src
ENV APP_ENV=production
ENV APP_DEBUG=false

EXPOSE 8000

CMD ["uvicorn", "agentguard.main:app", "--host", "0.0.0.0", "--port", "8000"]
