from config import *
import requests


# Deny Byrchak @ 1/3/2025 2:24 AM
# script provides with ger_summoner_history_data function that returns list of dicts

def get_summoner(summoner_name):
    url = f"{BASE_URL}/riot/account/v1/accounts/by-riot-id/{summoner_name}"
    headers = {"X-Riot-Token": RIOT_DEVELOPMENT_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_match_list(puuid, count=5):
    url = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {"X-Riot-Token": RIOT_DEVELOPMENT_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_match_data(match_id):
    url = f"{BASE_URL}/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": RIOT_DEVELOPMENT_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to get match data for {match_id}: {response.status_code}")
        return []

    match_data = response.json()

    player_data = [
        {
            "summonerName": participant['summonerName'],
            "championName": participant['championName'],
            "win": participant['win']
        }
        for participant in match_data['info']['participants']
        if participant['summonerName'] in players
    ]
    return player_data


def get_summoner_history_data(summoner_name="MidOrFeed/Zoe"):
    summoner_data = get_summoner(summoner_name)
    puuid = summoner_data.get("puuid")

    if puuid:
        match_ids = get_match_list(puuid)

        for match_id in match_ids:
            match_data = get_match_data(match_id)
            for item in match_data:
                print(item)

            print()
