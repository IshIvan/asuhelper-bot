import telebot

from BotController import BotController
from ChatListener import ChatListener
from config import token

bot = telebot.TeleBot(token)
controller = BotController(bot)
listener = ChatListener(controller)


@bot.message_handler(content_types=["text"])
def chat_listener(message):
    """
    Декорируем бота слушать текст из нашего чата.
    :param message:
    :return:
    """
    listener.listen(message)


@bot.callback_query_handler(func=lambda call: len(call.data) > 0)
def inline_listener(call):
    """
    Декорируем бота слушать инлайн кнопки.
    :param call:
    :return:
    """
    controller.inline_getter(call)


if __name__ == '__main__':
    bot.polling(none_stop=True)
