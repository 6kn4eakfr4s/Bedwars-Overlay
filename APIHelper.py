import requests

hypixelAPIKey1 = ""


class APIhelper:
    hypixelEndpoint = "https://api.hypixel.net/v2/player"
    mojangEndpoint = "https://api.mojang.com/users/profiles/minecraft/"
    hypixelStatusEndpoint = "https://api.hypixel.net/v2/status"
    hypixelAPIKey1 = ""
    @staticmethod
    def statsFromUUID(uuid: str, name: str, APIKey):
        params = {
            "key": APIKey,
            "uuid" : uuid
        }
        #start = time.time()
        data = requests.get(url=APIhelper.hypixelEndpoint, params=params).json()
        if data['success'] == False:
            raise Exception(data['cause'])
        if data['player'] == None:
            raise Exception('Player doesn\'t exist in Hypixel')
        if'playername' not in data['player']:
            raise Exception('Player name not found in Hypixel')
        if data['player']['playername'] != name.lower():
            raise Exception('Player name doesn\'t match, is it a Nick?')
        if 'stats' not in data['player']:
            raise Exception('Player has not stats in Hypixel')
        if 'achievements' not in data['player']:
            raise Exception('Player doesn\'t have achievements in Hypixel')
        if 'Bedwars' not in data['player']['stats']:
            raise Exception('Player doesn\'t have Bedwars stats')
        if 'final_kills_bedwars' in data['player']['stats']['Bedwars'] and 'final_deaths_bedwars' in data['player']['stats']['Bedwars']:
            FKDR = round(float(data['player']['stats']['Bedwars']['final_kills_bedwars'] / data['player']['stats']['Bedwars']['final_deaths_bedwars']),2)
        else:
            FKDR = 0
        if 'bedwars_level' in data['player']['achievements']:
            Star = data['player']['achievements']['bedwars_level']
        else:
            Star = 0
        if 'winstreak' in data['player']['stats']['Bedwars']:
            WS = data['player']['stats']['Bedwars']['winstreak']
        else:
            WS = -1
        playerStats = [
            data['player']['displayname'],
            Star,
            FKDR,
            WS
        ]
        return playerStats

    @staticmethod
    def nameToUUID(playerIGN: str):
        data = requests.get(url= APIhelper.mojangEndpoint+playerIGN).json()
        #print(data)
        if 'errorMessage' in data:
            raise Exception(data['errorMessage'])
        return data

    @staticmethod
    def statusGetter(uuid: str, APIKey):
        params = {
            "key": APIKey,
            "uuid": uuid
        }
        try:
            data = requests.get(url=APIhelper.hypixelStatusEndpoint, params=params).json()
        except Exception as e:
            raise e

        result = [data['session']['online']]
        """
        if result[0]:
            result.append(data['session']['gameType'])
            result.append(data['session']['mode'])
            if result[2] != 'LOBBY':
                result.append(data['session']['map'])
            else:
                result.append('')
        else:
            result.append('')
            result.append('')
        """
        return result
    @staticmethod
    def query(ign: str, APIKey):
        try:
            uuidQuery = APIhelper.nameToUUID(ign)

        except Exception as e:
            raise Exception(e)
        uuid = uuidQuery['id']
        name = uuidQuery['name']
        #print(uuid)
        #print(name)

        result = [name]
        stats = APIhelper.statsFromUUID(uuid, name, APIKey)
        #print(stats)
        for i in stats:
            result.append(i)
        status = APIhelper.statusGetter(uuid, APIKey)
        #print(status)
        for i in status:
            result.append(i)
        #print(result)
        return result

    @staticmethod
    def rawStats(IGN: str, APIKey):
        try:
            uuid = APIhelper.nameToUUID(IGN)
        except Exception as e:
            raise e
        params = {
            "key": APIKey,
            "uuid": uuid['id']
        }
        data = requests.get(url = APIhelper.hypixelEndpoint,params=params).json()
        if data['success'] == False:
            raise Exception(data['cause'])
        #print(data)
        return data
    @staticmethod
    def rawStatus(IGN: str, APIKey):
        try:
            uuid = APIhelper.nameToUUID(IGN)
        except Exception as e:
            raise e
        params = {
            "key": APIKey,
            "uuid": uuid['id']
        }
        data = requests.get(url = APIhelper.hypixelStatusEndpoint, params=params).json()
        #print(data)
        return data

#print(APIhelper.nameToUUID("boomboom_YT"))
#print(APIhelper.rawStats("Lunarlmao"))
#print(APIhelper.rawStatus("boomboom_yt"))
#print(APIhelper.rawStats("lioness_rising"))
#print(APIhelper.query("lunar",hypixelAPIKey1 ))