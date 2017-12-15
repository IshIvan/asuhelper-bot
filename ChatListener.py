class ChatListener:

    def __init__(self, sender):
        self.bot = sender

    @property
    def _commands(self):
        return {
            '/menu': self.bot.show_keyboard,
            '/help': self.bot.print_help,
            '/show': self.bot.teaser,
            self.bot.SHOW_BUTTON: self.bot.teaser,
            self.bot.HELP_BUTTON: self.bot.print_help,
            self.bot.FIND_BUTTON: self.bot.prepare_to_find,
            '/find': self.bot.prepare_to_find,
            '/start': self.bot.start_message
        }

    def listen(self, message):
        user_id = message.chat.id
        if len(message.text) > 20:
            self.bot.error(user_id)
            return

        command = self._commands.get(message.text, None)
        if not command:
            self._find(message)
        else:
            command(user_id)

    def _find(self, message):
        self.bot.find(message.chat.id, message.text)
