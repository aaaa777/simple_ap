import requests
import json
from urllib.parse import urlparse
from httpsig import HeaderSigner
from datetime import datetime
import hashlib
import base64

from .logger import logger

def sign_headers(account, method, path, headers={}):
    # create http signature
    sign = HeaderSigner(
        account.ap_id()+"#main-key",
        account.private_key,
        algorithm='rsa-sha256',
        headers=['(request-target)', 'host', 'date', 'accept', 'digest']
    ).sign(
        headers,
        method=method,
        path=path
    )
    print(sign)
    auth = sign['authorization']
    # auth = sign.auth('authorization')
    sign['Signature'] = auth[len('Signature '):] if auth.startswith('Signature ') else ''
    return sign

def post_accept(account, target, activity):
    to = target.inbox
    jsn = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'type': 'Accept',
        'actor': account.ap_id(),
        'object': activity,
    }
    logger.debug('post accept: '+str(jsn))
    try:
        logger.debug('post digest:' + base64.b64encode(hashlib.sha256(json.dumps(jsn).encode()).digest()).decode())
    except Exception as e:
        logger.debug('post digest error: '+str(e))
        throw(e)


    headers = {
        'Host': urlparse(to).netloc,
        'Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'),
        'Accept': 'application/activity+json, application/ld+json',
        'Digest': 'SHA-256='+base64.b64encode(hashlib.sha256(json.dumps(jsn).encode()).digest()).decode(),
    }
    
    headers = sign_headers(account, method='POST', path=urlparse(to).path, headers=headers)
    logger.debug('post accept headers: '+str(headers))
    
    response = requests.post(to, json=jsn, headers=headers)
    logger.debug('post accept response: '+str(response.status_code) + "" + response.text)
    if response.status_code >= 400 and response.status_code < 600:
        raise Exception('accept post error')
