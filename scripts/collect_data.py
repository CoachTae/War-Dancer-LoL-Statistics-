import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import api.riot_api as API
from api.riot_api import get_match_ids, get_match_data
from api.MyInfo import MY_PUUID
from api.MyInfo import MySQL_Password


import mysql.connector
from mysql.connector import errorcode

import sql as SQL



def collect_data(puuid=None, name=None, tagline=None, region=None, platform=None):
    '''
    To manually collect data on a specific individual, give either the puuid
        or the summoner name and tagline

    FOR MANUAL USE, YOU MAY USE EITHER:
        PUUID + REGION + PLATFORM, or
        NAME + TAGLINE + REGION + PLATFORM
        

    Parameters:
        puuid = The PUUID (str) of the individual you wish to update information on
        name = The summoner name of the individual you wish to update information on
        tagline = The tagline (after the hashtag of the individual you wish to update information on
        region = Region of the user (NA, EUW, OCE, ASIA)
    '''

    # Connect to database
    conn = SQL.get_conn()
    

    # If user hasn't explicitly asked for a user to be updated, get the most stale summoner
    if puuid is None and name is None:
        summoner = SQL.get_stale_summoner(conn)
        puuid = summoner['puuid']
        platform = summoner['Platform']

    elif platform is None or region is None:
        print("To give a custom summoner update, please provide the region (NA, EU, etc) and platform (na1, br1, etc).")
        sys.exit()
    
    # If the user has given a RiotID, look that up.
    elif puuid is None and name is not None:
        if tagline is None:
            print("Please give a tagline for the summoner (characters after the #).")
            sys.exit()
        RiotID = name + "#" + tagline
        puuid = API.get_puuid(RiotID, region)
        

    # Pull that player's match history
    matches = get_match_ids(puuid, region, count=100)
        
    for match in matches:
        # We already have the platform, so just pull the matchid numbers
        _, matchid = match.split("_", 1)

        matchid = int(matchid)
        # Check if match already exists in the DB
        already_exists = SQL.match_exists(conn, platform, matchid)
        if already_exists:
            continue
        
        # Get match information
        matchid_string = platform.upper() + "_" + str(matchid)
        matchDTO = API.get_match_data(region, platform, matchid_string)


        # Get patch
        patch = API.get_patch(matchDTO)

        # Check if partition exists, if not, create it
        SQL.matches.ensure_partition(conn, patch)

        # Add in match data!

        # Add match to table
        SQL.matches.insert_match(conn, platform, matchid, patch)
        
    
    conn.close()


if __name__ == '__main__':
    collect_data(MY_PUUID, platform="na1", region="NA")
