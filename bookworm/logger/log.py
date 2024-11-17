import os.path

import loguru

from bookworm.settings import BASE_DIR


def set_logger(file_path: str, level: str, rotation: str, compression: str):
    log = loguru.logger
    log.add(file_path, level=level, rotation=rotation, compression=compression)
    return log


logger = set_logger(
    os.path.join(BASE_DIR, 'logger', 'backup', 'bookworm.log'),
    level="ERROR",
    rotation="300 MB",
    compression="zip",
)
