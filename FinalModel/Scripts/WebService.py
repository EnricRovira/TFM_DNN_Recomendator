#C:\Users\enric\Google Drive\PROYECTOS\TFM_Motor de Recomendacion\Master\99_FinalModel\Scripts
#set FLASK_APP=WebService.py
#flask run --host=0.0.0.0
#192.168.1.47:5000

from flask import Flask, request, redirect, render_template
from forms import form
from tensorflow.keras.models import Model, Sequential, load_model
import tensorflow as tf
import Recommendator as r
import os

app = Flask(__name__)
path = os.path.join('../Data/')
path_models = os.path.join('../Models/')

def load_keras_model():
	global rec_model
	rec_model = load_model(path_models + 'candidate_generation')
	global graph
	graph = tf.get_default_graph() 


@app.route('/', methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    # Create form
    formulary = form.ReusableForm(request.form)

    if request.method == 'POST' and formulary.validate():
        # Extract information
        customer = int(request.form['customer'])
        top = int(request.form['top'])
        print(customer, top)
        load_keras_model()
        return render_template('rec.html', input = r.recommend_1(model = rec_model, customer = customer, N = top))

    # Send template information to index.html
    return render_template('index.html', form=formulary)

@app.route('/rec', methods=['GET', 'POST'])
def rec():
	return 

if __name__ == '__main__':
	app.debug = True
	app.run()
	#app.run(host = '0.0.0.0')
