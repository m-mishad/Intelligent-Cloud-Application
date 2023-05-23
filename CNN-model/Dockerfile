FROM ubuntu:latest

# Set the working directory
WORKDIR /app

# Set environment variable to disable interactive prompts
ENV DEBIAN_FRONTEND=noninteractive


# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libopencv-dev

# Copy the code into the container
COPY . . 

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python3", "app.py"]




