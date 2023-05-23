# Base image
FROM python:3.9-alpine3.14

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copy the code into the container
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt


# Set the environment variables
ENV ACCESS_KEY=""
ENV SECRET_KEY=""
ENV REGION_NAME=""

# Expose the required port
EXPOSE 5004

# Start the Flask application
CMD ["python", "speech_aws.py"]

