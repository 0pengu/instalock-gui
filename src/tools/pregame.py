from requests import get

def checkGame(URL, puuid, eT, aT):
    getPreGamePlayerURL = f"{URL}/pregame/v1/players/{puuid}"
    sessions = get(url = getPreGamePlayerURL, headers = {"X-Riot-Entitlements-JWT": f"{eT}", "Authorization": f"Bearer {aT}"})
    sessions_data = sessions.json()
    print(sessions_data)
    return sessions_data