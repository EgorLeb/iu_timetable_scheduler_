import os, time
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from script2 import get_schedule
from src.output_formatting.output_algorithms import parametrized, create_xlsx

UPLOAD_FOLDER = 'mysite/input_data'
DOWNLOAD_FOLDER = 'output_data'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        print(file.filename)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "Time_Table_Input.xlsx"))
            week1, week2, groups = get_schedule()
            create_xlsx(parametrized(week1), parametrized(week2), groups)
            return redirect(url_for('download'))
    return  render_template('index.html')
@app.route('/download/', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        print(request)
        return send_from_directory(os.path.join(app.config['DOWNLOAD_FOLDER']), "schedule.xlsx")
    return render_template('download.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
   print(1)
   return render_template('download.html')

# if(__name__ == "__main__"):
#     app.run(debug=True)
