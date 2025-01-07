from flask import Flask, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import aiprompter
from azureStorage import get_upload_images

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    genre = StringField("Genre")  # Correct usage
    artist = StringField("Artist")  # Correct usage
    file = FileField("File")
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        genre = form.genre.data
        artist = form.artist.data

        # Access the uploaded file
        uploaded_file = form.file.data  # This is a FileStorage object

        # Get the file name (safe for saving to the filesystem)
        file_name = secure_filename(uploaded_file.filename)

        # Read the file content as bytes
        file_bytes = uploaded_file.read()  # Get the raw file content as bytes

        # Save the bytes to a file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        with open(file_path, 'wb') as f:
            f.write(file_bytes)

        # Upload the file to Azure Storage and get the image URL
        image_url = get_upload_images(file_bytes, file_name)
        return jsonify({"Result": aiprompter.main(genre, artist, image_url)})
    return render_template('home.html', form=form)

if __name__ == '__main__':
    app.run()
