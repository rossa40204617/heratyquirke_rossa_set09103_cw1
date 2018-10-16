from flask import Flask, url_for, redirect, flash, abort, session, request, render_template
from civilisation import Civilisation
from era import Era
import os
import json
import json_reader

app = Flask(__name__)
app.secret_key = 'this is a secret!!!'

@app.route('/home/')
@app.route('/')
def home_page():
    eras = json_reader.read_eras_from_json_file()
    
    return render_template('era_index_page.html', eras=eras )

@app.route('/admin_login/', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':  
      if request.form['username'] == 'admin' and request.form['password'] == 'root':
        session['admin'] = True
      return render_template('admin_login_page.html')
    else:
      return render_template('admin_login_page.html')

@app.route('/admin_logout/', methods=['POST', 'GET'])
def admin_logout():
  session['admin'] = False
  flash("You have been logged out")
  return redirect(url_for('admin_login'))

@app.route('/editor/')
def editor_page():
  try: 
    if session['admin']:
      return render_template('admin_editor_page.html')
  except KeyError:
    pass
  flash("You need to be logged in as Admin to access that page")
  return redirect(url_for('admin_login'))

@app.route('/editor/add_civilisation/', methods=['POST', 'GET'])
def add_civilisation():
  try:
    if session['admin']:
      if request.method == 'POST':

        image = request.files['image']
        add_new_civilisation(request.form, image)      
      return render_template('add_new_civilisation_page.html') 
  except KeyError:
    pass
  flash("You need to be logged in as Admin to access that page")
  return redirect(url_for('admin_login')) 

@app.route('/editor/remove_civilisation/', methods=['POST', 'GET'])
def remove_civilisation():
  try:
    if session['admin']:
      if request.method == 'POST':
        remove_civilisation(request.form)
    return render_template('remove_civilisation_page.html')
  except KeyError:
    pass
  flash("You need to be logged in as Admin to access that page")
  return redirect(url_for('admin_login'))

def remove_civilisation(request):
   
   name = convert_url_to_field(request['name'])
   region = convert_url_to_field(request['region'])
   time_period = convert_url_to_field(request['time_period'])
   era = convert_url_to_field(request['era'])
    
   new_civ = {'name': name, 'region': region}
   
   filepath = construct_civilisation_filepath(era, time_period) 
    
   with open(filepath) as f:
     civs = json.load(f)

   civs.remove(new_civ)      
   
   with open(filepath, 'w') as f:
     json.dump(civs, f)
   flash("The entry on: '" + name + "' has been removed.")
   return(civs)

def add_new_civilisation(request, image):
   
   name = convert_url_to_field(request['name'])
   region = convert_url_to_field(request['region'])
   time_period = convert_url_to_field(request['time_period'])
   era = convert_url_to_field(request['era'])
   info = request['info']
   
   new_civ = {'name': name,'region': region, 'image': image.filename, 'info': info}
   
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
       
def check_if_civ_already_exists_in_file(name, civs = [], *args):
  for civ in civs:
    if name.lower() == civ['name'].lower():
      return True
  return False

def construct_civilisation_filepath(era, time_period):
  era = format_for_url_from_string(era)
  time_period = format_for_url_from_string(time_period)
  filepath = ('civilisations' + '/' + era + '/' + time_period + '/' + 'civilisations.json')
  return filepath 

@app.route('/<string:era_name>/')
def time_period_index_page(era_name):
    eras = json_reader.read_eras_from_json_file()

    era_name = convert_url_to_field(era_name) 
    era = filter_eras_by_name(era_name, eras) 

    return render_template('time_period_index_page.html', era=era)

def convert_url_to_field(url_string):
  result = url_string.replace("_", " ").title()
  return result

def filter_eras_by_name(era_name, eras = [], *args):
    for era in eras:
      if era.name.lower() == era_name.lower():
        return era
    abort(404)

@app.route('/<string:era_name>/<string:time_period>')
def region_index_page(era_name, time_period):
    civs = json_reader.read_civs_from_json_file(era_name, time_period)

    era_name = convert_url_to_field(era_name)
    time_period = convert_url_to_field(time_period)  
    regions = get_unique_regions_from_civs(civs)

    return render_template('region_index_page.html', era_name=era_name, time_period=time_period, regions=regions)

@app.route('/<string:era_name>/<string:time_period>/<string:region>/')
def civilisations_index_page(era_name, time_period, region):  
    civs = json_reader.read_civs_from_json_file(era_name, time_period)
	
    era_name = convert_url_to_field(era_name)
    time_period = convert_url_to_field(time_period)
    region = convert_url_to_field(region) 
    filtered_civs = filter_civs_by_region(region , civs)

    return render_template('civilisations_index_page.html', era_name=era_name, time_period=time_period, 
                           region=region, civs=filtered_civs)

@app.route('/<string:era_name>/<string:time_period>/<string:region>/<string:civ_name>/')
def civilisation_page(era_name, time_period, region, civ_name):
    print time_period
    civs = json_reader.read_civs_from_json_file(era_name, time_period)
     
    civ_name = convert_url_to_field(civ_name)  
    print time_period 
    time_period = convert_url_to_field(time_period) 
    print time_period
    civ = get_civ_by_name(civ_name, civs)

    return render_template('civilisation_page.html', era_name=era_name, 
                           time_period=time_period, region=region, civ=civ)
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404_error_page.html'), 404

def get_civ_by_name(civ_name, civs = [], *args):
    for civ in civs:
      if civ.name.lower() == civ_name.lower():
        return civ
    abort(404)

@app.errorhandler(401)
def unauthorised_error(error):
  return render_template('404_error_page.html'), 401

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

def format_for_url_from_string(string):
  result = string.replace(" ", "_").lower()
  return result

@app.context_processor
def utility_processor():
  def format_for_url_from_string(string):
    result = string.replace(" ","_").lower()
    return result
  return dict(format_string=format_for_url_from_string)

if __name__ == ("__main__"):
    app.run(host='0.0.0.0', debug=True)
