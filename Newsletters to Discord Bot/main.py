# -*- coding: utf-8 -*-

import new_email_checker as nec
import constants as cs

import discord
import asyncio
import datetime

client = discord.Client()

@client.event
async def on_ready():
    print('Bot is logging as ({0.user.name}, {0.user.id})'.format(client))
    
@client.event
async def look_for_email_news():
   await client.wait_until_ready()
   while(True):
      mailbox = nec.mail_connexion()
      txt = nec.mail_get_newswletter_text(mailbox)
      if len(txt) > 0:
          await client.get_channel(cs.channel_id).send(txt)
      print("time = " + str(datetime.datetime.now()), end = "\r")
      mailbox.logout()
      await asyncio.sleep(cs.time_sleep)

client.loop.create_task(look_for_email_news())                
client.run(cs.token)