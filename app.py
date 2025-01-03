from flask import Flask, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import aiprompter

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
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return jsonify({"Result": aiprompter.main(genre, artist)})
    return render_template('home.html', form=form)

if __name__ == '__main__':
    app.run()
