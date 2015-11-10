"""
Logger is a class to manage log output and format so that we
don't have to pass loggers into methods or classes in order
to get the desired results.
"""

import logging

class Logger(object):
    """
    Logger class that is a little messy and requires you to run
    configure() before using any of the other methods. Not in love
    with this setup but it allow me to not pepper logging throughout
    the application and have to pass it down 3 levels to get it to the
    proper class.
    """
    logger = ""

    @classmethod
    def configure(cls):
        """
        Create configuration for logger and change
        the default format that it uses.
        """
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger_handler = logging.StreamHandler()
        logger.addHandler(logger_handler)
        logger_handler.setFormatter(logging.Formatter('%(message)s'))
        cls.logger = logger

    @classmethod
    def info(cls, string, *opts):
        """
        Print info out to screen
        """
        cls.logger.info(string, *opts)
