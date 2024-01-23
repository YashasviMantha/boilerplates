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
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
def get_module_logger(mod_name):
    """
    To use this,
        logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    # formatter = logging.Formatter(
    #     '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    # handler.setFormatter(formatter)
    # print(len(logger.handlers))
    
    # check if there is a handeler already present. If not then add. Fixes multiple logging of the same message in context of streamlit stuff. 
    if (sum([isinstance(handler, logging.StreamHandler) for handler in logger.handlers]) == 0):
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
