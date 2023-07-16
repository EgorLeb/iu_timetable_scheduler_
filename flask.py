import os, time
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from script import get_schedule
from src.output_formatting.output_algorithms import parametrized, create_xlsx
from src.class_hierarchy.exception_classes.always_no_as_preference import AlwaysNoAsTeacherPreference
from src.class_hierarchy.exception_classes.no_such_group_exists import NoSuchGroupExists
from src.class_hierarchy.exception_classes.no_teacher_preference import NoTeacherPreferenceException
from src.class_hierarchy.exception_classes.not_a_number_provided import NotANumberProvided
from src.class_hierarchy.exception_classes.wrong_course_activity_format import WrongCourseActivityFormat
from src.class_hierarchy.exception_classes.wrong_course_activity_type import WrongCourseActivityTypeException
from src.class_hierarchy.exception_classes.wrong_format_for_sport_reservation import WrongFormatForSportReservation
from src.class_hierarchy.exception_classes.wrong_sheet_name import WrongSheetNameProvided

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
            try:

                week1, week2, groups, rooms = get_schedule()
                create_xlsx(week1, week2, groups, rooms)

                return redirect(url_for('download'))
            except AlwaysNoAsTeacherPreference as e:
                return render_template('index.html', upload = False, message = e.args[0])
            except NoSuchGroupExists as e:
                return render_template('index.html', upload = False, message = e.args[0])
            except NoTeacherPreferenceException as e:
                return render_template('index.html', upload = False, message = e.args[0])
            except NotANumberProvided as e:
                return render_template('index.html', upload = False, message = e.args[0])
            except WrongCourseActivityFormat as e:
                return render_template('index.html', upload = False, message = e.args[0])
            except WrongCourseActivityTypeException as e:
                return render_template('index.html', upload = False, message = e.args[0])
            except WrongFormatForSportReservation as e:
                return render_template('index.html', upload = False, message = e.args[0])
            except WrongSheetNameProvided as e:
                return render_template('index.html', upload = False, message = e.args[0])
            except AttributeError:
                return render_template('index.html', upload = False, message = "Empty cell error")
    return render_template('index.html', upload = True, message = "Input file verification")
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