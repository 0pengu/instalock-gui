import os
import sys

import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

from requests.auth import HTTPBasicAuth
import json
import asyncio

class Files:
    def __init__(self, baseURL):
        self.baseURL = baseURL

    async def grabToken(self):
        path = f"C:/Users/{os.getlogin()}/AppData/Local/Riot Games/Riot Client/Config/lockfile"
        if os.path.isfile(path):
            with open(path, 'r') as f:
                data = f.read().split(":")
                self.dataName=data[0]
                self.pid=data[1]
                self.port=data[2]
                self.password=data[3]
                self.protocol=data[4]

            url = f"{self.baseURL}{self.port}/entitlements/v1/token"
            entitlement = requests.get(url=url, auth=HTTPBasicAuth('riot', self.password), verify=False)
            #print(f"{entitlement.json()}")
            if entitlement is not None and entitlement.status_code == 200:  
                tokenDict = json.loads(entitlement.text)
                self.puuid = tokenDict['subject']
                self.accessToken = tokenDict["accessToken"]
                self.entitlementToken = tokenDict["token"]
                return self.puuid, self.accessToken, self.entitlementToken, self.port, self.password
            else:
                print(f"\n\nConnection refused. Are you sure Valorant is running?\nExiting in 3 seconds...")
                await asyncio.sleep(3)
                sys.stdout = open(os.devnull, "w")
                sys.stderr = open(os.devnull, "w")
                sys.exit(1)
        else:
            checkPath = f"C:/Users/{os.getlogin()}/AppData/Local/Riot Games/Riot Client/Config/lockfile"
            if os.path.exists(checkPath):
                print(f"Valorant must be launched before this program is started!\nExiting in 3 seconds...")
                await asyncio.sleep(3)
                sys.stdout = open(os.devnull, "w")
                sys.stderr = open(os.devnull, "w")
                sys.exit(200)
            else:
                print(f"\n\nError: Valorant does not exist in the machine!\nExiting in 3 seconds...")
                await asyncio.sleep(3)
                sys.stdout = open(os.devnull, "w")
                sys.stderr = open(os.devnull, "w")
                sys.exit(1000)