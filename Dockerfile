FROM python:3.7

WORKDIR /app

WORKDIR /usr/share/ca-certificates/extra
COPY support/DOIRootCA2.cer DOIRootCA2.crt
RUN echo "extra/DOIRootCA2.crt" >> /etc/ca-certificates.conf && update-ca-certificates

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.6/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=c3b78d342e5413ad39092fd3cfc083a85f5e2b75

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/aqmswatcher
COPY DOIRootCA.crt .
COPY setup.py .
COPY setup.cfg .
COPY aqmswatcher aqmswatcher
RUN python setup.py install

COPY cron-aqmswatcher .
RUN pip freeze > requirements.txt
CMD ["/usr/local/bin/supercronic", "/app/aqmswatcher/cron-aqmswatcher"]
