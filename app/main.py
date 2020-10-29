from flask import Flask

import requests
from pprint import pprint
import operator
from flask import render_template

app = Flask(__name__,
            static_url_path='/static')

overview_url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.json"
death_url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.json"
github = "https://github.com/jacombo/covid-death-stats"

@app.route("/")
def home_view():
    return render_template('index.html', deaths=deaths_by_age(), general=general_stats())


def deaths_by_age():
    response = requests.get(death_url)
    deaths = dict()
    summary = {}
    age_count = 0
    total_deaths = 0
    for item in response.json()['data']:
        age = round(item['vek'], -1)
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
    deaths['groups'] = list()
    for k, v in sorted_dict.items():
        deaths['groups'].append({ "age": k, "count": v, "percentage": round((v / total_deaths) * 100, 1) })
    deaths['last_updated'] = response.json()['modified']
    deaths['average_death_age'] = round(age_count / total_deaths, 1)
    deaths['total_deaths'] = total_deaths
    return deaths

def general_stats():
    response = requests.get(overview_url)
    item = response.json()['data'][0]
    general = dict()
    general['to_date'] = item['datum']
    general['tests_total'] = item['provedene_testy_celkem']
    general['confirmed_cases_total'] = item['potvrzene_pripady_celkem']
    general['active_cases'] = item['aktivni_pripady']
    general['cured'] = item['vyleceni']
    general['deaths'] = item['umrti']
    general['currently_hospitalized'] = item['aktualne_hospitalizovani']
    general['mortality'] = round((item['umrti'] / item['potvrzene_pripady_celkem'] * 100), 4)
    general['src_general'] = overview_url
    general['src_deaths'] = death_url
    general['src_code'] = github
    return general
