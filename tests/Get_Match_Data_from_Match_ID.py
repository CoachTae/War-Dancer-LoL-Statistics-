import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import api.riot_api as API

#-------------------------------------------------------------------------------

match_data = API.get_match_data("NA", "na1", "5282963377")
print("INFO KEYS: ", match_data["info"].keys())
print(f'\n\n\nVersion: {match_data["info"]["gameVersion"]}')
