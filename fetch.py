from urllib.request import urlopen
import json
from pprint import pprint
from datetime import date



url = "https://api.github.com/repos/jomjol/AI-on-the-edge-device/releases?page=1&per_page=10"

response = urlopen(url)
data_json = json.loads(response.read())

summary = {}


for releaseIndex in range(0, len(data_json)):
    release_name = data_json[releaseIndex]['name']
    summary[release_name] = {}

    for assetIndex in range(0, len(data_json[releaseIndex]['assets'])):
        asset_name = data_json[releaseIndex]['assets'][assetIndex]['name']
        asset_download_count = data_json[releaseIndex]['assets'][assetIndex]['download_count']

        summary[release_name][asset_name] = asset_download_count



pprint(summary)

filename = date.today().strftime("%Y-%m-%d") + ".json"

with open("database/" + filename, "w") as outfile:
    json.dump(summary, outfile, indent=4, sort_keys=True)
