from flask import Flask,render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
import os,datetime
from werkzeug.utils import secure_filename
import uuid


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'Uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123456@localhost:5432/imagesdb'
db=SQLAlchemy(app)


#Model class of Uploads_Tbl
class UploadFiles(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    fileName = db.Column(db.String(100))
    createdon = db.Column(db.DateTime)

    def __init__(self, fileName, createdon):
        self.fileName = fileName
        self.createdon = createdon



#db.create_all()

#Home
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result',methods=['GET'])
def result():
    return "File Uploaded Successfully"



#Upload
@app.route('/api/upload',methods=['GET','POST'])
def uploadFile():
    if request.method == 'POST':

        file = request.files['file']
        filename = secure_filename(file.filename)

        # Gen GUUID File Name
        fileExt = filename.split('.')[1]
        autoGenFileName = uuid.uuid4()

        newFileName = str(autoGenFileName) + '.' + fileExt

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName)    )

        #Save file Info into DB
        file = UploadFiles(fileName=newFileName, createdon=datetime.datetime.now(datetime.timezone.utc))

        db.session.add(file)
        db.session.commit()


        return redirect(url_for('result'))


if __name__ == "__main__":
    app.run(debug=True)