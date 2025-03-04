FROM mcr.microsoft.com/playwright/python:v1.41.0

WORKDIR /app

RUN apt-get update && apt-get install -y wget tar
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps
RUN wget -qO - https://github.com/allure-framework/allure2/releases/download/2.32.2/allure-2.32.2.tgz | tar -xz -C /opt/
ENV PATH="/opt/allure-2.32.2/bin:${PATH}"

COPY . .

CMD ["bash", "-c", "pytest --alluredir=allure-results && allure serve allure-results"]
