import re

import discord.ext.test as dpytest


def discord_message_contains(expected: str):
    message = dpytest.get_message().content
    return expected in message


def discord_message_equals(expected: str):
    message = dpytest.get_message().content
    return expected == message


def discord_message_matches(regex: str):
    message = dpytest.get_message().content
    return re.match(regex, message)
