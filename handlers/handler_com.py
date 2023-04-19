from handlers.handler import Handler
from settings import config


class HandlerCommands(Handler):
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        if message.from_user.id == config.ADMIN_ID:
            self.bot.send_message(message.chat.id,
                                  f'{message.from_user.first_name},'f' здравствуйте ! Жду дальнейших указаний.',
                                  reply_markup=self.keyboards.start_admin_menu())
        else:
            self.bot.send_message(message.chat.id,
                                  f'{message.from_user.first_name},'f' здравствуйте ! Жду дальнейших указаний.',
                                  reply_markup=self.keyboards.start_menu())

    def handle(self):
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)
