import re # RegEx for email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash # NEW - for flash messages
from flask_app.models import user, category
# from flask_app.models import name_of_model_file # If you need to import other model files, do so here

class Job:
    db_name = "user_job_category_m2m_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.location = data["location"]
        self.creator_id = data["creator_id"]
        self.job_holder_id = data["job_holder_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None
        self.holder = None
        self.categories = []

    '''
        0. # done READ grab all jobs
        1. # todo READ grab_one_job
        2. # todo DELETE a job by id
        3. # todo READ grab a job by id
        3b. # todo UPDATE a job by id
        4. nothing needed
        4b. # todo CREATE a job
        5. # todo READ grab a job and add it to users_job_list
        6. # todo DELETE a job after removing it from user_job_list
        7. # todo READ grab a job by user and remove it from users_job_list
    ''' 

    @classmethod
    def grab_all_jobs(cls):
        query = "SELECT * FROM jobs;"
        results = connectToMySQL(cls.db_name).query_db(query)
        job_instances = []
        for job_instance in results:
            job_instances.append(cls(job_instance))
        return job_instances

    @staticmethod
    def validate_new_job(form_data):
        is_valid = Job.validate_job(form_data) # validate title, description, location
        # todo add category validations here
        return is_valid

    @staticmethod
    def validate_job(form_data):
        is_valid = True # For now, the data from the form are OK
        if len(form_data["title"]) < 3: # Must be at least 3 characters long
            is_valid = False
            flash("Title must be at least 3 characters.")
        if len(form_data["description"]) < 3: # Must be at least 3 characters long
            is_valid = False
            flash("Description must be at least 3 characters.")
        if len(form_data["location"]) < 3: # Must be at least 3 characters long
            is_valid = False
            flash("Location must be at least 3 characters.")
        #todo add validation for categories here later.
        return is_valid # Return if everything checks out - True if so, False if not

    @classmethod
    def create_new_job(cls, data):
        query = "INSERT INTO jobs (title, description, location, creator_id) VALUES (%(title)s, %(description)s, %(location)s, %(creator_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data) # Return the ID of the new job - to be saved in session

    @classmethod
    def grab_one_job(cls, data):
        query = "SELECT * FROM jobs WHERE id = %(job_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results[0])
        print(results[0]['creator_id'])
        return cls(results[0])

    @classmethod
    def grab_one_job_with_creator(cls, data):
        query = "SELECT * FROM jobs LEFT JOIN users ON jobs.creator_id = users.id LEFT JOIN categories_has_jobs ON jobs.id = categories_has_jobs.job_id LEFT JOIN categories ON categories.id = categories_has_jobs.category_id WHERE jobs.id = %(job_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        # print (results[0])
        if len(results) == 0:
            return []
        # print(results[0]['creator_id'])
        this_job = cls(results[0])
        user_data = {
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }
        user_instance = user.User(user_data) # create an instance of user class
        this_job.creator = user_instance  # link user to job instance as a job attribute 
        # ling categories to job here
        for current_category in results:
            category_dictionary = {
            "id": current_category['categories.id'],
            "name": current_category['name'],
            "created_at": current_category['categories.created_at'],
            "updated_at": current_category['categories.updated_at']
        }
        category_instance = category.Category(category_dictionary)
        this_job.categories.append(category_instance)
        print(this_job.categories[0].name)
        return this_job

    # grab all jobs with users connected
    @classmethod
    def grab_all_job_with_creators(cls):
        query = "SELECT * FROM jobs JOIN users ON jobs.creator_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        # print (results[0])
        if len(results) == 0:
            return []
        all_jobs = []
        for current_job in results:
            this_job = cls(current_job)
            user_data = {
                "id": current_job['users.id'],
                "first_name": current_job['first_name'],
                "last_name": current_job['last_name'],
                "email": current_job['email'],
                "password": current_job['password'],
                "created_at": current_job['users.created_at'],
                "updated_at": current_job['users.updated_at']
            }
            user_instance = user.User(user_data) # create an instance of user class
            this_job.creator = user_instance  # link user to job instance as a job attribute
            all_jobs.append(this_job) # add job with linked User to this list
        return all_jobs
    
    # grab all jobs split up by those not taken by anyone and those taken by the logged in user
    @classmethod
    def grab_all_jobs_split_up(cls, user_id):
        query = "SELECT * FROM jobs JOIN users ON jobs.creator_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        # print (results[0])
        if len(results) == 0:
            return []
        '''
        3 scenarios
        1. nobody has taken the job.
        2. someone has taken the job, and it's the logged in user.
        3. someone has taken the job, and it's Not the logged in user.  No need to display that job.
        '''
        nonTaken_jobs = [] # scenario 1
        your_jobs = [] # scenario 2
        for current_job in results:
            this_job = cls(current_job)
            user_data = {
                "id": current_job['users.id'],
                "first_name": current_job['first_name'],
                "last_name": current_job['last_name'],
                "email": current_job['email'],
                "password": current_job['password'],
                "created_at": current_job['users.created_at'],
                "updated_at": current_job['users.updated_at']
            }
            user_instance = user.User(user_data) # create an instance of user class
            this_job.creator = user_instance  # link user to job instance as a job attribute
            if current_job["job_holder_id"] == None: # Not taken, so null in db (or None in Python)
                nonTaken_jobs.append(this_job) # add job with linked User to this list
            elif current_job["job_holder_id"] == user_id: # Is taken, and is taken by the logged in user
                your_jobs.append(this_job) # add job with linked User to this list
        # Dictionary to hold both lists
        returned_jobs = {
            "nonTaken_jobs": nonTaken_jobs,
            "your_jobs": your_jobs
        }
        return returned_jobs

    @classmethod
    def delete_job(cls, data):
        query = 'DELETE FROM jobs WHERE id = %(id)s;'
        connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def edit_job(cls, data):
        query = 'UPDATE jobs SET title = %(title)s, description = %(description)s, location = %(location)s WHERE id = %(job_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def link_user_to_job_holder_id(cls, data):
        query = 'UPDATE jobs Set job_holder_id = %(user_id)s WHERE id = %(job_id)s;'
        connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def unlink_user_to_job_holder_id(cls, data):
        query = 'UPDATE jobs Set job_holder_id = %(job_holder_id)s WHERE id = %(job_id)s;'
        connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_a_job_holder_and_all_jobs(cls, data):
        query = 'SELECT * FROM jobs join users on jobs.job_holder_id = users.id WHERE users.id = %(id)s;'
        connectToMySQL(cls.db_name).query_db(query, data)

    # @classmethod
    # def get_a_job_holder_and_all_jobs(cls, data):
    #     query = 'SELECT * FROM users join jobs on jobs.job_holder_id = users.id WHERE users.id = %(users_id)s;'
    #     connectToMySQL(cls.db_name).query_db(query, data)