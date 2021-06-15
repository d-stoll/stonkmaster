import discord


class DiscordContextMock:
    def __init__(self):
        self.messages = []
        self.embeds = []

    async def send(self, msg: str = None, embed: discord.Embed = None):
        if embed is not None:
            self.embeds.append(embed)

        if msg is not None:
            self.messages.append(msg)
