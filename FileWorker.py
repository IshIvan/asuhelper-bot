import os

from Logger import Logger


class FileWorker:
    @staticmethod
    def find(query):
        """
        Ищем файлы по текстовой строке.
        :param query:
        :return:
        """
        Logger.info('find {0}'.format(query))
        document_names = []
        documents = [x.lower() for x in os.listdir('./documents')[:10]]
        for document_name in documents:
            if document_name.find(query.lower()) != -1:
                document_names.append(document_name)

        return document_names

    @staticmethod
    def get(name):
        """
        Получаем файл по точному названию.
        :param name:
        :return:
        """
        return open('./documents/' + name, 'rb')
