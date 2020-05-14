import logging

from json import loads
from json import dumps
from os.path import isfile
from random import choice

from discord.ext import commands, tasks
from praw import Reddit

login_data = {}
ban_list = []

client = commands.Bot(command_prefix="r/")


def collapse_list(input: list) -> str:
    output = ""
    for line in input:
        output += line
    return output


@client.command()
async def reddit(ctx: commands.Context, *, question: str) -> None:
    if ctx.channel.name not in ban_list:
        reddit = Reddit(client_id=login_data['reddit_token'],
                        client_secret=login_data['reddit_secret'],
                        username=login_data['reddit_uname'],
                        password=login_data['reddit_pword'],
                        user_agent=login_data['reddit_useragent'])
        entries = []
        for item in reddit.subreddit(question).new():
            entries.append(item)
        entry = choice(entries)
        await ctx.send(entry.url)
    else:
        await ctx.send("Reddit bot can not post to this channel")


@client.command()
async def ban_channel(ctx: commands.Context) -> None:
    if ctx.channel.name not in ban_list:
        ban_list.append(ctx.channel.name)
        file = open('./banlist.json', 'w')
        file.write(collapse_list(dumps(ban_list)))
        file.close()
        await ctx.send("This channel has been banned from the reddit bot's use")
    else:
        await ctx.send("This channel is already banned")


@client.command()
async def unban_channel(ctx: commands.Context) -> None:
    if ctx.channel.name in ban_list:
        ban_list.remove(ctx.channel.name)
        file = open('./reddit_banlist.json', 'w')
        file.write(collapse_list(dumps(ban_list)))
        file.close()
        await ctx.send("This channel has been permitted for the reddit bot's use")
    else:
        await ctx.send("This channel is already permitted")


if __name__ == "__main__":
    prawlogger = logging.getLogger('prawcore')
    prawlogger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    prawlogger.addHandler(handler)
    handler = logging.FileHandler("reddit.log")
    handler.setLevel(logging.DEBUG)
    prawlogger.addHandler(handler)

    if isfile('./reddit_login.txt'):
        file = open('./reddit_login.txt', 'r')
        login_data['discord_secret'] = str(file.readline().rstrip())
        login_data['reddit_token'] = str(file.readline().rstrip())
        login_data['reddit_secret'] = str(file.readline().rstrip())
        login_data['reddit_uname'] = str(file.readline().rstrip())
        login_data['reddit_pword'] = str(file.readline().rstrip())
        login_data['reddit_useragent'] = str(file.readline().rstrip())
        file.close()
    else:
        login_data['discord_secret'] = input("Enter your discord secret: ")
        login_data['reddit_token'] = input("Enter your reddit token")
        login_data['reddit_secret'] = input("Enter your reddit secret")
        login_data['reddit_uname'] = input("Enter your reddit uname")
        login_data['reddit_pword'] = input("Enter your reddit pword")
        login_data['reddit_useragent'] = input("Enter your reddit user agent")

    if isfile('./reddit_banlist.json'):
        file = open('./reddit_banlist.json', 'r')
        ban_list = list(loads(collapse_list(file.readlines())))
        file.close()
    else:
        file = open('./reddit_banlist.json', 'w')
        file.write(collapse_list(dumps(ban_list)))
        file.close()

    file = open('./reddit_login.txt', 'w')
    file.writelines([login_data['discord_secret'] + "\n",
                    login_data['reddit_token'] + "\n",
                    login_data['reddit_secret'] + "\n",
                    login_data['reddit_uname'] + "\n",
                    login_data['reddit_pword'] + "\n",
                    login_data['reddit_useragent'] + "\n"])
    file.close()

    client.run(login_data['discord_secret'])
