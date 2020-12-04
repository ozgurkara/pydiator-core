from abc import ABC, abstractmethod


class BaseLogger(ABC):

    @abstractmethod
    def log(self, source: str, message: str, data: object = None):
        pass


class Logger(BaseLogger):
    def __init__(self):
        pass

    def log(self, source: str, message: str, data: object = None):
        print(f'source:{source}, message:{message}, data:{data}')


class LoggerFactory:
    @classmethod
    def get_logger(cls):
        if not hasattr(cls, "logger") or cls.logger is None:
            cls.logger = Logger()
        return cls.logger

    @classmethod
    def set_logger(cls, logger):
        cls.logger = logger
