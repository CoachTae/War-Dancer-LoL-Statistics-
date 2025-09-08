import mysql.connector
import sys
import os


# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import api.riot_api as API
from api import MyInfo


#---------------------------------------------------------------------------------

me = API.get_puuid("Coach Tae#123", "NA")
print(me)

db = mysql.connector.connect(
    host="localhost",
    user="Tae",
    password=MySQL_Password,
    database="league_data"
    )

cursor = db.cursor()

cursor.execute("SHOW TABLES;")
for table in cursor.fetchall():
    print(table)

cursor.close()
db.close()
    
#MySummoner = API.get_summoner_by_puuid("NA", f"{MY_PUUID}")
#print(f"{MySummoner['gameName']}#{MySummoner['tagLine']}")
