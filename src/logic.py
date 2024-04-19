import requests

class Logic:
    def __init__(self, onlineURL, puuid, aT, eT):
        self.url = onlineURL
        self.puuid = puuid
        self.aT = aT
        self.eT = eT

    async def getPreMatchID(self):
        self.getPreGamePlayerURL = f"{self.url}/pregame/v1/players/{self.puuid}"
        sessions = requests.get(url = self.getPreGamePlayerURL, headers = {"X-Riot-Entitlements-JWT": f"{self.eT}", "Authorization": f"Bearer {self.aT}"})
        sessions_data = sessions.json()
        print(sessions_data)
        self.prematchID = sessions_data['MatchID']
        await self.hoverRaze()

    async def hoverRaze(self): # Jett now
        self.selectCharURL = f"{self.url}/pregame/v1/matches/{self.prematchID}/select/add6443a-41bd-e414-f6ad-e58d267f4e95"
        sessions = requests.post(url = self.selectCharURL, headers = {"X-Riot-Entitlements-JWT": f"{self.eT}", "Authorization": f"Bearer {self.aT}"})
        sessions_data = sessions.json()
        print(sessions_data)


