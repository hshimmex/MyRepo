Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary packages including jq
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Fetch compatible ChromeDriver version based on installed Chrome
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1-3) && \
    CHROME_VERSIONS_DATA=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json) && \
    CHROME_VERSIONS_LIST=$(echo $CHROME_VERSIONS_DATA | jq -r '.versions | reverse | .[] | select(.version | startswith("'"$CHROME_VERSION"'"))') && \
    echo "$CHROME_VERSIONS_LIST" | while read -r version; do \
        HOSTS_DATA=$(echo "$version" | jq -r '.downloads.chromedriver[] | select(.platform=="linux64") | .url'); \
        wget -q "$HOSTS_DATA" -O chromedriver.zip && \
        unzip chromedriver.zip -d /usr/local/bin/ && \
        rm chromedriver.zip; \
        break; \
    done

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the tests
CMD ["python", "-m", "pytest", "-n", "auto"]