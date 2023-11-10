Online Voting System
====================

The application is written in Python3 and uses FLask, WTForms, sqlite and many others mentioned in the requirements.txt file.

The application allows to create users. Users can create their own voting events and close them as well. Once a voting event is created, it is visible in the dashboards for all the users so that they can caste their vote to the candidates participating in the vote event. Once a vote is casted by the user, they will not be able to cast it again and the results are shown only when the vote event is closed by the user who created that event.

---
## Creating a virtual python env
sudo apt install python3.8-venv
python3 -m venv virt
source virt/bin/activate (for linux, mac)
---

## Installing sqlitebrowser
Since, we are using sqlite, we need a browser to see the tables and data inside. To install the browser:
```Bash
sudo apt-get install sqlitebrowser
```
---

## Database
The database file is in intsance folder and if you want to create a new db file, create models in app.py and open the python terminal to execute the below commands:
```Python
from app import app, db
app.app_context().push()
db.create_all()
exit()
```

If you make any changes to the model in the app.py like adding a new column etc. These changes will have to be migrated/applied on the database.db file. These commands will help:
This will create the migrations folder (for the first time only):
```Bash
flask db init 
```
This will create a python code in versions folder with upgrade and downgrade methods in it:
```Bash
flask db migrate -m "comment" 
```
Push changes to database file:
```Bash
flask db upgrade
```
---