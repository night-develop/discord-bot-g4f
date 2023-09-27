import logging


def logger_factory(
    logger_name: str,
    log_level: int,
    file_name: str,
    log_format: str
) -> logging.Logger:
    """Функция получения логера

    Args:
        logger_name (str): имя логера
        log_level (int): уровень логирования
        file_name (str): имя фалйа лога
        log_format (str): формат логов

    Returns:
        logging.Logger: _description_
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    formatter = logging.Formatter(log_format)
    
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger