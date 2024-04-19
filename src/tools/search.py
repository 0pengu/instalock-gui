from os import path, getlogin

from requests import get, packages
packages.urllib3.disable_warnings(packages.urllib3.exceptions.InsecureRequestWarning)

from requests.auth import HTTPBasicAuth
from json import loads

def grabToken(baseURL):
    Path = f"C:/Users/{getlogin()}/AppData/Local/Riot Games/Riot Client/Config/lockfile"
    if path.isfile(Path):
        with open(Path, 'r') as f:
            data = f.read().split(":")
            dataName=data[0]
            pid=data[1]
            port=data[2]
            password=data[3]
            protocol=data[4]

        url = f"{baseURL}{port}/entitlements/v1/token"
        entitlement = get(url=url, auth=HTTPBasicAuth('riot', password), verify=False)
        #print(f"{entitlement.json()}")
        if entitlement is not None and entitlement.status_code == 200:
            returnDict = {}
            tokenDict = loads(entitlement.text)
            print(tokenDict)
            returnDict['puuid'] = tokenDict['subject']
            returnDict['aT'] = tokenDict["accessToken"]
            returnDict['eT'] = tokenDict["token"]
            returnDict['port'] = port
            returnDict['pw'] = password
            return True, returnDict
        else:
            return False, 2
    else:
        return False, 0