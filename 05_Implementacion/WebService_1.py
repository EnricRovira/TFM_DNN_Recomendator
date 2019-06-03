#C:\Users\enric\Google Drive\PROYECTOS\TFM_Motor de Recomendacion\Master\TFM_DNN_Recomendator\05_Implementacion
#C:\Users\aeroengy\Desktop\Personal\Rec_ML\Recommender_keras-master\04_Modelado_y_Evaluacion
#set FLASK_APP=WebService.py
#flask run --host=0.0.0.0
#192.168.1.47:5000

from flask import Flask, request, redirect, render_template, flash
from forms import form
from tensorflow.keras.models import Model, Sequential, load_model
import tensorflow as tf
import Recommendator_20190527 as r

app = Flask(__name__)

def load_keras_model():
	global rec_model
	rec_model = load_model('../04_Modelado_y_Evaluacion/candidate_generation_20190525')
	global graph
	graph = tf.get_default_graph() 


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<a href="/rec"> click here for view your recommendations</a>'

@app.route('/rec', methods=['GET', 'POST'])
def rec():
    return None


if __name__ == '__main__':
	app.debug = True
	app.run()
	#app.run(host = '0.0.0.0')
