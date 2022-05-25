from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from urllib.request import urlopen
import json
import math
import os
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)
app.secret_key='12345'

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    url = "https://rhul.buggyrace.net/specs/data/types.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchone();
        return render_template("buggy-form.html", buggy = record)
    elif request.method == 'POST':
        msg=""
        qty_wheels = request.form['qty_wheels']
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        aux_power_type = request.form['aux_power_type']
        aux_power_units = request.form['aux_power_units']
        hamster_booster = request.form['hamster_booster']
        flag_color = request.form['flag_color']
        flag_pattern = request.form['flag_pattern']
        flag_color_secondary = request.form['flag_color_secondary']
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']
        armour = request.form['armour']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        fireproof = request.form['fireproof']
        insulated = request.form['insulated']
        antibiotic = request.form['antibiotic']
        banging = request.form['banging']
        algo = request.form['algo']
        power_cost = data_json['power_type'][power_type]['cost']
        if aux_power_type == 'none':
            aux_power_cost = '0'
        else:
            aux_power_cost = data_json['power_type'][aux_power_type]['cost']
        hamster_cost = data_json['special']['hamster_booster']['cost']
        tyres_cost = data_json['tyres'][tyres]['cost']  
        armour_cost = data_json['armour'][armour]['cost'] 
        attack_cost = data_json['attack'][attack]['cost']     
        algo_cost = data_json['algo'][algo]['cost']
        if fireproof == 'false':
            fireproof_cost = '0'
        else:
            fireproof_cost = data_json['special']['fireproof']['cost']
        if insulated == 'false':
            insulated_cost = '0'
        else:
            insulated_cost = data_json['special']['insulated']['cost']
        if antibiotic == 'false':
            antibiotic_cost = '0'
        else:
            antibiotic_cost = data_json['special']['antibiotic']['cost']
        if banging == 'false':
            banging_cost = '0'
        else:
            banging_cost = data_json['special']['banging']['cost']

        total_power_cost = ((int(power_units) * int(power_cost)) + (int(aux_power_units) * int(aux_power_cost))+(int(hamster_booster)*int(hamster_cost)))
        total_tyres_cost = (int(qty_tyres) * int(tyres_cost))
        total_offdef_cost = (int(armour_cost)+int(int(attack_cost)*int(qty_attacks))+int(algo_cost))
        total_special_cost = (int(fireproof_cost)+int(insulated_cost)+int(antibiotic_cost)+int(banging_cost))
        total_cost = (int(total_power_cost)+int(total_tyres_cost)+int(total_offdef_cost)+int(total_special_cost))

        
        
        error = None
        
        
        if qty_wheels.isdigit() is False:
            error = 'Incorrect type of data entered, please enter an integer.'
            flash(error)
            return render_template('buggy-form.html', error=error)
            
        else:
            flash('Data entered is valid')
            try:
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    cur.execute(
                        "UPDATE buggies set qty_wheels=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, flag_color=?, flag_pattern=?, flag_color_secondary=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, algo=?, power_cost=?, aux_power_cost=?, hamster_cost=?, tyres_cost=?, armour_cost=?, attack_cost=?, algo_cost=?, fireproof_cost=?, insulated_cost=?, antibiotic_cost=?, banging_cost=?, total_power_cost=?, total_tyres_cost=?, total_offdef_cost=?, total_special_cost=?, total_cost=? WHERE id=?",
                        (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, power_cost, aux_power_cost, hamster_cost, tyres_cost, armour_cost, attack_cost, algo_cost, fireproof_cost, insulated_cost, antibiotic_cost, banging_cost, total_power_cost, total_tyres_cost, total_offdef_cost, total_special_cost, total_cost, DEFAULT_BUGGY_ID)
                    )
                    con.commit()
                    msg = "Record successfully saved"
            except:
                con.rollback()
                msg = "error in update operation"
            finally:
                con.close()
            return render_template("updated.html", msg = msg)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();
    return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# Show buggy info page
#------------------------------------------------------------
@app.route('/info')
def show_info():
    return render_template("info.html")

#------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
#------------------------------------------------------------
@app.route('/edit')
def edit_buggy():
    return render_template("buggy-form.html")

#------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items()
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None) })

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    alloc_port = os.environ['CS1999_PORT']
    app.run(debug=True, host="0.0.0.0", port=alloc_port)
