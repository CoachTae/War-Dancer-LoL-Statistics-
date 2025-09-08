import requests
import urllib.parse
import sys
from urllib.parse import quote

from api.constants import *
from api.MyInfo import *


def get_base_url(region, is_platform_specific=False):
    '''Parameters = NA, EU, OCE, ASIA'''

    if is_platform_specific:
        return f"https://{region}.api.riotgames.com"

    else:
        if region == "NA":
            return AMERICAS_URL
        elif region == "EU":
            return EUROPE_URL
        elif region == "OCE":
            return SEA_URL
        elif region == "ASIA":
            return ASIA_URL
        else:
            print("ERROR IN 'get_base_url' METHOD CALL IN 'riot_api.py'.")
            print(f"GOT {region} AS A RESPONSE WHEN EXPECTED NA, EU, OCE, OR ASIA.")
            sys.exit()
            



def get_champion_data(patch_version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{patch_version}/data/en_US/champion.json"
    response = requests.get(url)
    response.raise_for_status() # Raise an error for bad status codes
    return response.json()






def get_match_ids(puuid, region, start=0, count=20):
    '''Gets (count) most recent games from (puuid)'s match history.

        Parameters:
           puuid = Unique player ID
           region = NA, EU, OCE, ASIA
           start = index start is 0. 0 is most recent match
           count = Number of matches to return

        Returns:
            List of match IDS (platform_region included in match ID string)
            e.g. "NA1_5197758177"

        TESTED AND WORKS!!!
    '''
    BASE_URL = get_base_url(region)
    url = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()






def get_match_data(region, platform_region, match_id):
    """
    Parameters:
        region (str) = NA, EU, OCE, ASIA
        platform_region (str) = na1, br1, etc
        match_id (str) = match ID

    Returns:
        MatchDTO (dict)
    
    TESTED AND WORKS!
    """
    BASE_URL = get_base_url(region)
    if "_" in match_id:
        url = f"{BASE_URL}/lol/match/v5/matches/{match_id}"
    else:
        url = f"{BASE_URL}/lol/match/v5/matches/{platform_region.upper()}_{match_id}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()



def get_summoner_data(puuid, platform_region):
    """
    Given a puuid, retrieves encrypted ID, account ID, profile icon ID, and summoner Level.

    Parameters:
        puuid = Unique player ID
        platform_region (str) = na1, br1, etc

    return:
        SummonerDTO
    """
    url = f"https://{platform_region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_Riot_ID(puuid, region):
    """
    Fetches Riot ID (in-game ID) given a puuid. e.g. "Coach Tae#123"

    Parameters:
        puuid (str): Unique player ID
        region (str): NA, EU, OCE, ASIA

    returns:
        Riot ID (str)
    """
    BASE_URL = get_base_url(region)
    url = f"{BASE_URL}/riot/account/v1/accounts/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    Riot_ID = f'{response.json()["gameName"]}#{response.json()["tagLine"]}'
    return Riot_ID


def get_puuid(RiotID, region):
    """
    Gets puuid given a RiotID (e.g. Coach Tae#123).

    Parameters:
        puuid (str): Unique player ID
        region (str): NA, EU, OCE, ASIA

    returns:
        puuid
    """
    gameName, tag_line = RiotID.split("#")
    encoded_gameName = quote(gameName)
    encoded_tag_line = quote(tag_line)
    
    BASE_URL = get_base_url(region)
    url = f"{BASE_URL}/riot/account/v1/accounts/by-riot-id/{encoded_gameName}/{encoded_tag_line}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["puuid"]


def get_patch(matchDTO):
    fullversion = matchDTO['info']['gameVersion']
    parts = fullversion.split('.')
    return '.'.join(parts[:2])
