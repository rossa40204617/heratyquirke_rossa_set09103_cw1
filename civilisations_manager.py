from civilisation import Civilisation
from flask import Flask, url_for, flash, abort
import json

def remove_civilisation(request):

   name = convert_url_to_field(request['name'])
   time_period = convert_url_to_field(request['time_period'])
   era = convert_url_to_field(request['era'])

   filepath = construct_civilisation_filepath(era, time_period)

   with open(filepath) as f:
     civs = json.load(f)

   for civ in civs:
     if civ['name']  == name:
       civs.remove(civ)
   
   with open(filepath, 'w') as f:
     json.dump(civs, f)
   flash("The entry on: '" + name + "' has been removed.")
   return(civs)

def add_new_civilisation(request, image):

   name = convert_url_to_field(request['name'])
   region = convert_url_to_field(request['region'])
   time_period = convert_url_to_field(request['time_period'])
   era = convert_url_to_field(request['era'])
   established = convert_url_to_field(request['established'])
   end_date = convert_url_to_field(request['end_date'])
   gov_type = convert_url_to_field(request['gov_type'])
   religion = convert_url_to_field(request['religion'])
   fun_fact = convert_url_to_field(request['fun_fact'])
   info = request['info']

   new_civ = {'name': name,'region': region, 'image': image.filename, 'info': info, 'established': established,
              'end_date': end_date, 'gov_type': gov_type, 'religion': religion, 'fun_fact': fun_fact }

   filepath = construct_civilisation_filepath(era, time_period)

   with open(filepath) as f:
     civs = json.load(f)

   if check_if_civ_already_exists_in_file(name, civs):
     flash("An entry for the civilisation '" + name + "' already exists")
   else:
     civs.append(new_civ)
     image.save('static/img/' + image.filename)
     with open(filepath, 'w') as f:
       json.dump(civs, f)
     flash(name + " has been added as a new civilisation")

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

def get_civ_by_name(civ_name, civs = [], *args):
    for civ in civs:
      if civ.name.lower() == civ_name.lower():
        return civ
    abort(404)

def convert_url_to_field(url_string):
  result = url_string.replace("_", " ").title()
  return result

def filter_eras_by_name(era_name, eras = [], *args):
    for era in eras:
      if era.name.lower() == era_name.lower():
        return era
    abort(404)

def construct_civilisation_filepath(era, time_period):
  era = format_for_url_from_string(era)
  time_period = format_for_url_from_string(time_period)
  filepath = ('civilisations' + '/' + era + '/' + time_period + '/' + 'civilisations.json')
  return filepath

def check_if_civ_already_exists_in_file(name, civs = [], *args):
  for civ in civs:
    if name.lower() == civ['name'].lower():
      return True
  return False

def format_for_url_from_string(string):
  result = string.replace(" ", "_").lower()
  return result
