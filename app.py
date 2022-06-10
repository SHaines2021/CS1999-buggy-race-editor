from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from urllib.request import urlopen, Request
import json
import random
import math
import os
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)
#secret key required to utlise the session's cookie for flash messages.
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
# the poster page
#------------------------------------------------------------
@app.route('/poster')
def poster():
    return render_template('poster.html')


#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    #this variable holds the url for the buggy race server's json API that gives all the buggy spec variables.
    url = Request("https://rhul.buggyrace.net/specs/data/types.json", headers={'User-Agent': 'Mozilla/5.0'})
    #open the page 
    response = urlopen(url)
    #load the json from the read page. This variable will be used extensively for referencing individual specifications
    data_json = json.loads(response.read())


    #this block connects to the SQL database and gets the first row and turns it into a dictionary like object (here: 'record')
    #This record give what is the default buggy record
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();
    
    
    if request.method == 'GET':
        #convert the sql dictionary-type object to an actual python dictionary
        record=dict(record)
        #delete the id present in the record
        del record['id']
        #load the buggy form template with this record as buggy, which gives the whole form filled with the default buggy but without an id for the new buggy creation
        return render_template("buggy-form.html", buggy = record)

    elif request.method == 'POST':
        #intialise without error or msg
        error = None
        msg=""
        #buggy id from the buggy form
        buggy_id = request.form['id']

        #if button pressed for default_buggy, then as follows
        if request.form.get('default_button') != None:
            #import the json data from the server API, specificly the defaults only
            url_default = "https://rhul.buggyrace.net/specs/data/defaults.json"
            response_def = urlopen(url_default)
            data_json_def = json.loads(response_def.read())
            
            #import each variable from the server defults, as strings
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
            pass

        elif request.form.get('random_button') != None:
            power_list = ['petrol', 'fusion', 'steam', 'bio', 'electric', 'rocket', 'hamster', 'thermo', 'solar', 'wind']
            aux_power_list = ['none', 'petrol', 'fusion', 'steam', 'bio', 'electric', 'rocket', 'hamster', 'thermo', 'solar', 'wind']
            color_list = ['#000000', '#808080','#FFFFFF','#800000','#FF0000','#800080','#FF00FF','#008000','#00FF00','#808000','#FFFF00','#000080','#0000FF','#008080','#00FFFF']
            pattern_list = ['plain', 'vstripe', 'hstripe', 'dstripe', 'checker', 'spot']
            tyres_list = ['knobbly', 'slick', 'steelband', 'reactive', 'maglev']
            armour_list = ['none', 'wood', 'aluminium', 'thinsteel', 'thicksteel', 'titanium']
            attack_list = ['none', 'spike', 'flame', 'charge', 'biohazard']
            special_list = ['true','false']
            algo_list = ['defensive', 'steady', 'offensive', 'titfortat', 'random', 'buggy']
            qty_list = ['4','6','8','10']
            unit_list = ['1','2','3','4','5','6','7','8','9','10']
            qty_wheels = random.choice(qty_list)
            power_type = random.choice(power_list)
            power_units = random.choice(unit_list)
            aux_power_type = random.choice(aux_power_list)
            if aux_power_type == 'none':
                aux_power_units = 0
            else:
                aux_power_units = random.choice(unit_list)
            hamster_booster = random.choice(unit_list)
            flag_color = random.choice(color_list)
            flag_pattern = random.choice(pattern_list)
            if flag_pattern != 'plain':
                second_color_list = [value for value in color_list if value != flag_color]
                flag_color_secondary = (random.choice(second_color_list))
            else:
                flag_color_secondary = (random.choice(color_list))
            tyres = (random.choice(tyres_list))
            qty_tyres = qty_wheels
            armour = (random.choice(armour_list))
            attack = (random.choice(attack_list))
            qty_attacks = (random.choice(unit_list))
            fireproof = (random.choice(special_list))
            insulated = (random.choice(special_list))
            antibiotic = (random.choice(special_list))
            banging = (random.choice(special_list))
            algo = (random.choice(algo_list))
            pass


        else:
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
            pass


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
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        elif power_units.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (power_units)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        elif aux_power_units.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (aux_power_units)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        elif hamster_booster.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (hamster_booster)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        elif qty_tyres.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (qty_tyres)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        elif qty_attacks.isdigit() is False:
            error = 'Oops! Incorrect type of data entered, please enter an integer. (qty_attacks)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        #are there 4 or more wheels?
        elif int(qty_wheels)<=3:
            error = 'Oops! Please enter 4 or more wheels. (qty_wheels)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        #are the wheels an even number?
        elif int(qty_wheels)%2 !=0:
            error = 'Oops! Please enter an even number of wheels. (qty_wheels)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        #at least 1 unit of power?
        elif int(power_units)<1:
            error = 'Oops! Please enter at least 1 unit of power. (power_units)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        #at least 0 units of power?
        elif int(aux_power_units)<0:
            error = 'Oops! Please enter at least 0 units of aux power. (aux_power_units)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        #two flag colours required if flag pattern is not plain
        elif flag_pattern != 'plain' and flag_color == flag_color_secondary:
            error = 'Oops! Please enter two different flag colours when not using the plain flag pattern. (flag_color)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        #are there equal number or more tyres than wheels?
        elif int(qty_tyres)<int(qty_wheels):
            error = 'Oops! Please enter an equal or greater number of tyres than wheels. (qty_tyres)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
                return render_template('buggy-form.html', buggy = record)
        #at least 0 units of attack?
        elif int(qty_attacks)<0:
            error = 'Oops! Please enter at least 0 attacks. (qty_attacks)'
            flash(error)
            if buggy_id == '':
                record=dict(record)
                del record['id']
                return render_template('buggy-form.html', buggy = record)
            else:
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
# a delete section
#------------------------------------------------------------
@app.route('/delete/<buggy_id>')
def delete_buggy(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("DELETE FROM buggies WHERE ID=?", (buggy_id,))
    con.commit()
    cur.execute("SELECT * FROM buggies")
    records = cur.fetchall();
    msg = f"Success! Buggy #{buggy_id} deleted."
    return render_template("buggy.html", buggies = records, msg=msg)

#------------------------------------------------------------
# render json template to select buggy to view json data export

#------------------------------------------------------------
@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    records = cur.fetchall();
    return render_template("json.html", buggies = records)

#------------------------------------------------------------
# extension of json route with individual json being selected for export

#------------------------------------------------------------

@app.route('/json/<buggy_id>')
def summary_json(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (buggy_id,))
    buggies = dict(zip([column[0] for column in cur.description], cur.fetchone())).items()
    return jsonify({ key: val for key, val in buggies if (val != "" and val is not None)})

#------------------------------------------------------------

# You shouldn't need to add anything below this!
if __name__ == '__main__':
    alloc_port = os.environ['CS1999_PORT']
    app.run(debug=True, host="0.0.0.0", port=alloc_port)
