from random import choice
from json import dumps, loads
from os.path import isfile

from youtube_api import YouTubeDataAPI
from discord.ext import commands, tasks

client = commands.Bot(command_prefix="youtube ")

login_details = {}
ban_list = []


def collapse_list(input: list) -> str:
    output = ""
    for line in input:
        output += line
    return output


def translate_to_url(search_result: dict) -> str:
    return "https://www.youtube.com/watch?v=" + search_result['video_id']


@client.command()
async def search(ctx: commands.Context, *, question: str) -> None:
    if ctx.channel.name not in ban_list:
        yt = YouTubeDataAPI(login_details['youtube_api'])
        await ctx.send(translate_to_url(choice(yt.search(question))))


@client.command()
async def ban_channel(ctx: commands.Context) -> None:
    if ctx.channel.name not in ban_list:
        ban_list.append(ctx.channel.name)
        open('./youtube_banlist.json', 'w').write(
            collapse_list(dumps(ban_list)))
        await ctx.send(
            "This channel has been banned from the reddit bot's use"
        )
    else:
        await ctx.send("This channel is already banned")


@client.command()
async def unban_channel(ctx: commands.Context) -> None:
    if ctx.channel.name in ban_list:
        ban_list.remove(ctx.channel.name)
        open('./youtube_banlist.json', 'w').write(collapse_list(dumps(
            ban_list)))
        await ctx.send(
            "This channel has been permitted for the reddit bot's use"
        )
    else:
        await ctx.send("This channel is already permitted")


if __name__ == '__main__':
    if isfile('./youtube_login.txt'):
        file = open('./youtube_login.txt', 'r')
        login_details['discord_secret'] = file.readline().rstrip()
        login_details['youtube_api'] = file.readline().rstrip()
        file.close()
    else:
        login_details['discord_secret'] = input(
            "Enter your discord bot secret: ")
        login_details['youtube_api'] = input("Enter your youtube api key: ")

    if isfile('./youtube_banlist.json'):
        file = open('./youtube_banlist.json', 'r')
        ban_list = list(loads(collapse_list(file.readlines())))
        file.close()
    else:
        file = open('./youtube_banlist.json', 'w')
        file.write(collapse_list(dumps(ban_list)))
        file.close()

    file = open('./youtube_login.txt', 'w')
    file.writelines([login_details['discord_secret'] + "\n",
                    login_details['youtube_api'] + "\n"])
    file.close()

    client.run(login_details['discord_secret'])