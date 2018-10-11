from flask import Flask, request, render_template
from civilisation import Civilisation
from era import Era
import os
import json
import json_reader
app = Flask(__name__)

@app.route('/home/')
@app.route('/')
def home_page():
    return render_template('base.html')

@app.route('/admin_login/', methods=['POST', 'GET'])
def admin_login():
    return render_template('admin_login_page.html')

@app.route('/add_civ/', methods=['POST', 'GET'])
def add_civ():
    if request.method == 'POST':
      print request.form
      name = request.form['name']
      region = request.form['region']
      time_period = request.form['time_period']
      era = request.form['era']
      
      new_civ = {'name': name,'region': region}
      
      filename = ('civilisations' + '/' + era + '/' + time_period + '/' + 'civilisations.json').lower()
      with open(filename) as f:
        civs = json.load(f)
      
      civs.append(new_civ) 
      
      with open(filename, 'w') as f:
        json.dump(civs, f)

      
      return render_template('add_new_civ_page.html')
    else:
      return render_template('add_new_civ_page.html')

@app.route('/<string:era_name>/')
def time_period_index_page(era_name):
    eras = json_reader.read_eras_from_json_file() 
    era = filter_eras_by_name(era_name, eras) 
    return render_template('time_period_index_page.html', era=era)

def filter_eras_by_name(era_name, eras = [], *args):
    for era in eras:
      if era.name.lower() == era_name.lower():
        return era
    abort(404)

@app.route('/<string:era_name>/<string:time_period>')
def region_index_page(era_name, time_period):
    civs = json_reader.read_civs_from_json_file(era_name, time_period)
    regions = get_unique_regions_from_civs(civs)
    return render_template('region_index_page.html', era_name = era_name, time_period = time_period, regions = regions)

@app.route('/<string:era_name>/<string:time_period>/<string:region>/')
def civilisations_index_page(era_name, time_period, region):
    civs = json_reader.read_civs_from_json_file(era_name, time_period)
    filtered_civs = filter_civs_by_region(region , civs)
    return render_template('civilisations_index_page.html', era_name=era_name, time_period = time_period, 
                           region = region, civs = filtered_civs)

@app.route('/<string:era_name>/<string:time_period>/<string:region>/<string:civ_name>/')
def civilisation_page(era_name, time_period, region, civ_name):
    civs = json_reader.read_civs_from_json_file(era_name, time_period)
    civ = get_civ_by_name(civ_name, civs)
    return render_template('civilisation_page.html', era_name = era_name, 
                           time_period = time_period, region = region, civ = civ)

def get_civ_by_name(civ_name, civs = [], *args):
    for civ in civs:
      if civ.name.lower() == civ_name.lower():
        return civ
    abort(404)

def filter_civs_by_region(region, civs = [], *args):
    filtered_civs = []
    for civ in civs:
      if civ.region.lower() == region.lower(): 
        filtered_civs.append(civ)
    return filtered_civs   

def get_unique_regions_from_civs(civs = [], *args):
  regions = set()
  for civ in civs:
    regions.add(civ.region)
  return regions

if __name__ == ("__main__"):
    app.run(host='0.0.0.0', debug=True)
