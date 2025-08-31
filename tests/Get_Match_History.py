import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import api.riot_api as API
from api import MyInfo

#---------------------------------------------------------------------------------

match_ids = API.get_match_ids(MyInfo.MY_PUUID, "NA", start=0, count=20)
print(match_ids)
