FROM python:3.10-slim

ENV PYTHONPATH "${PYTHONPATH}:/code"

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=1000 \
  POETRY_VERSION=1.4

WORKDIR /code

RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction

COPY . .

CMD ["gunicorn", \
    "--access-logfile", "/dev/stdout", \
    "--error-logfile", "/dev/stderr", \
    "--timeout", "120", \
    "--bind", "0.0.0.0:80", \
    "adapters.flask.app:app"]
