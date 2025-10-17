FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    xvfb \
    libglib2.0-0 \
    libnss3 \
    libfontconfig1 \
    libxss1 \
    libxtst6 \
    libxrandr2 \
    libxcomposite1 \
    libasound2 \
    fonts-liberation \
    openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*





RUN apt-get update && apt-get install -y wget curl gnupg2 ca-certificates \
    && curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-key.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y google-chrome-stable


# RUN wget -q "https://chromedriver.storage.googleapis.com/117.0.5938.92/chromedriver_linux64.zip" \
#     && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
#     && rm chromedriver_linux64.zip \
#     && chmod +x /usr/local/bin/chromedriver



ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /tests
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz -O allure.tgz \
    && tar -zxvf allure.tgz -C /opt/ \
    && ln -s /opt/allure-2.27.0/bin/allure /usr/local/bin/allure \
    && rm allure.tgz

COPY . .

CMD ["pytest", "--alluredir=reports/allure-results"]