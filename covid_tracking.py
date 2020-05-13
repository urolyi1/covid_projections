import requests
from matplotlib import pyplot as plt
from matplotlib import dates
from datetime import datetime
overall = requests.get(f"https://covidtracking.com/api/v1/states/daily.json",\
                     headers={'User-Agent': 'Mozilla/5.0'}).json()

print('\n'.join(sorted(overall[0].keys())))

state_list = sorted(list(set([day["state"] for day in overall])))


def percentPositiveTests(state):
    state_data = list(filter(lambda x: x["state"]==state, overall))
    data = [{datetime.strptime(str(day["date"]), "%Y%m%d"):\
             day["positiveIncrease"]/day["totalTestResultsIncrease"]}\
            for day in state_data if day["totalTestResultsIncrease"]]
    x,y = zip(*[list(d.items())[0] for d in data])
    plt.plot(x,y)
    plt.show()

def graph(state, param):
    state_data = list(filter(lambda x: x["state"]==state, overall))
    data = [{datetime.strptime(str(day["date"]), "%Y%m%d"):\
             day[param]}\
            for day in state_data if day.get(param)]
    x,y = zip(*[list(d.items())[0] for d in data])
    plt.plot(x,y)
    plt.title(state)


def hospitalized(state):
    try:
        graph(state, "hospitalizedCurrently")
    except:
        return None

def up_hospital(state):
    graph(state, "hospitalizedIncrease")

def icu(state):
    try:
        graph(state, "inIcuCurrently")
    except:
        return None

def vent(state):
    try:
        graph(state, "onVentilatorCurrently")
    except:
        return None

def everything(state):
    hospitalized(state)
    icu(state)
    vent(state)
    plt.ylim(bottom=0)
    plt.show()

