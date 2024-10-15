# Dockerfile
FROM selenium/standalone-chrome

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary packages including jq
USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py


# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the tests
CMD ["python", "-m", "pytest", "-n", "auto"]
