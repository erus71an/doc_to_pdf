import logging
from logging.handlers import TimedRotatingFileHandler

log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_file = "service.log"

handler = TimedRotatingFileHandler(
    log_file, when="W0", interval=1, backupCount=4, encoding="utf-8"
)
handler.setFormatter(log_formatter)
handler.setLevel(logging.INFO)

logger = logging.getLogger("ConverterService")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
