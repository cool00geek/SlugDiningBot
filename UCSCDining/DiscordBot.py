#!/usr/bin/env python3

import discord
import os
from UCSCDining import UCSCDining
import DiningBot

token = os.environ.get('DISCORD_UCSC_KEY')

client = discord.Client()

def parse(msg):
    msg_list = msg.split(" ")
    if msg_list[0].lower() == "!menu":
        del msg_list[0]
    dining = UCSCDining()
    if dining.verify_name(msg_list[0]):
        college_name = dining.get_college_name(msg_list[0])
        meal_name = msg_list[len(msg_list)-1]
        text = DiningBot.get_menu(dining, college_name, meal=meal_name)
    else:
        print("DC-err: " + msg)
        text="Sorry, I don't know what college that is!"
    return text

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!start') or message.content.startswith('!help'):
        msg = DiningBot.help(platform="Discord", prefix="!")
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!about'):
        msg = DiningBot.about(platform="Discord")
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!menu'):
        msg = parse(message.content)
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!'):
        msg = "I don't understand that command!"
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
