from flask import Flask, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, SubmitField
from werkzeug.utils import secure_filename
from azureStorage import get_upload_images
import os
import aiprompter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = os.path.join(os.environ.get('HOME', 'D:\\home'), 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class UploadFileForm(FlaskForm):
    genre = StringField("Genre")  # Correct usage
    artist = StringField("Artist")  # Correct usage
    files = MultipleFileField("File")
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        genre = form.genre.data
        artist = form.artist.data
        files = form.files.data
        for file in files:
            if file:
                filename = secure_filename(file.name)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                folder_path = app.config['UPLOAD_FOLDER']
            else:
                return jsonify({"error": "No file uploaded"}), 400

        image_urls = get_upload_images(folder_path)

        return jsonify({"Result": aiprompter.main(genre, artist, image_urls)})
    return render_template('home.html', form=form)

if __name__ == '__main__':
    app.run()
