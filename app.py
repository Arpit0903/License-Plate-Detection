from flask import Flask,render_template,request
import pickle
from livereload import Server

app=Flask(__name__)

@app.route('/'
def home():
    return render_template('home.html')

@app.route('/result',methods=['GET','POST'])
def result():
    if request.method=='POST':
        file=request.files.get('myfile')
        filename=file
        #from skimage.io import imread
        import matplotlib.pyplot as plt
        car_image = plt.imread(filename)
        from PIL import Image
        #car_image = Image.open(filename)
        car_image=Image.fromarray(car_image)
        car_image.save("static/car.png")
        car_image.save("car.png")
        import requests
        regions = ['fr', 'it']
        with open('car.png', 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),  # Optional
                files=dict(upload=fp),
                headers={'Authorization': 'Token 2ec5878b06ca1be24f61f34142443cc5baa3194c'})
        #print(response.json())
        #print(response.json()['results'][0]['plate'])
        #plate_num=Detect(file)
        plate_num=response.json()['results'][0]['plate']
        plate_num=plate_num.upper()
        #print(plate_num)
        return render_template('result.html', plate = plate_num)

if __name__=='__main__':
    server = Server(app.wsgi_app)
    server.serve()
    server.watch('/Views/*')
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
