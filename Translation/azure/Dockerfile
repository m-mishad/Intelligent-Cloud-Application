FROM python:3.9-alpine3.14

WORKDIR /app

COPY . .

RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc musl-dev && \
    apk add --no-cache libffi-dev openssl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

ENV KEY=""
ENV ENDPOINT=""
ENV LOCATION=""

# Expose the port
EXPOSE 5002

CMD ["python", "translate-azure.py"]



