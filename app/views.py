"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask_wtf.csrf import generate_csrf
from app.forms import MovieForm
from app.models import Movie
from flask import render_template, request, jsonify, make_response, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import os

ERROR = {
    'status': 'error',
    'errors': []
}

SUCCESS = {
    'status': 'success',
    'message': 'Movie successfully added!',
    'title': '',
    'description': '',
    'poster': ''
}

MOVIES = {'movies':[]}

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/movies', methods=['GET', 'POST'])
def movies():
    movie_form = MovieForm()
    if request.method=='POST' and movie_form.validate_on_submit:
        movie_form.validate()
        if not movie_form.errors:
            # get form data and its photo file to be saved
            title = movie_form.title.data.strip()
            description = movie_form.description.data.strip()
            poster = request.files['poster'] or movie_form.poster.data
            
            # get filename and rename to save in upload folder directory
            file_path = app.config['UPLOAD_FOLDER']
            file_in = secure_filename(poster.filename)
            name, ext = file_in.split(".") 
            file_name = name + "_" + datetime.strftime(datetime.now(),"%Y-%m-%dT%H-%M-%S") + f".{ext}"
            
            # create movie object to be added to database
            movie = Movie(title, description, file_name)
            try:
                # create uploads directory if not exists
                path = os.path.join(os.getcwd(),file_path)
                if not os.path.exists(path):
                    os.mkdir(path)
                
                # add movie to database and save poster image  
                db.session.add(movie)
                poster.save(os.path.join(file_path,file_name))
                db.session.commit()
                
                # build out the json object dictionary to send 
                response = SUCCESS
                response['title'] = title
                response['description'] = description
                response['poster'] = file_name
                return make_response(response)
            except OSError:
                # build response when unable to save photo
                response = ERROR
                response['errors'].append('Unable to save movie to database - Error saving poster image!')
            except Exception:
                # delete poster
                if os.path.exists(os.path.join(file_path,file_name)):
                    os.remove(os.path.join(file_path,file_name))
                    response = ERROR
                    response['errors'].append('Unable to save movie to database - Error updating database!')
        else:
            response = ERROR
            response['errors'] = form_errors(movie_form)
            return make_response(response,400)
    else:
        response = MOVIES
        movies = db.session.query(Movie.id, Movie.title, Movie.description, Movie.poster).all()
        response['movies'] = [dict(zip(['id', 'title', 'description', 'poster'], mov)) for mov in movies]
        return make_response(response,200)
    response = ERROR
    response['errors'].append({"method": request.method, "message": "Invalid method used!"})
    return make_response(response, 400)
        

@app.route("/api/v1/posters/<filename>", methods=['GET'])
def get_poster(filename):
    response =  ERROR
    response['errors'] = []
    response['errors'].append("Image not found!")
    for dir, subdirs, files in os.walk(os.getcwd()+app.config['UPLOAD_FOLDER']):
        for file in files:
            if filename.lower() == file.lower():
                return send_from_directory(dir, file)
    return make_response(response,404)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404