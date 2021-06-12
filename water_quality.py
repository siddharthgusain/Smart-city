import requests
api = "WE15XY55QOB0YVXW"
channel_id = "876968"
field1 = "https://api.thingspeak.com/channels/{}/fields/1.json?api_key={}&results=1".format(channel_id,api)
r1 = requests.get(field1).json()
turbidity = r1['feeds'][0]['field1']

field2 = "https://api.thingspeak.com/channels/{}/fields/2.json?api_key={}&results=1".format(channel_id,api)
r2 = requests.get(field2).json()
pH = r2['feeds'][0]['field2']

field3 = "https://api.thingspeak.com/channels/{}/fields/3.json?api_key={}&results=1".format(channel_id,api)
r3 = requests.get(field3).json()
temp = r3['feeds'][0]['field3']

print("{}\n{}\n{}".format(turbidity,pH,temp))
#1 turbidity
#2 pH
#3 Temperature
