FROM python:3.12-alpine

ARG APP_DIR=/var/www
ARG APP_USER=web
ARG APP_USER_UID=1000
ENV PYTHONPYCACHEPREFIX=/var/cache/pycache

RUN adduser -D -h "${APP_DIR}" -u "${APP_USER_UID}" "${APP_USER}" \
    && mkdir -p "${PYTHONPYCACHEPREFIX}" \
    && chown -R "${APP_USER}:${APP_USER}" "${PYTHONPYCACHEPREFIX}" \
    && mkdir -p /etc/gunicorn

WORKDIR "${APP_DIR}"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown="${APP_USER}:${APP_USER}" server .
COPY deploy/apiserver/docker-entrypoint.sh /usr/local/bin
COPY deploy/apiserver/gunicorn.conf.py /etc/gunicorn
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

USER "${APP_USER}"

CMD [ "/usr/local/bin/docker-entrypoint.sh" ]
