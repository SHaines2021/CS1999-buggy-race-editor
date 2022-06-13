# Application Testing
---

## Contents:
* [Aim](#Aim:)
* [Method](#Method:)
    * [Initial set up](#Initial-set-up:)
    * [Testing Links and Templates](#Testing-Links-and-Templates:)
        * [Test the Index Page](#Test-the-Index-Page:)
        * [Test the /new Page](#Test-the-/new-Page:)
        * [Test the /buggy Page](#Test-the-/buggy-Page:)
        * [Test the /json Page](#Test-the-/json-Page:)
        * [Test the /info Page](#Test-the-/info-Page:)
        * [Test the /poster Page](#Test-the-/poster-Page:)
    * [Testing Database](#Testing-Database:)
        * [Default Buggy](#Default-Buggy:)
        * [Random Buggy](#Random-Buggy:)
        * [Clear Changes](#Clear-Changes:)
    * [Data Validation](#Data-Validation:)
        * [Is the entered data an integer?](#Is-the-entered-data-an-integer?:)      
        * [Are there 4 or more wheels?](#Are-the-wheels-an-even-number?:)
        * [At least 1 unit of power?](#At-least-1-unit-of-power?:)
        * [At least 0 units of power?](#At-least-0-units-of-power?:)
        * [Two flag colours required if flag pattern is not plain](#Two-flag-colours-required-if-flag-pattern-is-not-plain:)
        * [Are there equal number or more tyres than wheels?](#Are-there-equal-number-or-more-tyres-than-wheels?:)
        * [At least 0 units of attack?](#At-least-0-units-of-attack?:)
* [Testing Comments](#Testing-Comments:)
 

---

## Aim
To manually test and verify the functionality of the `app.py` buggy editor.
This testing is grouped into the major functionalities of each code module.

---

## Method:

### Initial set up:
If the `database.db` exists, delete it and 
run `python3 init_db.py`
this will generate a new `database.db`

When this is successful the following message should be shown:
>>> cim-ts-node-02$ python3 init_db.py 
Opened database successfully in file "database.db"
Table "buggies" exists OK
Added one default buggy
OK, your database is ready



### Testing Links and Templates
This is to ensure all the links within the website are functioning as expected.
Run: `python3 app.py` and open the server

##### Test the Index Page:
The first page is the Index page with the title "Sarah's Buggy Editor" and this page will give 6 links to test, as follows:
* "Make a buggy"
    * this should route to the url `/new`
* "Show Buggies"
    * this should route to the url `/buggy`
* "Get Buggy JSON"
    * this should route to the url `/json`
* "View Buggy Specs"
    * this should route to the url `/info`
* "View Poster"
   *  this should route to the url `/poster`
* "race server"
    * this should route to the url `https://rhul.buggyrace.net/`

##### Test the `/new` page:
Once on this page there are 10 more links, 5 links repeated at the top and bottom of the page:
* "Return Home"
    * This should route to the index page
* "Submit Form"
    * This should submit all the data within the form and display the "Updated Buggy" page
* "Clear Changes"
    * This clears all the modified fields in the form and restores them to what the page had when it loaded
* "Submit a Random Buggy"
    * This should submit **random** values for all buggy attributes and display the "Updated Buggy" page
* "Submit a Default Buggy"
    * This should submit **default**  values for all buggy attributes and display the "Updated Buggy" page

##### Test the `/buggy` page:
This should take you to a page with the title "All buggies". Visible should be a message that says "default buggy loaded OK." and six navigation buttons, three at the top and the same at the bottom:

* "Return Home"
    * This should route to the index page
* "Make a New Buggy"
    * This should route to the `/new` page to create a new buggy
* "Get Buggy JSON"
    * This should route to the `/json` page to select buggy JSON to view

Each displayed buggy should also list the following links:
* "Edit me"
    * This should route to the `/new/<buggy_id>` page to update this buggy's record
* "Show JSON"
    * This should route to the `/json/<buggy_id>` page to directly view this buggy's JSON
* "Delete me"
    * This should reload the `/buggy` page with a success message
        >Success! Buggy #2 deleted.

##### Test the `/json` page:
This should take you to a page with the title "Get Buggy JSON". Visible three navigation buttons and records for each buggy in the database (not id#0) including their IDs, flags and Show JSON link:
* "Return Home"
    * This should route to the index page
* "Make a New Buggy"
    * This should route to the `/new` page to create a new buggy
* "Get Buggy JSON"
    * This should route to the `/json` page to select buggy JSON to view
* "Show JSON"
    * This should route to the /json/<buggy_id> page to directly view this buggy’s JSON

##### Test the `/info` page:
This should take you to a page with the title "Buggy Specifications". This page has one navigation link and a live i-frame displaying the buggy race server specifications from the url: ( https://rhul.buggyrace.net/specs ):
* "Return Home"
    * This should route to the index page

##### Test the `/poster` page:
This should take you to a page with one navigation link and details about the buggy editor:
* "Return Home"
    * This should route to the index page

### Testing Database
##### Default Buggy
* Submit a **default** buggy to the database
* Look this buggy up in the `/buggy` page
* Verify the costs for each subsection match the costs listed, i.e.: 
    >>>Type of tyres:	knobbly 
    cost: 15
    Number of tyres: 4
    Total Traction Cost: **60**
* Verify that the links in the buggy page navigate to that buggy's record
    * Edit Me
    * View JSON
    * Delete Me
    
#### Random Buggy
* Submit a **random** buggy to the database
* Look this buggy up in the `/buggy` page

##### Clear Changes
* Enter data into the buggy form and reset it with the `Clear Changes` button

##### JSON
* Open the `/json` page and verify that the route to the buggy's json data functions

### Data Validation
The data manually entered in the text fields are subject to data validation. Typically these are fields where only integers are expected or if the buggy race rules demands that only certain values are valid:

##### Is the entered data an integer?
* Enter a non-integer value into one of the following variables to challenge the form validation:
    ``` 
    qty_wheels, 
    power_units, 
    aux_power_units, 
    hamster_booster, 
    qty_tyres, 
    qty_attacks
    ```

##### Are there 4 or more wheels? Are the wheels an even number?
* Enter a `3` into the qty_wheels variable to challenge the form validation

##### At least 1 unit of power?
* Enter a `0` into the power_units variable to challenge the form validation

##### At least 0 units of power?
* Enter a `` into the aux_power_units variable to challenge the form validation

##### Two flag colours required if flag pattern is not plain
* Enter a the same flag colours for primary and secondary colours, with a pattern other than 'plain' to challenge the form validation

##### Are there equal number or more tyres than wheels?
* Enter a `3` into the qty_tyres variable to challenge the form validation

##### At least 0 units of attack?
* Enter a `` into the attack_units variable to challenge the form validation

 


--- 
## Testing Comments:
Over the course of this task a large number of potential testing methods were attempted with the view to generating an automatic test set. This proved not to be possible within the remaining time. If more time were avaiable then an automatic testing suite could be written in pytest or unittest generating a duplicate/test database and unit tests for each functional block of the application code and verification statements like AssertTrue(x) to determine a range of pass/fail criterions. For example, with the input of a dummy buggy record it would be possible to quickly test if the cost calculations, database and form were capable of functioning as anticipated. After this boarder/edge values could then be added to the trial to ensure greater stability. This may inclue a very large number of wheels, symbols or decimals.
   
---
   
Sarah Haines 2022.

---

END.



