from flask import Flask 

import requests
from pprint import pprint
import operator

app = Flask(__name__) 

@app.route("/") 
def home_view(): 
		return get_data()

def get_data():
    url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.json"
    github = "https://github.com/jacombo/covid-death-stats"
    response = requests.get(url)
    
    output = "<h1>Covid 19 pocet umrti od zacatku roku 2020</h1>"
    output = output + "<h3>Data aktualizovany:%s</h3>" % (response.json()['modified'])

    summary = {}
    age_count = 0
    total_deaths = 0
    for item in response.json()['data']:
        #print("%s %s" % (item['vek'], round(item['vek'],-1)))
        age = round(item['vek'],-1)
        age_count = age_count + age

        if age in summary:
            count = summary[age]
        else:
            count = 1    
        
        summary[age] = count + 1
        total_deaths = total_deaths + 1

    # Sort Dictionary by value using itemgetter
    sorted_dict = dict(sorted(summary.items(),
                                key=operator.itemgetter(1),
                                reverse=True))

    for k,v in sorted_dict.items():
        output = output + "Vek:%s+&nbsp;&nbsp;&nbsp;&nbsp;pocet umrti:%s&nbsp;&nbsp;&nbsp;&nbsp;%s%%</br>" % (k,v, round((v / total_deaths) * 100, 1))

    output = output + "</br>Prumerny vek mrtvych:%s</br>" % (round(age_count / total_deaths, 1))
    output = output + "</br>Celkovy pocet mrtvych:%s</br>" % (total_deaths)
    output = output + "</br><a target='_blank' href='%s'>Zdroj dat</a></br><a target='_blank' href='%s'>GitHub zdrojaky</a>" % (url,github)
    return output
