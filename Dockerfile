#checkov:skip=CKV_DOCKER_2
#checkov:skip=CKV_DOCKER_3
FROM python:3.15.1-alpine@sha256:54448f67d7c31c39e5cdd3ea2d6382395ce142806c284425f8e897d78a0465b3 AS builder

WORKDIR /

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv==0.13.5 && \
  uv export --frozen --no-dev --no-emit-project --format=requirements-txt > requirements.txt

FROM python:3.15.1-alpine@sha256:54448f67d7c31c39e5cdd3ea2d6382395ce142806c284425f8e897d78a0465b3 AS validator

WORKDIR /

RUN  apk add --no-cache git

COPY --chmod=755 run.sh run.sh
COPY validator validator

COPY --from=builder requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "/run.sh" ]
