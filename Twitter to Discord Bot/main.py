# -*- coding: utf-8 -*-

import tweepy as tw
import constants as cs
import twitter_getimage as tg
import datetime as dt
import discord
import asyncio
import os

## Authentification à twitter
auth = tw.OAuthHandler(cs.consumer_key, cs.consumer_secret)
auth.set_access_token(cs.access_token, cs.access_token_secret)
tw_api = tw.API(auth)
print("Logged into Twitter !")

client = discord.Client()

@client.event
async def on_ready():
    print('Bot is logging as ({0.user.name}, {0.user.id})'.format(client))
    
@client.event
async def search_twitter_news():
    """
    Boucle infinie qui effectue la vérification de tweets nouveaux, la sauvegarde
    des images contenues dans ces tweets, et leur envoi dans une conversation discord
    
    Returns
    -------
    None.
    
    """
    await client.wait_until_ready()
    ch_id = client.get_channel(cs.channel_id)
    while(True):
       L = tg.twitter_check_new_images(tw_api)
       L = tg.store_new_images(L)
       for l in L:
           print("Send File " + os.path.basename(l))
           await ch_id.send(file=discord.File(l))
       print('time = ' + str(dt.datetime.now()), end = "\r")
       await asyncio.sleep(cs.time_sleep)

client.loop.create_task(search_twitter_news())                
client.run(cs.token)
client.get_channel()