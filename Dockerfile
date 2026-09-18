FROM python:3.12-slim
WORKDIR /app
# requirements копируем отдельно от кода: COPY сбрасывает кеш
# всех слоёв ниже, а зависимости меняются реже кода
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
