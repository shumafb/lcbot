import json

with open('info.json', 'r', encoding='utf-8') as file:
    api = json.load(file)
print(api)
print(api['yapi_token'])