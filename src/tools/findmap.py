from requests import get
from json import dumps

MapDict = {
    '/Game/Maps/Ascent/Ascent':'Ascent',
    '/Game/Maps/Port/Port':'Icebox',
    '/Game/Maps/Duality/Duality':'Bind',
    "/Game/Maps/Foxtrot/Foxtrot":'Breeze',
    "/Game/Maps/Canyon/Canyon":'Fracture',
    "/Game/Maps/Triad/Triad":'Haven',
    "/Game/Maps/Jam/Jam":'Lotus',
    "/Game/Maps/Pitt/Pitt":'Pearl',
    "/Game/Maps/Bonsai/Bonsai":'Split',
    "/Game/Maps/Juliett/Juliett":'Sunset',
    'HURM':'TDM Map'
    }

def findMap(URL, matchID, eT, aT):
    preGame = get(url = f"{URL}/{matchID}", headers = {"X-Riot-Entitlements-JWT": f"{eT}", "Authorization": f"Bearer {aT}"})
    preGame_data = preGame.json()
    for filepath, mapname in MapDict.items():
        if preGame_data['MapID'] in filepath:
            return mapname
    return f"Error: Map cannot be found. Mapfile: {preGame_data['MapID']}"
