import os, time
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from src.main.script import get_schedule
from src.output_formatting.output_algorithms import parametrized, create_xlsx

UPLOAD_FOLDER = 'input_data'
DOWNLOAD_FOLDER = 'output_data'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "Time_Table_Input.xlsx"))
        week, groups = get_schedule()
        
        create_xlsx(parametrized(week), groups)
        return redirect(url_for('download'))
    return  render_template('index.html')
@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        return send_from_directory(os.path.join(app.config['DOWNLOAD_FOLDER']), "schedule.xlsx")
    return render_template('download.html') 

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
   print(1) 
   return render_template('download.html') #send_from_directory(os.path.join(app.config['DOWNLOAD_FOLDER']), filename)
