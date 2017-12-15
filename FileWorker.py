import os


class FileWorker:
    @staticmethod
    def find(query):
        document_names = []
        documents = [x.lower() for x in os.listdir('./documents')[:10]]
        for document_name in documents:
            if document_name.find(query.lower()) != -1:
                document_names.append(document_name)

        return document_names

    @staticmethod
    def get(name):
        return open('./documents/' + name, 'rb')
