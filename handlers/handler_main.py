from handlers.handler_com import HandlerCommands
from handlers.handler_all_text import HandlerAllText


class HandlerMain:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.handler_commands = HandlerCommands(self.bot, self.dp)
        self.handler_all_text = HandlerAllText(self.bot, self.dp)

    async def handle(self):
        await self.handler_commands.handle()
        await self.handler_all_text.handle()
