import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from prometheus_client import generate_latest


from file_validator import FileValidator
from converter import Converter
from health_checker import HealthChecker
from temp_file_manager import TempFileManager
from logger import logger
from metrics import REQUEST_COUNT, REQUEST_LATENCY
from fastapi.openapi.utils import get_openapi
from starlette.background import BackgroundTask

app = FastAPI(
    title="Документ Конвертер API",
    description="Этот сервис позволяет конвертировать файлы в \
        формат PDF с использованием LibreOffice.",
    version="1.0.0",
)


# Кастомизация OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.middleware("http")
async def add_metrics_and_logging_middleware(request, call_next):
    """
    Middleware для сбора метрик и логирования запросов.
    """
    endpoint = request.url.path
    method = request.method
    logger.info(f"Получен запрос: {method} {endpoint}")
    with REQUEST_LATENCY.labels(endpoint=endpoint).time():
        response = await call_next(request)
    status = response.status_code
    logger.info(f"Ответ для {method} {endpoint} со статусом {status}")
    REQUEST_COUNT.labels(endpoint=endpoint, method=method, status=status).inc()
    return response


@app.get("/metrics", response_class=PlainTextResponse, summary="Метрики для Prometheus")
async def metrics():
    """
    Эндпоинт для экспорта метрик в формате Prometheus.

    Используйте этот эндпоинт для мониторинга сервиса с помощью Prometheus.
    """
    logger.info("Эндпоинт /metrics вызван")
    return PlainTextResponse(generate_latest())


@app.get("/healthcheck", summary="Проверка здоровья сервиса")
async def healthcheck():
    """
    Проверяет доступность сервиса и наличие LibreOffice.

    Возвращает:
    - **200 OK**: Если сервис работает.
    - **500 Internal Server Error**: Если LibreOffice недоступен или есть проблемы.
    """
    try:
        logger.info("Эндпоинт /healthcheck вызван")
        if not HealthChecker.check_libreoffice():
            logger.error("LibreOffice не доступен")
            return JSONResponse(
                status_code=500,
                content={"status": "error", "details": "LibreOffice не доступен"},
            )
        return {"status": "ok", "details": "Сервис работает исправно"}
    except Exception as e:
        logger.exception("Ошибка в /healthcheck")
        return JSONResponse(
            status_code=500, content={"status": "error", "details": str(e)}
        )


@app.post(
    "/convert",
    summary="Конвертировать файл в PDF",
    description="Загруженный файл конвертируется в PDF с использованием LibreOffice. \
        Поддерживаются форматы `.doc`, `.docx`, `.xls`, `.xlsx`.",
    responses={
        200: {"description": "Файл успешно конвертирован."},
        400: {"description": "Файл неподдерживаемого формата."},
        500: {"description": "Ошибка при конвертации файла."},
    },
)
async def convert_document(
    file: UploadFile = File(
        ..., description="Загружаемый файл форматов .doc, .docx, .xls, .xlsx"
    )
):
    """
    Конвертирует загруженный файл в PDF.

    Пример успешного запроса:
    ```
    curl -X POST "http://127.0.0.1:8000/convert" -F "file=@example.doc"
    ```
    """
    if not FileValidator.is_allowed(file.filename):
        logger.warning(f"Файл с неподдерживаемым форматом: {file.filename}")
        raise HTTPException(status_code=400, detail="Файл неподдерживаемого формата")

    temp_manager = TempFileManager()
    try:
        logger.info(f"Начата обработка файла: {file.filename}")
        output_file_name = os.path.splitext(os.path.basename(file.filename))[0] + ".pdf"
        input_file_path = temp_manager.get_temp_path(
            "original" + os.path.splitext(os.path.basename(file.filename))[1]
        )
        output_file_path = temp_manager.get_temp_path('converted.pdf')

        # Сохраняем загруженный файл
        with open(input_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Конвертируем файл
        Converter.convert_to_pdf(output_file_path, input_file_path)

        # Возвращаем результат
        if not os.path.exists(output_file_path):
            logger.error(f"Ошибка конвертации файла: {file.filename}")
            temp_manager.cleanup()
            raise HTTPException(status_code=500, detail="Ошибка при конвертации файла")

        logger.info(f"Файл успешно конвертирован: {file.filename} в {output_file_path}")

        return FileResponse(
            output_file_path,
            media_type="application/pdf",
            filename = output_file_name,
            background=BackgroundTask(lambda: temp_manager.cleanup()),
        )
    except Exception as err:
        HTTPException(status_code=500, detail="Что-то пошло не так")
