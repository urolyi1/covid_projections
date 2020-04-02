import requests
from datetime import datetime
import os
import io
import zipfile

name_to_id = {'Alabama': 523, 'Alaska': 524, 'Arizona': 525, 'Arkansas': 526, 'California': 527, 'Colorado': 528,\
              'Connecticut': 529, 'Delaware': 530, 'District of Columbia': 531, 'Florida': 532, 'Georgia': 533,\
              'Hawaii': 534, 'Idaho': 535, 'Illinois': 536, 'Indiana': 537, 'Iowa': 538, 'Kansas': 539, 'Kentucky': 540,\
              'Louisiana': 541, 'Maine': 542, 'Maryland': 543, 'Massachusetts': 544, 'Michigan': 545, 'Minnesota': 546,\
              'Mississippi': 547, 'Missouri': 548, 'Montana': 549, 'Nebraska': 550, 'Nevada': 551, 'New Hampshire': 552,\
              'New Jersey': 553, 'New Mexico': 554, 'New York': 555,'North Carolina': 556, 'North Dakota': 557, 'Ohio': 558,\
              'Oklahoma': 559, 'Oregon': 560, 'Pennsylvania': 561,'Rhode Island': 562, 'South Carolina': 563,\
              'South Dakota': 564, 'Tennessee': 565, 'Texas': 566, 'Utah': 567, 'Vermont': 568, 'Virginia': 569,\
              'Washington': 570, 'West Virginia': 571, 'Wisconsin': 572, 'Wyoming': 573}

## Alternatively, we could read the total deaths from 8/4/2020.
## I didn't end up changing this function to make this consistent with our previous measurements
def total_deaths(dicts, keyword):
    return sum([i[keyword] for i in dicts if i["covid_measure_name"] == "deaths"])

low = mean = up = {}

# Save full csv to raw_data
r = requests.get('https://ihmecovid19storage.blob.core.windows.net/latest/ihme-covid19.zip', stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extract(z.namelist()[1], path='raw_data')


# For each state
for name,identity in name_to_id.items():
    # Get request and store total low, mean, high death projections
    state = requests.get(f"https://covid19.healthdata.org/api/data/hospitalization?location={identity}",\
                     headers={'User-Agent': 'Mozilla/5.0'}).json()
    low[name] = total_deaths(state,"lower")
    mean[name] = total_deaths(state,"mean")
    up[name] = total_deaths(state,"upper")

# Print low, mean, upper numbers for all states
for diction in [low,mean,up]:
    for name in sorted(diction):
        print(diction[name])

    print("-----------") 

