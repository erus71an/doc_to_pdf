import os
import tempfile
import shutil


class TempFileManager:
    """Класс для управления временными файлами."""

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    def get_temp_path(self, filename: str) -> str:
        """Возвращает полный путь к файлу внутри временной директории."""
        return os.path.join(self.temp_dir, filename)

    def get_tempdir_files(self):
        """Возвращает список файлов и поддиректорий во временной директории."""
        for root, dirs, files in os.walk(self.temp_dir):
            yield root, dirs, files

    def cleanup(self):
        """Удаляет временную директорию и все её содержимое."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
