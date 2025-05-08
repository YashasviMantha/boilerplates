import logging

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    light_blue = "\x1b[1;36m"
    blue = "\x1b[1;34m"
    green = "\x1b[1;32m"
    purple = "\x1b[1;35m"

    format = "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: purple + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_module_logger(mod_name, log_level="default"):
    """
    To use this,
        logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    # formatter = logging.Formatter(
    #     '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    # handler.setFormatter(formatter)
    if (
        sum([isinstance(handler, logging.StreamHandler) for handler in logger.handlers])
        == 0
    ):
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)
    log_level_mapping = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "crital": logging.CRITICAL,
        "default": logging.WARNING,
    }
    logger.setLevel(log_level_mapping.get(log_level))
    return logger
