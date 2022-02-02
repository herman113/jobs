from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash # NEW - for flash messages
import re # RegEx for email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt # NEW - for hashing passwords
from flask_app import app # Needed for bcrypt as well
bcrypt = Bcrypt(app)
# from flask_app.models import name_of_model_file # If you need to import other model files, do so here

class User:
    db_name = "user_job_category_m2m_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def create_new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data) # Return the ID of the new user - to be saved in session
    # SELECT *, DATE_FORMAT(created_at, "%W %M %e %Y") AS date_created FROM users WHERE id = 1;
    @classmethod
    def grab_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def grab_one_user_with_jobs(cls, data):
        query = "select * from users left join jobs on users.id = jobs.creator_id WHERE creator_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_registration(form_data):
        is_valid = True # For now, the data from the form are OK
        if len(form_data["first_name"]) < 2: # Must be at least 2 characters long
            is_valid = False
            flash("First name must be at least 2 characters.")
        if len(form_data["last_name"]) < 2: # Must be at least 2 characters long
            is_valid = False
            flash("Last name must be at least 2 characters.")
        if not EMAIL_REGEX.match(form_data['email']):
            is_valid = False
            flash("Email is invalid.")
        if len(form_data["password"]) < 8: # Must be at least 8 characters long for password
            is_valid = False
            flash("Password must be at least 8 characters.")
        if form_data["password"] != form_data["password_confirmation"]:
            is_valid = False
            flash("Passwords don't agree.")
        return is_valid # Return if everything checks out - True if so, False if not

    @staticmethod
    def validate_login(query_data):
        db_name = "user_job_category_m2m_schema"
        # Check the email in the database
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db_name).query_db(query, query_data)
        print(results)
        if len(results) == 0:
            flash("Invalid login credentials.")
            return False # No need to check password - you can't log in
        # Check the password
        if not bcrypt.check_password_hash(results[0]["password"], query_data['password']):
            flash("Invalid login credentials.")
            return False # No need to check password - you can't log in
        return results[0]["id"] # Return the id of the user if their login credentials are good