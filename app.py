from flask import Flask, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, SubmitField
from werkzeug.utils import secure_filename
import os

from azureStorage import get_upload_images
import aiprompter
import spotify

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
    if form.validate_on_submit():
        try:
            genre = "none"
            artist = "none"
            files = form.files.data
            personalization = "spotify"

            if not files:
                return jsonify({"error": "No files uploaded"}), 400

            image_urls = get_upload_images(files)
            user_tracks = spotify.main()  # returns a list of track strings

            result = aiprompter.main(genre, artist, image_urls, personalization, user_tracks)
            return jsonify({"Result": result})

        except Exception as e:
            return jsonify({'error': str(e), 'status': 'error'}), 500

    return render_template('spotify.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
