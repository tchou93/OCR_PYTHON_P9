# Project P9

## Steps to install the environment:
```
* Clone the project from github:
git clone https://github.com/tchou93/OCR_PYTHON_P9.git

* Install the last version of python
https://www.python.org/downloads/

* Use a virtual environment
python -m venv env
source env/Scripts/activate

* Install some specific packets on this virtual environment
pip install -r requirements.txt
```

## Step to run the Django server:
```
* Enter to the directory: src
python manage.py runserver (or run the script run_server.sh)

* Enter to the server link
http://127.0.0.1:8000/
```

## Information to use the administration mode:
```
* Enter to the link : http://127.0.0.1:8000/admin (name: tan, pass:Angela93)
```

## Main information of the database necessary for the tests:
```
name: tan
pass: Angela93
subscriptions: henri, jjacques, alison
subscribers: alison
Posts:
 review:
 - Candide (tan)
 - The secret garden (alison)
 - Gone with the wind (jjacques)
 - Alice au pays des merveilles (henri)
 ticket:
 - Le petit prince (tan)
 - Candide (tan)
 
name: henri
pass: Angela94
subscriptions: alison
subscribers: tan, jjacques, alison
Posts:
 review
 - Alice au pays des merveilles (henri)
 - The secret garden (alison)
 ticket:
 - Alice au pays des merveilles (henri)
 
name: jjacques
pass: Angela95
subscriptions: henri, alison
subscribers: tan
Posts:
 ticket:
 - Gone with the wind (jjacques)

name: alison
pass: Angela96
subscriptions: tan, henri
subscribers: henri, jjacques, tan
 ticket:
 - The secret garden (alison)
```