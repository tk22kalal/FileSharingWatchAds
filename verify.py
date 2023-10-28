import os
import string
import random
import pytz
from datetime import date
import requests as re

SHORTNER = os.environ.get("SHORTENER_SITE")
API = os.environ.get("SHORTENER_API")

async def get_shortlink(link):
    res = re.get(f'https://{SHORTNER}/api?api={API}&url={link}')
    res.raise_for_status()
    data = res.json()
    return data.get('shortenedUrl')

TOKENS = {}
VERIFIED = {}


async def generate_random_string(num: int):
    if num == 28:
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(num))
        return random_string
    else:
        raise ValueError("The 'num' parameter must be 28 for generating a 28-character string.")

async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    if user.id in TOKENS.keys():
        TKN = TOKENS[user.id]
        if token in TKN.keys():
            is_used = TKN[token]
            if is_used == True:
                return False
            else:
                return True
    else:
        return False


async def get_token(bot, userid, link):
    user = await bot.get_users(userid)
    token = await generate_random_string(28)
    TOKENS[user.id] = {token: False}
    link = f"{link}{token}"
    shortened_verify_url = await get_shortlink(link)
    return str(shortened_verify_url)

async def verify_user(bot, userid, token):
    user = await bot.get_users(userid)
    TOKENS[user.id] = {token: True}
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    VERIFIED[user.id] = str(today)

async def check_verification(bot, userid):
    user = await bot.get_users(userid)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    if user.id in VERIFIED.keys():
        EXP = VERIFIED[user.id]
        years, month, day = EXP.split('-')
        comp = date(int(years), int(month), int(day))
        if comp < today:
            return False
        else:
            return True
    else:
        return False
