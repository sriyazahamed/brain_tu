import keras
from PIL import Image
import numpy as np
from flask_cors import *
import logging
from werkzeug.utils import secure_filename
from flask import *
import os
import dbService
import json




UPLOAD_FOLDER = 'C:/Riyaz/CIT/Main Project/8 sem project/Flask app/venv/uploaded_imgs'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def getStatus(number):
    if number==0:
       return  "Its a tumour" 
    else:
        return "No ,Its not a tumour"



model = keras.models.load_model(r'C:/Riyaz/CIT/Main Project/8 sem project/Flask app/venv/my_h5_model.h5')		

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/getScanResult', methods = ['POST'])
def return_image_id():
	target=os.path.join(UPLOAD_FOLDER,'imgs')
	if not os.path.isdir(target):
		os.mkdir(target)
	file = request.files['file']
	filename = "new.jpg"
	destination="/".join([target, filename])
	file.save(destination) 
	img = Image.open(r"C:/Riyaz/CIT/Main Project/8 sem project/Flask app/venv/uploaded_imgs/imgs/new.jpg")
	img.convert('RGB')

	x = np.array(img.resize((128,128)))
	x = x.reshape(1,128,128,3)
	res = model.predict_on_batch(x)
	classification = np.where(res == np.amax(res))[1][0]
	status = getStatus(classification)
	predictionPercentage = round(res[0][classification]*100,2)

	return  {"result":status,"predictionPercentage":str(predictionPercentage)}

@app.route('/getImage')
def return_image():
	args = request.args
	imageId = args.get('imageId')
	print(imageId)
	try:
		return send_file(r"C:/Riyaz/CIT/Main Project/8 sem project/Flask app/venv/uploaded_imgs/imgs/"+str(imageId)+".jpg", mimetype='image/gif')
	except Exception as e:
		return str(e)

@app.route('/registerPatient', methods=['POST'])
def return_patientId():
	id = dbService.insertPatient(json.loads(request.data))
	return id

@app.route('/insertScanImage', methods=['POST'])
def return_imageId():
	id = dbService.insertScanImage(json.loads(request.data))
	source = 'C:/Riyaz/CIT/Main Project/8 sem project/Flask app/venv/uploaded_imgs/imgs/new.jpg'
	dest = 'C:/Riyaz/CIT/Main Project/8 sem project/Flask app/venv/uploaded_imgs/imgs/'+id+'.jpg'
	os.rename(source, dest)
	return id


@app.route('/getPatient', methods=['POST'])
def return_patient():
	id= json.loads(request.data)
	id = id["patientId"]
	
	patient = dbService.getPatient(id)
	return patient

@app.route('/getScanResults', methods=['POST'])
def return_results():
	id= json.loads(request.data)
	id = id["patientId"]
	
	scanResults = dbService.getScanResults(id)
	return scanResults


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

CORS(app, expose_headers='Authorization')