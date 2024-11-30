FROM --platform=linux/amd64 python:3.9

ENV DEBIAN_FRONTEND=noninteractive


# Install basic dependencies
# Install basic dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    ca-certificates \
    && apt-get clean

# Add Google's official GPG key and repository
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-linux.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Fetch the latest compatible ChromeDriver version
RUN set -eux; \
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1); \
    echo "Detected Chrome major version: $CHROME_VERSION"; \
    CHROMEDRIVER_VERSION=$(curl -sSL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION" || echo ""); \
    if [ -z "$CHROMEDRIVER_VERSION" ]; then \
        echo "No specific ChromeDriver found for Chrome version $CHROME_VERSION, falling back to the latest version."; \
        CHROMEDRIVER_VERSION=$(curl -sSL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"); \
    fi; \
    if [ -z "$CHROMEDRIVER_VERSION" ]; then \
        echo "Error: Could not fetch ChromeDriver version."; \
        exit 1; \
    fi; \
    echo "Fetching ChromeDriver version: $CHROMEDRIVER_VERSION"; \
    wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"; \
    unzip chromedriver_linux64.zip -d /usr/local/bin/; \
    chmod +x /usr/local/bin/chromedriver; \
    rm chromedriver_linux64.zip

# Verify installations
RUN google-chrome --version && chromedriver --version
ENV PATH=$PATH:/usr/local/bin

RUN mkdir /app/
WORKDIR /app/

COPY src /app/src/
COPY requirements.txt /app/

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN python3 -m venv .venv
COPY docker-entrypoint.sh /usr/bin/

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]