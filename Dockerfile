FROM python:3.10-slim

# Установка LibreOffice, шрифтов и зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    unoconv \
    fontconfig \
    build-essential \
    python3-pip \
    wget \
    cabextract && \
    wget -q https://downloads.sourceforge.net/corefonts/andale32.exe && \
    cabextract -F '*' -d /usr/share/fonts/truetype/msttcorefonts andale32.exe && \
    fc-cache -f && \
    apt-get clean && rm -rf /var/lib/apt/lists/* andale32.exe


# Создаем символическую ссылку для Python и LibreOffice
RUN ln -s /usr/bin/python3 /usr/lib/libreoffice/program/python

# Установка Python-зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .


# Форматирование и проверка синтаксиса
#RUN black --check . && flake8 .

# Указываем порт и команду запуска
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]