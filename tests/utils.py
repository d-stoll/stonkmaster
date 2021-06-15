import discord
from typing import List


class DiscordContextMock:
    def __init__(self):
        self.messages: List[str] = []
        self.embeds: List[discord.Embed] = []

    async def send(self, msg: str = None, embed: discord.Embed = None):
        if embed is not None:
            self.embeds.append(embed)

        if msg is not None:
            self.messages.append(msg)
