# Use the official Python base image with Alpine Linux
FROM python:3.9-alpine3.14

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache gcc musl-dev

# Copy the application code to the container
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the prediction server URL
ENV PREDICTION=""

# Set the environment variable for the translation server URL
ENV TRANSLATION=""

# Set the environment variable for the text-to-speech server URL
ENV TTS=""

# Expose the port on which the Flask app will run
EXPOSE 5001

# Start the Flask application
CMD ["python", "app_translation_speech.py"]

