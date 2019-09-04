from flask import Flask,render_template,request
import pickle
from pyt import Detect

#plate_no=''
app=Flask(__name__)
@app.route('/')

def home():
    if request.method=='POST':
        fname=request.form['myfile']
        plate=Detect(fname)
        return render_template('home.html',plate_no=plate)
    else:
        print('hi')

if __name__=='__main__':
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True) 
