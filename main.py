from flask import Flask, url_for, redirect, flash, abort, session, request, render_template
from civilisation import Civilisation
from era import Era
import os
import json
import json_reader
import civilisations_manager
from random import randint

app = Flask(__name__)
app.secret_key = 'this is a secret!!!'

@app.route('/home/')
@app.route('/')
def home_page():
    eras = json_reader.read_eras_from_json_file()
    
    return render_template('era_index_page.html', eras=eras )

@app.route('/admin_login', methods=['POST', 'GET'], strict_slashes=False)
def admin_login():
    if request.method == 'POST':  
      if request.form['username'] == 'admin' and request.form['password'] == 'root':
        session['admin'] = True
      else:
        flash("Invalid credentials")
      return render_template('admin_login_page.html')
    else:
      return render_template('admin_login_page.html')

@app.route('/admin_logout', methods=['POST', 'GET'], strict_slashes=False)
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

@app.route('/editor/add_civilisation', methods=['POST', 'GET'], strict_slashes=False)
def add_civilisation():
  try:
    if session['admin']:
      if request.method == 'POST':

        image = request.files['image']
        civilisations_manager.add_new_civilisation(request.form, image)      
      return render_template('add_new_civilisation_page.html') 
  except KeyError:
    pass
  flash("You need to be logged in as Admin to access that page")
  return redirect(url_for('admin_login')) 

@app.route('/editor/remove_civilisation', methods=['POST', 'GET'], strict_slashes=False)
def remove_civilisation():
  try:
    if session['admin']:
      if request.method == 'POST':
        civilisations_manager.remove_civilisation(request.form)
    return render_template('remove_civilisation_page.html')
  except KeyError:
    pass
  flash("You need to be logged in as Admin to access that page")
  return redirect(url_for('admin_login'))

@app.route('/<string:era_name>/')
def time_period_index_page(era_name):
    eras = json_reader.read_eras_from_json_file()

    era_name = civilisations_manager.convert_url_to_field(era_name) 
    era = civilisations_manager.filter_eras_by_name(era_name, eras) 

    return render_template('time_period_index_page.html', era=era)

@app.route('/<string:era_name>/<string:time_period>/')
def region_index_page(era_name, time_period):
    civs = json_reader.read_civs_from_json_file(era_name, time_period)

    era_name = civilisations_manager.convert_url_to_field(era_name)
    time_period = civilisations_manager.convert_url_to_field(time_period)  
    regions = civilisations_manager.get_unique_regions_from_civs(civs)

    return render_template('region_index_page.html', era_name=era_name, time_period=time_period, regions=regions)

@app.route('/<string:era_name>/<string:time_period>/<string:region>/')
def civilisations_index_page(era_name, time_period, region):  
    civs = json_reader.read_civs_from_json_file(era_name, time_period)
    
    era_name = civilisations_manager.convert_url_to_field(era_name)
    time_period = civilisations_manager.convert_url_to_field(time_period)
    region = civilisations_manager.convert_url_to_field(region) 
    filtered_civs = civilisations_manager.filter_civs_by_region(region , civs)

    if not filtered_civs:  
      return redirect(url_for('region_index_page', era_name=civilisations_manager.format_for_url_from_string(era_name), time_period=civilisations_manager.format_for_url_from_string(time_period)))
    
    return render_template('civilisations_index_page.html', era_name=era_name, time_period=time_period, 
                           region=region, civs=filtered_civs)

@app.route('/<string:era_name>/<string:time_period>/<string:region>/<string:civ_name>', strict_slashes=False)
def civilisation_page(era_name, time_period, region, civ_name):
    civs = json_reader.read_civs_from_json_file(era_name, time_period)
     
    civ_name = civilisations_manager.convert_url_to_field(civ_name)  
    time_period = civilisations_manager.convert_url_to_field(time_period) 
    civ = civilisations_manager.get_civ_by_name(civ_name, civs)

    return render_template('civilisation_page.html', era_name=era_name, 
                           time_period=time_period, region=region, civ=civ)
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404_error_page.html'), 404

@app.context_processor
def format_processor():
  def format_for_url_from_string(string):
    result = string.replace(" ","_").lower()
    return result
  return dict(format_string=format_for_url_from_string)

@app.context_processor
def random_number_generator():
  def generate_unique_random_number(max_number, previous_numbers = [],*args):
    maximum = max_number-1
    number = randint(0, maximum)
    while number in previous_numbers:
      number = randint(0, maximum)
    return number  
  return dict(get_random_number=generate_unique_random_number)

if __name__ == ("__main__"):
    app.run(host='0.0.0.0', debug=True)
