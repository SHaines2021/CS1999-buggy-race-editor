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
    
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();

    if request.method == 'GET':
        return render_template("buggy-form.html", buggy = None)
            
    elif request.method == 'POST':
        error = None
        msg=""
        if request.form.get('defaults') == 'Apply Defaults':
            url_default = "https://rhul.buggyrace.net/specs/data/defaults.json"
            response_def = urlopen(url_default)
            data_json_def = json.loads(response_def.read())

            buggy_id = request.form['id']
            qty_wheels = str(data_json_def['qty_wheels'])
            power_type = str(data_json_def['power_type'])
            power_units = str(data_json_def['power_units'])
            aux_power_type = str(data_json_def['aux_power_type'])
            aux_power_units = str(data_json_def['aux_power_units'])
            hamster_booster = str(data_json_def['hamster_booster'])
            flag_color = str(data_json_def['flag_color'])
            flag_pattern = str(data_json_def['flag_pattern'])
            flag_color_secondary = str(data_json_def['flag_color_secondary'])
            tyres = str(data_json_def['tyres'])
            qty_tyres = str(data_json_def['qty_tyres'])
            armour = str(data_json_def['armour'])
            attack = str(data_json_def['attack'])
            qty_attacks = str(data_json_def['qty_attacks'])
            fireproof = str(data_json_def['fireproof'])
            insulated = str(data_json_def['insulated'])
            antibiotic = str(data_json_def['antibiotic'])
            banging = str(data_json_def['banging'])
            algo = str(data_json_def['algo'])

        else:
            buggy_id = request.form['id']
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
        if aux_power_type == 'none' or 'null':
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


        
        # data validation:
        #is the entered data an integer?
        if qty_wheels.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (qty_wheels)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        elif power_units.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (power_units)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        elif aux_power_units.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (aux_power_units)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        elif hamster_booster.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (hamster_booster)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        elif qty_tyres.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (qty_tyres)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        elif qty_attacks.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (qty_attacks)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        #are there 4 or more wheels?
        elif int(qty_wheels)<=3:
            error = 'Oops! Please enter 4 or more wheels. (qty_wheels)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        #are the wheels an even number?
        elif int(qty_wheels)%2 !=0:
            error = 'Oops! Please enter an even number of wheels. (qty_wheels)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        #at least 1 unit of power?
        elif int(power_units)<1:
            error = 'Oops! Please enter at least 1 unit of power. (power_units)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        #at least 0 units of power?
        elif int(aux_power_units)<0:
            error = 'Oops! Please enter at least 0 units of aux power. (aux_power_units)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        #two flag colours required if flag pattern is not plain
        elif flag_pattern != 'plain':
            if flag_color == flag_color_secondary:
                error = 'Oops! Please enter two different flag colours when not using the plain flag pattern. (flag_color)'
                flash(error)
                return render_template('buggy-form.html', buggy = record)
        #are there equal number or more tyres than wheels?
        elif int(qty_tyres)<int(qty_wheels):
            error = 'Oops! Please enter an equal or greater number of tyres than wheels. (qty_tyres)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)
        #at least 0 units of attack?
        elif int(qty_attacks)<0:
            error = 'Oops! Please enter at least 0 attacks. (qty_attacks)'
            flash(error)
            return render_template('buggy-form.html', buggy = record)

        else:
            total_power_cost = ((int(power_units) * int(power_cost)) + (int(aux_power_units) * int(aux_power_cost))+(int(hamster_booster)*int(hamster_cost)))
            total_tyres_cost = (int(qty_tyres) * int(tyres_cost))
            total_offdef_cost = (int(armour_cost)+int(int(attack_cost)*int(qty_attacks))+int(algo_cost))
            total_special_cost = (int(fireproof_cost)+int(insulated_cost)+int(antibiotic_cost)+int(banging_cost))
            total_cost = (int(total_power_cost)+int(total_tyres_cost)+int(total_offdef_cost)+int(total_special_cost))
            flash('Thanks! Data entered is valid!')
            
            try:
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    if buggy_id:
                        cur.execute(
                            "UPDATE buggies set qty_wheels=?, power_type=?, power_units=?, aux_power_type=?, aux_power_units=?, hamster_booster=?, flag_color=?, flag_pattern=?, flag_color_secondary=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, antibiotic=?, banging=?, algo=?, power_cost=?, aux_power_cost=?, hamster_cost=?, tyres_cost=?, armour_cost=?, attack_cost=?, algo_cost=?, fireproof_cost=?, insulated_cost=?, antibiotic_cost=?, banging_cost=?, total_power_cost=?, total_tyres_cost=?, total_offdef_cost=?, total_special_cost=?, total_cost=? WHERE id=?",
                            (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, power_cost, aux_power_cost, hamster_cost, tyres_cost, armour_cost, attack_cost, algo_cost, fireproof_cost, insulated_cost, antibiotic_cost, banging_cost, total_power_cost, total_tyres_cost, total_offdef_cost, total_special_cost, total_cost, buggy_id)
                        )
                    else:
                        cur.execute(
                            "INSERT INTO buggies (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, power_cost, aux_power_cost, hamster_cost, tyres_cost, armour_cost, attack_cost, algo_cost, fireproof_cost, insulated_cost, antibiotic_cost, banging_cost, total_power_cost, total_tyres_cost, total_offdef_cost, total_special_cost, total_cost) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, power_cost, aux_power_cost, hamster_cost, tyres_cost, armour_cost, attack_cost, algo_cost, fireproof_cost, insulated_cost, antibiotic_cost, banging_cost, total_power_cost, total_tyres_cost, total_offdef_cost, total_special_cost, total_cost)
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
    records = cur.fetchall();
    return render_template("buggy.html", buggies = records)

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
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE ID=?", (buggy_id,))
    record = cur.fetchone();
    return render_template("buggy-form.html", buggy = record)

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
