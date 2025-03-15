# Switch to the target image
FROM alpine:edge

# Arguments
ARG CONT_UID=1001
ARG CONT_USER=docker

ARG BUILD_COMMIT=unknown
ARG BUILD_BRANCH=unknown

# Environment
ENV TZ=Asia/Shanghai
ENV DUALSTACK 1
ENV IP 0.0.0.0
ENV PORT 1688
ENV EPID ""
ENV LCID 1033
ENV CLIENT_COUNT 26
ENV ACTIVATION_INTERVAL 120
ENV RENEWAL_INTERVAL 10080
ENV HWID RANDOM
ENV LOGLEVEL INFO
ENV LOGFILE STDOUT
ENV LOGSIZE ""
ENV WEBUI 0

WORKDIR /app

COPY requirements.txt start.py healthcheck.py /app/
COPY py-kms /app

RUN apk add --no-cache --update \
  python3 \
  py3-pip \
  sqlite-libs \
  ca-certificates \
  tzdata \
  && pip3 install --no-cache-dir -r /app/requirements.txt --break-system-packages \
  && mkdir -p /app/db \
  # Fix undefined timezone, in case the user did not mount the /etc/localtime
  && ln -sf /usr/share/zoneinfo/UTC /etc/localtime

RUN chmod 550 /app/start.py /app/healthcheck.py

# HEALTHCHECK --interval=5m --timeout=10s --start-period=10s --retries=3 CMD /usr/bin/python3 /app/healthcheck.py

RUN addgroup --system --gid ${CONT_UID} ${CONT_USER} \
&& adduser --home "/app" --shell "/bin/sh" --uid ${CONT_UID} --ingroup ${CONT_USER} --disabled-password ${CONT_USER}

RUN chown -Rf ${CONT_USER}:${CONT_USER} /app

USER ${CONT_USER}

ENTRYPOINT [ "/usr/bin/python3", "-u", "/app/start.py" ]