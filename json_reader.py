from flask import json, abort
from era import Era
from civilisation import Civilisation 

def read_eras_from_json_file():
    try:
      with open(('civilisations/eras_info.json'), 'r') as f:
        json_data = json.load(f)
      eras = [Era(era['name'], era['summary'], era['image'], era['time_periods']) for era in json_data]
      return eras
    except IOError:
      abort(404) 

def read_civs_from_json_file(era_name, time_period):
    try:
      filepath = 'civilisations/' + era_name.lower() + '/' + time_period.lower() + '/civilisations.json'
      with open((filepath), 'r') as f:
        json_data = json.load(f)
      civs = [Civilisation(civ['name'], civ['region'], civ['established'], civ['end_date'], civ['gov_type'], civ['religion'], civ['image'], civ['fun_fact'], civ['info']) for civ in json_data]
      return civs
    except IOError: 
      abort(404)
