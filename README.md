# user authentication template

- rename project

  app
  |---- flask_app
  | |---- config
  | | |\_**\_ mysqlconnection.py
  | |
  | |---- controllers
  | | |\_\_** users.py
  | |
  | |---- models
  | | |\_**\_ users.py
  | |
  | |---- static
  | | |---- css
  | | | |\_\_** style.css
  | | |
  | | |---- images
  | | |---- js
  | | | |\_**\_ app.js
  | | |---- videos
  | | |---- templates
  | | | |---- landing_page.html
  | | | |\_\_** login_reg_page.html
  | |---- **init**.py
  | |\_\_\_\_ server.py

## stack

- python
- flask
- pymysql

## backend

### mysql

- rename users_schema_starter.mwb and forward engineer it to mysql workbench
- db_name = "put schema name here" in user model
- put password in the mysqlconnection.py

### pipenv packages

- flask
- pymsql
- flask-bcrypt

### flask commands

- pipenv shell
- pipenv install flask pymysql flask-bcrypt
- pipenv graph
- python3 server.py

## frontend

- bootstrap
- jinja
- html

# functionality

- register(sign up)
- login
