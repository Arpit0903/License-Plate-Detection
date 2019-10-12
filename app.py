from flask import Flask,render_template,request
import pickle
from pyt import Detect

UPLOAD_FOLDER = '/home/me/Desktop/arpit/MachineLearning/License plate detection/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result',methods=['GET','POST'])
def result():
    if request.method=='POST':
        file=request.files.get('myfile')
        plate_num=Detect(file)
        print(plate_num)
        #if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file', filename=filename))
    #filename = 'http://127.0.0.1:5000/uploads/' + filename
        return render_template('result.html', plate = plate_num)

if __name__=='__main__':
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True) 
