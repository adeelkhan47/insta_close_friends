FROM --platform=linux/amd64 python:3.9

ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    ca-certificates

# Add Google's official GPG key and repository
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-linux.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome (stable)
RUN apt-get update && apt-get install -y google-chrome-stable

# Install the latest ChromeDriver
RUN wget -q "https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
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