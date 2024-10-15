# Dockerfile
FROM selenium/standalone-chrome

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Switch to root user to install pip and other packages
USER root

# Install necessary packages including pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean


# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the tests
CMD ["python", "-m", "pytest", "-n", "auto"]
