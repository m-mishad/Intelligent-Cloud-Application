FROM ubuntu:latest

WORKDIR /app

# Install system dependencies
RUN echo "deb http://security.ubuntu.com/ubuntu focal-security main" | tee /etc/apt/sources.list.d/focal-security.list && \ 
    apt-get update && \
    apt-get install -y build-essential \
                       libssl-dev \
                       ca-certificates \
                       libasound2 \
                       libssl1.1 \
                       python3 \
                       python3-pip

RUN rm /etc/apt/sources.list.d/focal-security.list


# Copy the application code into the container
COPY . .

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt


# Set the environment variables
ENV SPEECH_KEY=""
ENV SPEECH_LOCATION=""

# Expose the port that Flask will run on
EXPOSE 5005

# Run the Flask application
CMD ["python3", "speech_azure.py"]
