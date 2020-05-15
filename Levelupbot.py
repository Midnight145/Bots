from getpass import getpass
from discord import Message
from json import dumps, loads
from discord.ext.commands import Bot, Context

client = Bot(command_prefix="!")

exp_dictionary = {}
level_dictionary = {}


@client.event
async def on_message(message: Message):
    if message.author != client.user:
        context = await client.get_context(message)

        if message.author in exp_dictionary.keys():
            exp_dictionary[message.author] += 10
        else:
            exp_dictionary[message.author] = 10

        for user in exp_dictionary:
            if exp_dictionary[user] >= 100:
                if user in level_dictionary.keys():
                    level_dictionary[user] += 1
                else:
                    level_dictionary[user] = 1

                await context.send("You leveled up!")


client.run(getpass("What is your discord secret: "))