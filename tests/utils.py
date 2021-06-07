class DiscordContextMock:
    def __init__(self):
        self.messages = []

    async def send(self, msg: str):
        self.messages.append(msg)
