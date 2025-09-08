import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import api.riot_api as API
import sql as SQL

#-------------------------------------------------------------------------------

matchDTO = API.get_match_data("NA", "na1", "5364606450")
print("INFO KEYS: ", matchDTO["info"].keys())
print(f'\n\n\nVersion: {matchDTO["info"]["gameVersion"]}')

conn = SQL.connection.get_conn()
print(API.get_patch(matchDTO))
SQL.matches.ensure_partition(conn, API.get_patch(matchDTO))
sys.exit()

PartDTO = matchDTO['info']['participants'][0]

for key in PartDTO.keys():
    print(key)
