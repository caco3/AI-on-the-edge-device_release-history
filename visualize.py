import os
import json
from pprint import pprint
from datetime import date
import plotly.express as px

files = os.listdir('database')


files.sort()
#print(files)

print("Found %d files" % len(files))

history = {}

dates = []

for filename in files:
    with open("database/" + filename, "r") as infile:
        data = json.load(infile)
        #pprint(data)

        date = filename.replace(".json", "")

        for version in data:

            versionParts = version.split(".")
            if not versionParts[0].isnumeric():
                print("Error: version does not start with a number: %r -> Skipping!" % version)
                continue

            # Hide versions below v12
            if int(versionParts[0]) < 12:
                continue

            # Hide RC (Release Canditates)
            if "RC" in version:
                continue

            if not version in history:
                history[version] = {}

            sum = 0
            for file in data[version]:
                sum += data[version][file]

            if not 'date' in history[version]:
                history[version]['date'] = []

            if not 'downloads' in history[version]:
                history[version]['downloads'] = []

            history[version]['date'].append(date)
            history[version]['downloads'].append(sum)

        dates.append(date)



#pprint(history)



import plotly.graph_objects as go

fig = px.line(x=dates, y=[0]*len(dates), title="AI on the Edge Device - Release Downloads")
fig.update_traces(line_color='#FFFFFF') # Hide the first line


for version in history:
    fig.add_trace(go.Scatter(x=history[version]['date'], y=history[version]['downloads'],
                             name=version, mode="lines", hovertext="Version "+version))
#fig.update_yaxes(type="log")
fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='Cumulated Downloads')

fig.update_layout(legend=dict(title="Versions"))

# fig.show()

os.mkdir("html")
fig.write_html("html/index.html")


