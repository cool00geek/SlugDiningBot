#!/usr/bin/env python3

import discord
#from discord.ext.commands import Bot, Greedy
#from discord import User
import os
from UCSCDining import UCSCDining
import DiningBot

token = os.environ.get('DISCORD_UCSC_KEY')

client = discord.Client()

#bot = Bot(command_prefix='!@#$%^&()')

#@bot.command()
#async def pm(ctx, users: Greedy[User], *, message):
#    for user in users:
#        await user.send(message)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith('!menu') or message.content.startswith('!search'):
        print(str(message.author) + " sent message: " + str(message.content))
        DiningBot.store_from(str(message.author), 'discord_users.txt')

    if message.content.lower().startswith('!start') or message.content.startswith('!help'):
        msg = DiningBot.help(platform="Discord", prefix="!")
        #await client.send_message(message.channel, msg)
        await message.channel.send(msg)
    elif message.content.lower().startswith('!about'):
        msg = DiningBot.about(platform="Discord")
        #await client.send_message(message.channel, msg)
        await message.channel.send(msg)
    elif message.content.lower().startswith('!menu'):
        msg = DiningBot.parse(message.content, platform="DC", prefix="!")
        if not msg:
            #await client.send_message(message.channel, "I'm not sure what college that is!")
            await message.channel.send("I'm not sure what college that is!")
        else:
            #await client.send_message(message.channel, msg)
            await message.channel.send(msg)
    elif message.content.lower().startswith('!search'):
        #msg = DiningBot.parse(message.content, platform="DC", prefix="!")
        msg = message.content
        msg_list = msg.split(" ")
        del msg_list[0]
        dining = UCSCDining()
        meal = ""
        meal_id = dining.get_desired_meal(msg_list[len(msg_list) - 1])
        print(meal_id)
        if not meal_id == -1:
            meal = msg_list[len(msg_list) - 1]
            del msg_list[len(msg_list) - 1]
        msg_str = ""
        for x in msg_list:
            msg_str += x + " "
        msg_str = msg_str[:-1]
        send_msg = DiningBot.search(msg_str, meal=meal)
        if send_msg == "":
            send_msg = "That's not being served!"
        #bot.send_message(chat_id=update.message.chat_id, text=)
        #await client.send_message(message.channel, send_msg)
        await message.channel.sendsend_msg)
    #elif message.content.startswith('!'):
    #    msg = "I don't understand that command!"
    #    await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
