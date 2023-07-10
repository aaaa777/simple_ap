import logging, sys
logging.basicConfig(
                    stream = sys.stdout, 
                    filemode = "w",
                    level = logging.INFO)

class TeeLogging(object):
    def __init__(self, logger):
        self.logger = logger

    def info(self, message):
        self.logger.info(message)
        print(message)

    def debug(self, message):
        self.logger.debug(message)
        print(message)

    def warning(self, message):
        self.logger.warning(message)
        print(message)

    def error(self, message):
        self.logger.error(message)
        print(message)

logger = TeeLogging(logger=logging.getLogger('activitypub'))