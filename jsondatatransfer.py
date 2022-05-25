from urllib.request import urlopen
import json
    
    
url = "https://rhul.buggyrace.net/specs/data/types.json"
response = urlopen(url)
data_json = json.loads(response.read())
# print(data_json['power_type']['wind']["cost"])

print(data_json['special']['hamster_booster']["cost"])
print( data_json['algo']['steady']['cost'])