#C:\Users\enric\Google Drive\PROYECTOS\TFM_Motor de Recomendacion\Master\TFM_DNN_Recomendator\05_Implementacion
#set FLASK_APP = WebService.py
#flask run

from flask import Flask, request, redirect
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def hello_world():
    return 'Welcome to Enric´s Recommendator'

if __name__ == '__main__':
	app.debug = True
	#app.run(host = '0.0.0.0',port=33)