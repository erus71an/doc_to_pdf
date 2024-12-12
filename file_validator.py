import re

class FileValidator:
    """Класс для проверки типа загружаемых файлов."""

    ALLOWED_EXTENSIONS = {"doc", "docx", "xls", "xlsx"}

    @staticmethod
    def is_allowed(filename: str) -> bool:
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in FileValidator.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def validate_and_escape(filename: str) -> str:
        """
        Проверяет и конвертирует имя файла в формат, совместимый с UNIX-путями,
        с экранированием пробелов.

        :param filename: Исходное имя файла.
        :return: Имя файла, подходящее для UNIX-путей.
        """
        if not filename:
            raise ValueError("Имя файла не может быть пустым.")

        # Убираем недопустимые символы
        # Разрешённые символы: буквы, цифры, дефисы, подчёркивания, точки и пробелы
        sanitized = re.sub(r"[^\w.\s-]", "", filename, flags=re.UNICODE)

        # Экранируем пробелы для использования в UNIX
        escaped = sanitized.replace(" ", r"\ ")

        # Ограничиваем длину имени файла
        max_length = (
            255  # Ограничение на длину имени файла в большинстве файловых систем
        )
        escaped = escaped[:max_length]

        # Если результат пустой после обработки
        if not escaped:
            raise ValueError("Имя файла содержит только недопустимые символы.")

        return escaped
