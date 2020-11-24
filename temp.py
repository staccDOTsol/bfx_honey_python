import json

with open('BTCUSD'.replace('/','') + '.json', 'r') as outfile:
	temp = json.loads(outfile.read() + ']"')
print(temp)