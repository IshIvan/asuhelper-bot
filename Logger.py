import logging

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO, filename=u'my_log.log')
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'error.log')


class Logger:
    @staticmethod
    def warning(message):
        """
        Кидаем предупреждение
        :param message:
        :return:
        """
        logging.warning(message)

    @staticmethod
    def error(message):
        """
        Кидаем ошибку
        :param message:
        :return:
        """
        logging.error(message)

    @staticmethod
    def info(message):
        """
        Информативное сообщение
        :param message:
        :return:
        """
        logging.info(message)
