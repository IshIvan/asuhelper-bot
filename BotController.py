from telebot import types

from Logger import Logger
from FileWorker import FileWorker


class BotController:
    FIND_BUTTON = 'Найти документ'
    HELP_BUTTON = 'Помощь'
    SHOW_BUTTON = 'Показать файлы'

    def __init__(self, bot_instance):
        self.instance = bot_instance

    def prepare_to_find(self, user_id):
        """
        Оповщение, что бот готов принять текстовый запрос.
        :param user_id:
        :return:
        """
        self.send(user_id, 'Внимательно слушаем. Что найти?')

    def find(self, user_id, query):
        """
        Ищем документ по названию.
        Если документ один, то даем его скачать.
        Если более - выводим текстом.
        Если ни одного, говорим об этом.
        :param user_id: от конкретного пользоватлея
        :param query: строка поиска
        :return:
        """
        documents = FileWorker.find(query)
        if len(documents) == 0:
            reason = 'Мы ничего не нашли по запросу "{0}" :( \nВ следующий раз будем искать лучше'.format(query)
            self.send(user_id, reason)
        elif len(documents) == 1:
            try:
                document = FileWorker.get(documents[0])
                self.document(user_id, document, 'По запросу "{0}" мы нашли только этот файл'.format(query))
            except:
                Logger.warning('file is not exist {0}'.format(query))
        else:
            self.print_documents(user_id, documents)

    def inline_getter(self, call):
        """
        Человек нажал на кнопку с файлом.
        :param call:
        :return:
        """
        self.find(call.message.chat.id, call.data)
        self.instance.answer_callback_query(call.id, text='Файл выбран')

    def send(self, user_id, message, keyboard=None):
        """
        Отправялем сообщение пользователю, при этом ждем ошибки в различных вариантах.
        :param user_id:
        :param message:
        :param keyboard:
        :return:
        """
        try:
            self.instance.send_message(user_id, message, reply_markup=keyboard)
        except:
            Logger.error('cant send message to {0}'.format(user_id))

    def document(self, user_id, document, caption=''):
        """
        Отправляем человеку документ, ожидая ошибочек.
        :param user_id:
        :param document:
        :param caption:
        :return:
        """
        try:
            self.instance.send_document(user_id, document, caption=caption)
        except:
            Logger.error('cant send documents to {0}'.format(user_id))

    def print_documents(self, user_id, document_names):
        """
        Показываем инлайн клавиатуру с выбором файлов.
        Колбеком будет служить полное название файлла.
        :param user_id:
        :param document_names:
        :return:
        """
        keyboard = types.InlineKeyboardMarkup()
        for doc_name in document_names:
            button = types.InlineKeyboardButton(doc_name, callback_data=doc_name)
            keyboard.add(button)
        self.send(user_id, 'Мы нашли следующие файлы:', keyboard)

    def print_help(self, user_id):
        """
        Печатаем текст для помощи пользователю.
        Компанда /help.
        :param user_id:
        :return:
        """
        self.send(user_id, 'Чат разработан для поиска важных документов на кафедре АСУ')

    def start_message(self, user_id):
        """
        Человек первый раз вошел в чат.
        Печатаем ему приветственный текст.
        :param user_id:
        :return:
        """
        self.print_help(user_id)

    def error(self, user_id):
        """
        Произошла ошибка.
        :param user_id:
        :return:
        """
        self.send(user_id, 'Что-то мне дурно, попробуй еще разок позже.')
        Logger.error('query len > 20')

    def teaser(self, user_id):
        """
        Человек ввел "Показать все файлы".
        Сообщаем ему об этом.
        Ждем текста.
        :param user_id:
        :return:
        """
        documents = FileWorker.find('.')
        self.send(user_id, 'Хотите чего-нибудь интересненького?')
        self.print_documents(user_id, documents)

    def show_keyboard(self, user_id):
        """
        Показываем основное меню в обычной клавиатуре.
        :param user_id:
        :return:
        """
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button = types.KeyboardButton(text=self.FIND_BUTTON)
        keyboard.add(button)
        button = types.KeyboardButton(text=self.HELP_BUTTON)
        keyboard.add(button)
        button = types.KeyboardButton(text=self.SHOW_BUTTON)
        keyboard.add(button)
        self.send(user_id, 'Выберите действие', keyboard)
