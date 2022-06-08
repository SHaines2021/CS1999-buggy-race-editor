import sqlite3

DATABASE_FILE = "database.db"

# important:
#-------------------------------------------------------------
# This script initialises your SQLite database for you, just
# to get you started... there are better ways to express the
# data you're going to need... especially outside SQLite.
# For example... maybe flag_pattern should be an ENUM (which
# is available in most other SQL databases), or a foreign key
# to a pattern table?
#
# Also... the name of the database (here, in SQLite, it's a
# filename) appears in more than one place in the project.
# That doesn't feel right, does it?
#-------------------------------------------------------------

connection = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:

connection.execute("""

  CREATE TABLE IF NOT EXISTS buggies (
    id                    INTEGER PRIMARY KEY,
    qty_wheels            INTEGER DEFAULT 4,
    power_type            VARCHAR(20) DEFAULT 'petrol',
    power_units           INTEGER DEFAULT 1,
    aux_power_type        VARCHAR(20) DEFAULT 'none',
    aux_power_units       INTEGER DEFAULT 0,
    hamster_booster       INTEGER DEFAULT 0,
    flag_color            VARCHAR(20) DEFAULT 'white',
    flag_pattern          VARCHAR(20) DEFAULT 'plain',
    flag_color_secondary  VARCHAR(20) DEFAULT 'black',
    tyres                 VARCHAR(20) DEFAULT 'knobbly',
    qty_tyres             INTEGER DEFAULT 4,
    armour                VARCHAR(20) DEFAULT 'none',
    attack                VARCHAR(20) DEFAULT 'none',
    qty_attacks           INTEGER DEFAULT 0,
    fireproof             VARCHAR(20) DEFAULT 'false',
    insulated             VARCHAR(20) DEFAULT 'false',
    antibiotic            VARCHAR(20) DEFAULT 'false',
    banging               VARCHAR(20) DEFAULT 'false',
    algo                  VARCHAR(20) DEFAULT 'steady',
    power_cost            INTEGER DEFAULT 4,
    aux_power_cost        INTEGER DEFAULT 0,
    hamster_cost          INTEGER DEFAULT 0,
    tyres_cost            INTEGER DEFAULT 15,
    armour_cost           INTEGER DEFAULT 0,
    attack_cost           INTEGER DEFAULT 0,
    algo_cost             INTEGER DEFAULT 0,
    fireproof_cost        INTEGER DEFAULT 0,
    insulated_cost        INTEGER DEFAULT 0,
    antibiotic_cost       INTEGER DEFAULT 0,
    banging_cost          INTEGER DEFAULT 0,
    total_power_cost      INTEGER DEFAULT 4,
    total_tyres_cost      INTEGER DEFAULT 60,
    total_offdef_cost     INTEGER DEFAULT 0,
    total_special_cost    INTEGER DEFAULT 0,
    total_cost            INTEGER DEFAULT 64
    )

""")

print("- Table \"buggies\" exists OK")

cursor = connection.cursor()

cursor.execute("SELECT * FROM buggies LIMIT 1")
rows = cursor.fetchall()
if len(rows) == 0:
  cursor.execute("INSERT INTO buggies (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, hamster_booster, flag_color, flag_pattern, flag_color_secondary, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, algo, power_cost, aux_power_cost, hamster_cost, tyres_cost, armour_cost, attack_cost, algo_cost, fireproof_cost, insulated_cost, antibiotic_cost, banging_cost, total_power_cost, total_tyres_cost, total_offdef_cost, total_special_cost, total_cost, id) VALUES (4, 'petrol', 1, 'none', 0, 0, 'white', 'plain', 'black', 'knobbly', 4, 'none', 'none', 0, 'false', 'false', 'false', 'false', 'steady', 4, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 4, 60, 0, 0, 64, 0)")
  connection.commit()
  print("- Added one default buggy")
else:
  print("- Found a buggy in the database, nice")

print("- OK, your database is ready")

connection.close()
