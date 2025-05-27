from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, SubmitField
from werkzeug.utils import secure_filename
import os
import traceback

from azureStorage import get_upload_images
import aiprompter
import spotify
import resultPage


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = os.path.join(os.environ.get('HOME', os.getcwd()), 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class UploadFileForm(FlaskForm):
    genre = StringField("Genre")
    artist = StringField("Artist")
    files = MultipleFileField("File")
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    return render_template("home.html")


@app.route('/guest', methods=['GET', "POST"])
def guest():
    form = UploadFileForm()
    if form.validate_on_submit():
        genre = form.genre.data
        artist = form.artist.data
        files = form.files.data

        if not files:
            return jsonify({"error": "No files uploaded"}), 400

        image_urls = get_upload_images(files)
        personalization = "none"
        user_tracks = "none"

        result = aiprompter.main(genre, artist, image_urls, personalization, user_tracks)
        return jsonify({"Result": result})

    return render_template('guest.html', form=form)


@app.route("/spotify", methods=["GET", "POST"])
def spotify_route():  # renamed to avoid conflict with imported module
    form = UploadFileForm()
    user_tracks = None
    result = None
    if form.validate_on_submit():
        try:
            genre = "none"
            artist = "none"
            files = form.files.data
            personalization = "spotify"

            if not files:
                return jsonify({"error": "No files uploaded"}), 400

            image_urls = get_upload_images(files)
            user_tracks = spotify.main()  # returns a 3 of track strings

            result, track_recommendation, artist= aiprompter.main(genre, artist, image_urls, personalization, user_tracks)
             
            track, track_url, artist_name, image_url = spotify.get_recommendation_metadata(track_recommendation, artist)
            session['result'] = result
            session['user_tracks'] = user_tracks
            session['artist'] = artist
            session['track_url'] = track_url
            print("TRACK_URL IS: " + track_url)
            return redirect(url_for('result_page'))
        except Exception as e:
            return jsonify({'error': str(e), 'trace': traceback.format_exc(), 'status': 'error'}), 500

    return render_template('spotify.html', form=form,result = result, user_tracks=user_tracks)

@app.route("/result", methods=["GET", "POST"])
def result_page():
    artist = session.get('artist')
    sp = session.get('sp')
    track_url = session.get('track_url')
    result = session.get('result')
    user_tracks = session.get('user_tracks', [])
    print("Loaded result page with:", result, user_tracks)
    return render_template('resultPage.html', result=result, user_tracks=user_tracks, track_url = track_url)
    

if __name__ == '__main__':
    app.run(debug=True)
