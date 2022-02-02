from flask_app import app # NEED this line for app.route() among other things
from flask import render_template, redirect, request, session
from flask_app.models import user, job, category # Import your models here

'''
# * ROUTES 
0. #done show dashboard page                              /dashboard
-- #done grab all jobs - check if user is logged in
1. #done show view_job page                               /jobs/<int:id>
-- #done grab a user name
-- #todo grab job details
2. delete a job -                                   /
-- #!check to see if someone is logged in for a get req, otherwise this has to be a post req
3. show edit_job page                               /
3b. submit edit_job form POST                       /
4. #done show add_job page -                              /jobs/new
-- #done grab user
4b.#done submit add_job form                             /jobs/add_job_to_db     POST
5. adding a job to the users list                   /
6. finishing a job clicking done button             /
7. giving up on a job submission                    /
#?(8. adding job to categories)
'''

@app.route("/dashboard")
def landing_page():
    if "user_id" not in session: # If not logged in, send the user back
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    this_user = user.User.grab_one_user(data)
    # Before splitting up users
    all_jobs = job.Job.grab_all_jobs_split_up(session["user_id"])
    return render_template("dashboard.html", this_user = this_user, all_jobs = all_jobs)

@app.route("/jobs/<int:id>")
def show_view_job_page(id):
    # ? do I have to check if user is logged in
    if "user_id" not in session: # If not logged in, send the user back
        return redirect("/")
    data = {
        "id": session["user_id"],
        "job_id": id
    }
    this_user = user.User.grab_one_user(data)
    this_job = job.Job.grab_one_job(data)
    another_job = job.Job.grab_one_job_with_creator(data)
    
    return render_template("view_job.html", this_user = this_user, this_job = this_job, another_job = another_job)

@app.route("/jobs/new")
def show_add_job_page():
    if "user_id" not in session: # If not logged in, send the user back
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    this_user = user.User.grab_one_user(data)
    all_categories = category.Category.grab_all_categories()
    return render_template("add_job.html", this_user = this_user, all_categories = all_categories)

@app.route("/jobs/add_job_to_db", methods=["POST"])
def add_job_to_db():
    # print(request.form)
    # print(request.form.getlist("categories"))
    if not job.Job.validate_new_job(request.form):
        return redirect("/jobs/new")

    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "location": request.form["location"],
        "creator_id": session["user_id"] # creator is the person who is logged in
    }
    # job.Job.create_new_job(data)
    job_id = job.Job.create_new_job(data)
    # link categories to this job, if any
    # link pre existing categories (checkboxes)
    # if len(request.form.getlist("categories")) > 0: # If at least one checkbox is selected.
    category_id_list = request.form.getlist("categories")
    print (category_id_list)
    if len(category_id_list) > 0: # If at least one checkbox is selected.
        for category_id in category_id_list:

            print (type(category_id))
            print (type(job_id))
            category_data = {
                "category_id": category_id,
                "job_id": job_id
            }
            category.Category.add_category_to_job(category_data)
    # link a new category (text input)
    if request.form["other"] != "":
        # create new category
        category_data = {
            "name": request.form["other"]
        }
        new_category_id = category.Category.add_new_category(category_data)
        # link category to job
        category_job_data = {
            "category_id": new_category_id,
                "job_id": job_id
        }
        category.Category.add_category_to_job(category_job_data)
    # redirect to dashboard
    return redirect("/dashboard")

@app.route("/jobs/<int:id>/delete", methods=["POST"]) # Route to delete a job
def delete_job(id):
    if "user_id" not in session: # If not logged in, send the user back
        return redirect("/")
    data = {
        "id": id
    }
    job.Job.delete_job(data)
    return redirect("/dashboard")

@app.route("/jobs/<int:id>/edit_job_form")
def edit_job(id):
    if "user_id" not in session: # If not logged in, send the user back
        return redirect("/")
    # if not "user_id" == this_job jobs.creator_id: # If not logged in, send the user back
    #     return redirect("/")
    data = {
        "job_id": id,
        "id": session["user_id"]
    }
    this_user = user.User.grab_one_user(data)
    this_job = job.Job.grab_one_job(data)
    return render_template('edit_job_form.html', this_user = this_user, this_job = this_job)

@app.route("/jobs/<int:id>/edit_job_in_db", methods=["POST"])
def edit_job_in_db(id):
    if "user_id" not in session: # If not logged in, send the user back
        return redirect("/")
    if not job.Job.validate_job(request.form):
        return redirect(f"/jobs/{id}/edit_job_form")
    data = {
        "id": session["user_id"],
        "job_id": id,
        "title": request.form["title"],
        "description": request.form["description"],
        "location": request.form["location"],
    }
    job.Job.edit_job(data)
    return redirect("/dashboard")

@app.route("/jobs/<int:id>/link_user_to_job_holder_id")
def link_user_to_job_holder_id(id):
    data = {
        "job_id": id,
        "user_id": session["user_id"]
        }
    job.Job.link_user_to_job_holder_id(data)
    # get_a_job_holder_and_all_jobs(data)
    return redirect("/dashboard")

@app.route("/jobs/<int:id>/unlink_user_to_job_holder_id")
def unlink_user_to_job_holder_id(id):
    data = {
        "job_id": id,
        "id": session["user_id"],
        "job_holder_id": None
        }
    job.Job.unlink_user_to_job_holder_id(data)
    # get_a_job_holder_and_all_jobs(data)
    return redirect("/dashboard")

