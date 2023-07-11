import requests
from urllib.parse import urlparse

from .logger import logger
from .models import Account, Follower

def follower_from_actor(actor, account):
    response = requests.get(actor+".json")

    if response.status_code >= 400 and response.status_code < 600:
        logger.error('actor json request error')
        raise Exception('actor json request error')
    jsn = response.json()

    if 'id' not in jsn or 'preferredUsername' not in jsn or 'inbox' not in jsn:
        raise Exception('json error')
    
    domain = urlparse(actor).netloc
    logger.info('domain: '+domain + 'id: '+jsn['id']+'name: '+jsn['preferredUsername']+'inbox: '+jsn['inbox'])
    return Follower.objects.get_or_create(ap_id=jsn['id'], domain=domain, name=jsn['preferredUsername'], inbox=jsn['inbox'])[0]

def follow(account, actor):
    follower = follower_from_actor(actor, account)
    logger.info('searching follower result: '+str(follower))

    follower.followings.add(account) if follower else None
    return follower if follower else None

def unfollow(account, actor):
    unfollower = follower_from_actor(actor, account)
    unfollower.followings.remove(account) if unfollower else None
    return unfollower if unfollower else None
