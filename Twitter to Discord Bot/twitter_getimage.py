# -*- coding: utf-8 -*-

import tweepy as tw
import datetime as dt
import constants as cs
import os
import urllib

def twitter_check_new_images(tw_api):
    """
    Vérifie l'existence de nouveaux posts twitters

    Parameters
    ----------
    tw_api : tweepy.API
        API twitter utilisée

    Returns
    -------
    L : TYPE
        DESCRIPTION.

    """
    user = tw_api.get_user("dailyspheal")
    L = []
    end_date = dt.datetime.utcnow() - dt.timedelta(days = 30)
    for tweet in tw.Cursor(tw_api.user_timeline, id = user.id_str).items():
      if hasattr(tweet, "entities") and 'media' in tweet.entities:
          for image in tweet.entities['media']:
              L.append(image["media_url_https"])
      if tweet.created_at < end_date:
        break
    return L
    
def store_new_images(L):
    """
    Sauvegarde sous de nouveaux fichiers les nouveaux posts

    Parameters
    ----------
    L : Liste de string
        liste de liens url des derniers posts.

    Returns
    -------
    L : Liste de string
        liste des nouveaux fichiers sauvegardés en local.

    """
    n = len(L)
    for i in reversed(range(n)):
        filename = os.path.basename(L[i])
        filepath = os.path.join(cs.save_image_path, filename)
        if not os.path.exists(filepath):
            urllib.request.urlretrieve(L[i], filepath)
            L[i] = filepath
        else:
            del L[i]
    return L