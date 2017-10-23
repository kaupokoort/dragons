import logging


class Logging:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    # create logger for dragonsofmugloar
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler('battle.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)


class TerminalFontColors:
    BOLD = '\033[1m'
    BLUE = '\033[34m'
    ERROR = '\033[91m'
    GREEN = '\033[92m'
    GREY = '\033[90m'
    QUESTION = '\033[98m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    WHITE = '\033[97m'

