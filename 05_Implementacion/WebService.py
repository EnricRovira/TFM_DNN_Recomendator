#C:\Users\enric\Google Drive\PROYECTOS\TFM_Motor de Recomendacion\Master\TFM_DNN_Recomendator\05_Implementacion
#C:\Users\aeroengy\Desktop\Personal\Rec_ML\Recommender_keras-master\04_Modelado_y_Evaluacion
#set FLASK_APP=WebService.py
#flask run

from flask import Flask, request, redirect, render_template
from forms import form
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    # Create form
    formulary = form.ReusableForm(request.form)

    if request.method == 'POST' and formulary.validate():
        # Extract information
        customer = int(request.form['customer'])
        top = int(request.form['top'])

    # Send template information to index.html
    return render_template('index.html', form=formulary)

#def hello_world():
#    return '<h1>Welcome to Enric´s Recommendator</h1>'

if __name__ == '__main__':
	app.debug = True
	app.run()
	#app.run(host = '0.0.0.0',port=33)
