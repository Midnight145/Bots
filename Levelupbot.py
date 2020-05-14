from getpass import getpass
from discord.ext.commands import Bot, Context

client = Bot(command_prefix="!")


@client.command()
async def testCommand(ctx: Context, *, question: str):
    await ctx.send(question)


client.run(getpass("What is your discord secret: "))