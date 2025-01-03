from api.riot_api import get_match_ids, get_match_data
from data.storage import save_to_csv

def collect_and_save_matches(puuid, region, patch_version, output_file):
    match_ids = get_match_ids(puuid, region)
    match_data = [get_match_data(match_id) for match_id in match_ids]
    save_to_csv(match_data, output_file)

if __name__ == "__main__":
    PUUID = "my puuid"
    REGION = "na1"
    PATCH_VERSION = "14.24"
    OUTPUT_FILE = f"matches_{PATCH_VERSION}.csv"

    collect_and_save_matches(PUUID, REGION, PATCH_VERSION, OUTPUT_FILE)
    print(f"Data saved to {OUTPUT_FILE}")
