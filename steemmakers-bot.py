import os
import discord

# discord client
client = discord.Client()


def process_message(message):
    args = message.content.split(" ")

    return args


# create a new event
@client.event
async def on_ready():
    print()
    print("STEEMMAKERS ARE GO!")
    print("(Bot Ready)")
    servers = "\n   - ".join([s.name + " (" + s.id + ")" for s in client.servers])
    print(servers)
    channel = client.get_channel("383256479056134146")
    await client.send_message(channel, "Beep Boop Blurp! [Bot Ready]")

# listen for specific messages
@client.event
async def on_message(message):
    if message.content.startswith("/hello"):
        await client.send_message(message.channel, "BY YOUR COMMAND!")

    if message.content.startswith("/check-check"):
        await client.send_message(message.channel, ":+1: Channel = {}".format(message.channel))
        print(message.channel.id)


# welcome message
@client.event
async def on_member_join(member):
    print("** @" + member.name + " joined")

    welcome_message = member.name + """ - Welcome! :)

    Read this helpful introduction to get acquainted with the group:
    https://www.steemmakers.com/#/article/steemmakers/welcome-to-the-steemmakers-community

    """
    channel = client.get_channel("383256479056134146")
    await client.send_message(channel, welcome_message)


# run the bot
bot = os.environ['SMBOT']
client.run(bot)
