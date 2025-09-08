import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import api.riot_api as API
from api import MyInfo

#---------------------------------------------------------------------------------

me = API.get_puuid("Coach Tae#123", 'NA')
print(me)
