FROM python:3.10-slim as python-base
RUN pip install poetry==1.7.1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN touch README.md
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root --without dev


###############################
FROM python-base as development
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    FASTAPI_ENV=development

COPY --from=python-base ${VIRTUAL_ENV} ${VIRTUAL_ENV}
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --with dev --no-root
# Mount the code here to auto reload.
COPY api ./api
WORKDIR /app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

###############################
FROM python-base as production
ENV FASTAPI_ENV=production
COPY --from=python-base $PYSETUP_PATH $PYSETUP_PATH
COPY api ./api
WORKDIR /app
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api.main:app"]
