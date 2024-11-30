FROM --platform=linux/amd64 python:3.9

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y wget unzip

# Install Google Chrome (stable)
RUN apt-get install -y google-chrome-stable

# Install the latest ChromeDriver
RUN wget -q "https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Verify installations
RUN google-chrome-stable --version && chromedriver --version
ENV PATH=$PATH:/usr/local/bin

RUN mkdir /app/
WORKDIR /app/

COPY src /app/src/
COPY requirements.txt /app/

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN python3 -m venv .venv
COPY docker-entrypoint.sh /usr/bin/

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]