FROM python:3.9-alpine3.14

WORKDIR /app

COPY . .
RUN apk --no-cache add gcc musl-dev libffi-dev openssl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del gcc musl-dev libffi-dev openssl-dev


ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_DEFAULT_REGION=""

# Expose the port
EXPOSE 5003


CMD ["python", "translate-aws.py"]

