from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash # NEW - for flash messages
import re # RegEx for email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt # NEW - for hashing passwords
from flask_app import app # Needed for bcrypt as well
bcrypt = Bcrypt(app)
# from flask_app.models import name_of_model_file # If you need to import other model files, do so here

class Category:
    db_name = "user_job_category_m2m_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def grab_all_categories(cls):
        query = "SELECT * FROM categories;"
        results = connectToMySQL(cls.db_name).query_db(query)
        category_instance = []
        for category in results:
            category_instance.append(cls(category))
        return category_instance

    @classmethod
    def add_new_category(cls, data):
        query = "INSERT INTO categories (name) VALUES (%(name)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def add_category_to_job(cls, data):
        query = "INSERT INTO categories_has_jobs (category_id, job_id) VALUES (%(category_id)s, %(job_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

