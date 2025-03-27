from flask import Flask, request, render_template, jsonify, abort
from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, SubmitField
from werkzeug.utils import secure_filename
from azureStorage import get_upload_images
import os
import aiprompter

import spotify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = os.path.join(os.environ.get('HOME', 'C:\\'), 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class UploadFileForm(FlaskForm):
    genre = StringField("Genre")  # Correct usage
    artist = StringField("Artist")  # Correct usage
    files = MultipleFileField("File")
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    return render_template("home.html")

@app.route('/guest', methods=['GET', "POST"])
def guest():
    form = UploadFileForm()
    personalization = "none"
    if form.validate_on_submit():
        genre = form.genre.data
        artist = form.artist.data
        files = form.files.data
        user_tracks = "none"
        """
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                folder_path = app.config['UPLOAD_FOLDER']
                # Save the file
                file.save(file_path)
                folder_path = app.config['UPLOAD_FOLDER']
            else:
                return jsonify({"error": "No file uploaded"}), 400
                """
        image_urls = get_upload_images(files)
        return jsonify({"Result": aiprompter.main(genre, artist, image_urls, personalization, user_tracks)})
    return render_template('guest.html', form=form)

@app.route("/spotify", methods=["GET", "Post"])
def spoitfy():
    try:
        form = UploadFileForm()
        if form.validate_on_submit():
            genre = "none"
            artist = "none"
            files = form.files.data
            personalization = "spotify"
            image_urls = get_upload_images(files)
            user_tracks = spotify.main()
            return jsonify({
            "Result": aiprompter.main(genre, artist, image_urls, personalization, user_tracks)})
        else:
            print("No file submited")
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'})
    return render_template('spotify.html', form=form)

if __name__ == '__main__':
    app.run()