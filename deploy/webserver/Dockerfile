FROM caddy:2.8-alpine

ARG USER_UID=1000
ARG USER_USERNAME=web
ARG APP_DIR=/var/opt/webapp
ENV DEVELOPMENT=0

RUN adduser -u "${USER_UID}" -H -D "${USER_USERNAME}" \
    && apk add --no-cache yarn

RUN mkdir -p "${APP_DIR}" \
    && mkdir -p /srv \
    && mkdir -p /config/caddy \
    && chown -R "${USER_UID}:${USER_UID}" "${APP_DIR}" \
    && chown -R "${USER_UID}:${USER_UID}" /srv \
    && chown -R "${USER_UID}:${USER_UID}" /config/caddy

COPY ./deploy/webserver/docker-entrypoint.sh /usr/local/bin
RUN chmod a+x /usr/local/bin/docker-entrypoint.sh

WORKDIR "${APP_DIR}"
COPY --chown="$USER_UID:$USER_UID" webapp/ "${APP_DIR}"
USER "${USER_USERNAME}"
#RUN yarn \
#    && yarn build \
#    && mv build/* /srv \
#    && chown -R "${USER_UID}:${USER_UID}" /srv

COPY ./deploy/webserver/Caddyfile /etc/caddy/Caddyfile
CMD [ "/usr/local/bin/docker-entrypoint.sh" ]
