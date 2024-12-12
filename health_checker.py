from subprocess import call


class HealthChecker:
    """Класс для проверки состояния сервиса."""

    @staticmethod
    def check_libreoffice() -> bool:
        """Проверяет доступность LibreOffice."""
        result = call("libreoffice --version", shell=True)
        return result == 0
