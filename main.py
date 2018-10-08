from flask import Flask, render_template, json, jsonify
from civilisation import Civilisation
from era import Era
import os
app = Flask(__name__)

@app.route('/home/')
@app.route('/')
def home_page():
    return render_template('base.html')

@app.route('/<string:era_name>/')
def time_period_index_page(era_name):
    eras = read_eras_from_json_file() 
    era = filter_eras_by_name(era_name, eras) 
    return render_template('time_period_index_page.html', era=era)

def filter_eras_by_name(era_name, eras = [], *args):
    for era in eras:
      if era.name.lower() == era_name.lower():
        return era
    abort(404)

@app.route('/<string:era_name>/<string:time_period>')
def region_index_page(era_name, time_period):
    civs = read_civs_from_json_file(era_name.lower() + '.json')
    regions = get_unique_regions(civs)
    return render_template('region_index_page.html', era_name = era_name, time_period = time_period, regions = regions)

@app.route('/<string:era_name>/<string:time_period>/<string:region>/')
def civilisations_index_page(era_name, time_period, region):
    civs = read_civs_from_json_file(era_name.lower() + '.json')
    filtered_civs = filter_civs_by_time_and_region(time_period, region , civs)
    return render_template('civilisations_index_page.html', era_name=era_name, time_period = time_period, 
                           region = region, civs = filtered_civs)

@app.route('/<string:era_name>/<string:time_period>/<string:region>/<string:civ_name>/')
def civilisation_page(era_name, time_period, region, civ_name):
    civs = read_civs_from_json_file(era_name.lower() + '.json')
    civ = get_civ_by_name(civ_name, civs)
    return render_template('civilisation_page.html', era_name = era_name, 
                           time_period = time_period, region = region, civ = civ)

def get_civ_by_name(civ_name, civs = [], *args):
    for civ in civs:
      if civ.name.lower() == civ_name.lower():
        return civ
    abort(404)

def filter_civs_by_time_and_region(time_period, region, civs = [], *args):
    filtered_civs = []
    for civ in civs:
      if civ.time_period.lower() == time_period.lower() and civ.region.lower() == region.lower(): 
        filtered_civs.append(civ)
    return filtered_civs

def get_unique_time_periods(civs = [], *args):
  time_periods = set()
  for civ in civs:
    time_periods.add(civ.time_period)
  return time_periods   

def get_unique_regions(civs = [], *args):
  regions = set()
  for civ in civs:
    regions.add(civ.region)
  return regions

def read_eras_from_json_file():
    with open(('static/eras.json'), 'r') as f:
      json_data = json.load(f)
    eras = [Era(era['name'], era['summary'], era['time_periods']) for era in json_data]
    return eras

def read_civs_from_json_file(filename):
    with open(('static/' + filename), 'r') as f:
      json_data = json.load(f)
    civs = [Civilisation(civ['name'], civ['region'], civ['time_period']) for civ in json_data]
    return civs

if __name__ == ("__main__"):
    app.run(host='0.0.0.0', debug=True)
