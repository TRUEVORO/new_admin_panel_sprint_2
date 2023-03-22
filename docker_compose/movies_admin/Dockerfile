FROM python:3.11.2-slim-buster as build

WORKDIR /opt/movies_admin

COPY ./requirements.txt .

RUN apt update \
    && apt install -y gcc libpq-dev \
    && python -m venv venv \
    && venv/bin/pip install --no-cache-dir --upgrade pip \
    && venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.11.2-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/movies_admin/venv/bin:${PATH}"

ARG APP=/opt/movies_admin
ARG USER=web

WORKDIR ${APP}

RUN apt update \
    && apt install -y --no-install-recommends  \
      libpq-dev \
      netcat \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r ${USER} \
    && useradd -d ${APP} -r -g ${USER} ${USER} \
    && mkdir ${APP}/static

COPY --chown=${USER}:${USER} --from=build ${APP}/venv ./venv
COPY --chown=${USER}:${USER} . .

RUN chmod +x ${APP}/entrypoint.sh \
    && chown -R ${USER}:${USER} ${APP}/static

USER ${USER}

ENTRYPOINT ["/opt/movies_admin/entrypoint.sh"]
