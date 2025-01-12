#checkov:skip=CKV_DOCKER_2
#checkov:skip=CKV_DOCKER_3
FROM python:3.13-alpine AS builder

WORKDIR /

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry==2.0.0 && \
  pip install poetry-plugin-export && \
  poetry export --output=requirements.txt

FROM python:3.13-alpine AS validator

WORKDIR /

COPY --chmod=755 run.sh run.sh
COPY validator validator

COPY --from=builder requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "/run.sh" ]
