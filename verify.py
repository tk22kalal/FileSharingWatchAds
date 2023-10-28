import os
import string
import random
import pytz
from datetime import date
import requests as re

SHORTNER = os.environ.get("SHORTENER_SITE")
API = os.environ.get("SHORTENER_API")

async def get_shortlink(verification_link):
    res = re.get(f'https://{SHORTNER}/api?api={API}&url={verification_link}')
    res.raise_for_status()
    data = res.json()
    return data.get('shortenedUrl')

async def generate_random_string(num: int):
    if num == 28:
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(num))
        return random_string
    else:
        raise ValueError("The 'num' parameter must be 28 for generating a 28-character string.")

TOKENS = {}
VERIFIED = {}

# A dictionary to store user tokens and their usage status
TOKENS = {}

async def check_token(bot, userid, token):
    # Ensure the user exists
    user = await bot.get_users(userid)
    
    # Check if the user's ID is in the TOKENS dictionary
    if user.id in TOKENS:
        # Get the user's token dictionary
        user_tokens = TOKENS[user.id]
        
        # Check if the provided token exists for the user
        if token in user_tokens:
            # Check if the token has been used (True) or not (False)
            is_used = user_tokens[token]
            
            # Return True if the token is valid and not used, otherwise return False
            return not is_used
    
    # If the user or token doesn't exist, return False
    return False

async def get_token(bot, userid, link):
    # Ensure the user exists
    user = await bot.get_users(userid)
    
    # Generate a random 7-character token
    token = await generate_random_string(28)
    
    # Store the token in the TOKENS dictionary for the user with the "used" status set to False
    if user.id in TOKENS:
        TOKENS[user.id][token] = False
    else:
        TOKENS[user.id] = {token: False}
    
    # Create a verification link with user ID and token
    verification_link = f"{link}{token}"
    
    # Shorten the verification link
    shortened_verify_url = await get_shortlink(verification_link)
    
    # Return the shortened verification link
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
