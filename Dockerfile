#checkov:skip=CKV_DOCKER_2
#checkov:skip=CKV_DOCKER_3
FROM python:3.14-alpine AS builder

WORKDIR /

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv==0.9.0 && \
  uv export --format=requirements-txt > requirements.txt

FROM python:3.13-alpine AS validator

WORKDIR /

RUN  apk add --no-cache git=2.52.0-r0

COPY --chmod=755 run.sh run.sh
COPY validator validator

COPY --from=builder requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "/run.sh" ]
