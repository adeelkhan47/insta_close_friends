FROM --platform=linux/amd64 python:3.9

ENV DEBIAN_FRONTEND=noninteractive
ARG CACHEBUST=1

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable || (apt-get update && apt-get -f install -y) && \
    google-chrome-stable --version && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add Google Chrome to the repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Clear any cache to ensure we fetch the latest packages and then update the packages
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update -y

# Install Google Chrome with verbose output and log its version
RUN apt-get install -y google-chrome-stable || (apt-get update && apt-get -f install -y) && \
    google-chrome-stable --version
RUN which google-chrome-stable
RUN export CHROME_BIN=/usr/bin/google-chrome

ENV PATH=$PATH:/usr/local/bin

RUN mkdir /app/
WORKDIR /app/

COPY src /app/src/
COPY requirements.txt /app/

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN python3 -m venv .venv
COPY docker-entrypoint.sh /usr/bin/

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]