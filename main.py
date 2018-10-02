from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('base.html')

@app.route('/ancient_era/')
def ancient_era_page():
     return render_template('ancient_era_page.html')

@app.route('/middle_era/')
def middle_era_page():
    abort(404)

@app.route('/modern_era/')
def modern_era_page():
    abort(404)

if __name__ == ("__main__"):
    app.run(host='0.0.0.0', debug=True)

