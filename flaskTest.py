from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

@app.route('/', methods = ['GET', "POST"])
@app.route('/home', methods = ['GET', "POST"])

def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return "Upload succesful"
    return render_template('home.html', form=form)

def hello_world():
    return 'Hello World'

"""def input():
    user_input = request.args.get('filename')"""    

if __name__ == '__main__':
    app.run()