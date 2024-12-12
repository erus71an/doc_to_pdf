
# Document Converter API

Document Converter API — это веб-приложение на основе FastAPI для конвертации документов (DOC, DOCX, XLS, XLSX) в формат PDF с использованием LibreOffice и `unoconv`. Сервис предоставляет REST API для обработки локально загруженных файлов.

---

## **Функциональность**

- Конвертация загруженных файлов в PDF (`POST /convert`).
- Мониторинг состояния сервиса:
  - Проверка здоровья (`GET /healthcheck`).
  - Метрики Prometheus (`GET /metrics`).
- Документация API доступна в формате OpenAPI через Swagger UI.

---

## **Технологии**

- **FastAPI**: Фреймворк для разработки веб-приложений.
- **LibreOffice**: Для конвертации документов.
- **unoconv**: Инструмент для взаимодействия с LibreOffice в режиме командной строки.
- **Prometheus Client**: Для мониторинга метрик.
---

## **Структура проекта**

```
project/
│
├── main.py                # Основной файл приложения FastAPI
├── converter.py           # Класс для обработки файлов с использованием LibreOffice и unoconv
├── file_validator.py      # Валидация имён и форматов файлов
├── temp_file_manager.py   # Работа с временными файлами
├── logger.py              # Логирование запросов и ошибок
├── metrics.py             # Метрики для мониторинга
├── requirements.txt       # Зависимости проекта
├── Dockerfile             # Конфигурация для Docker
└── readme.md              # Документация проекта
```

---

## **Установка**

### **1. Локальная установка**

Убедитесь, что у вас установлен Python 3.10+ и LibreOffice.

1. Клонируйте репозиторий:
   ```bash
   git clone <URL>
   cd <project-directory>
   ```

2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустите сервер:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### **2. Установка через Docker**

1. Постройте Docker-образ:
   ```bash
   docker build -t document-converter .
   ```

2. Запустите контейнер:
   ```bash
   docker run -p 8000:8000 document-converter
   ```

---

## **Документация API**

Документация доступна в формате OpenAPI через Swagger UI и ReDoc:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Используйте Swagger UI для тестирования API и просмотра всех доступных эндпоинтов.

---

## **Мониторинг**

- **Prometheus**:
  Добавьте следующую конфигурацию в `prometheus.yml`:
  ```yaml
  scrape_configs:
    - job_name: 'document-converter'
      static_configs:
        - targets: ['127.0.0.1:8000']
  ```

- **Grafana**:
  Настройте Prometheus как источник данных и создайте дашборды для анализа метрик.

---

## **Использование**

### **Эндпоинты**

#### **1. Конвертация файла в PDF**
- **URL**: `POST /convert`
- **Описание**: Конвертирует загруженный файл в формат PDF.
- **Пример запроса**:
  ```bash
  curl -X POST -F "file=@example.docx" http://127.0.0.1:8000/convert
  ```
- **Пример ответа**: Скачивание PDF-файла.

#### **2. Проверка здоровья сервиса**
- **URL**: `GET /healthcheck`
- **Описание**: Проверяет доступность сервиса и LibreOffice.
- **Пример запроса**:
  ```bash
  curl http://127.0.0.1:8000/healthcheck
  ```
- **Пример ответа**:
  ```json
  {
    "status": "ok",
    "details": "Сервис работает исправно"
  }
  ```

#### **3. Метрики Prometheus**
- **URL**: `GET /metrics`
- **Описание**: Предоставляет метрики в формате Prometheus.

---

## **Мониторинг**

- **Prometheus**:
  Добавьте следующую конфигурацию в `prometheus.yml`:
  ```yaml
  scrape_configs:
    - job_name: 'document-converter'
      static_configs:
        - targets: ['127.0.0.1:8000']
  ```

- **Grafana**:
  Настройте Prometheus как источник данных и создайте дашборды для анализа метрик.

---

## **Разработчики**

- **Автор**: [iru71an]

---

Теперь ваш сервис готов к использованию для конвертации документов в формате PDF!
