# Use the Selenium standalone Chrome image
FROM selenium/standalone-chrome

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Switch to root user to install packages
USER root

# Install necessary packages including python3 and virtualenv
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment and install requirements
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Switch back to the selenium user
USER seluser

# Set the PATH to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Command to run the tests
CMD ["python", "-m", "pytest", "-n", "auto"]
