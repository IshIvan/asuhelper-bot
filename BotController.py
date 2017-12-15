from telebot import types

from FileWorker import FileWorker


class BotController:
    FIND_BUTTON = 'Найти документ'
    HELP_BUTTON = 'Помощь'
    SHOW_BUTTON = 'Показать файлы'

    def __init__(self, bot_instance):
        self.instance = bot_instance

    def prepare_to_find(self, user_id):
        self.send(user_id, 'Внимательно слушаем. Что найти?')

    def find(self, user_id, query):
        documents = FileWorker.find(query)
        if len(documents) == 0:
            reason = 'Мы ничего не нашли по запросу "{0}" :( \nВ следующий раз будем искать лучше'.format(query)
            self.send(user_id, reason)
        elif len(documents) == 1:
            document = FileWorker.get(documents[0])
            self.document(user_id, document, 'По запросу "{0}" мы нашли только этот файл'.format(query))
        else:
            self.print_documents(user_id, documents)

    def inline_getter(self, call):
        self.find(call.message.chat.id, call.data)
        self.instance.answer_callback_query(call.id, text='Файл выбран')

    def send(self, user_id, message, keyboard=None):
        try:
            self.instance.send_message(user_id, message, reply_markup=keyboard)
        except:
            print('log')

    def document(self, user_id, document, caption=''):
        try:
            self.instance.send_document(user_id, document, caption=caption)
        except:
            print('doc log')

    def print_documents(self, user_id, document_names):
        keyboard = types.InlineKeyboardMarkup()
        for doc_name in document_names:
            button = types.InlineKeyboardButton(doc_name, callback_data=doc_name)
            keyboard.add(button)
        self.send(user_id, 'Мы нашли следующие файлы:', keyboard)

    def print_help(self, user_id):
        self.send(user_id, 'Чат разработан для поиска важных документов на кафедре АСУ')

    def start_message(self, user_id):
        self.print_help(user_id)

    def error(self, user_id):
        self.send(user_id, 'Что-то мне дурно, попробуй еще разок позже.')

    def teaser(self, user_id):
        documents = FileWorker.find('.')
        self.send(user_id, 'Хотите чего-нибудь интересненького?')
        self.print_documents(user_id, documents)

    def show_keyboard(self, user_id):
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button = types.KeyboardButton(text=self.FIND_BUTTON)
        keyboard.add(button)
        button = types.KeyboardButton(text=self.HELP_BUTTON)
        keyboard.add(button)
        button = types.KeyboardButton(text=self.SHOW_BUTTON)
        keyboard.add(button)
        self.send(user_id, 'Выберите действие', keyboard)
