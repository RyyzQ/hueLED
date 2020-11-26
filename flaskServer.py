import hueScript

from flask import Flask, request, url_for, render_template, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

hueScript.defaultLedState()

@app.route("/")
def hello_world():
    return app.send_static_file('huecontrol.html')

@app.route("/hue", methods = ['POST'])
def hueControl():
    try:
        hueScript.insertHue(float(request.form['hue']))
        return jsonify(hueScript.calculateRGB(float(request.form['hue'])))
    except ValueError:
        return "Even if you're not using the slider, you still need to enter a number ;)"
    return "done."

@app.route("/hueflow", methods = ['POST'])
def hueFlow():
    if not hueScript.getIsFlowing():
        hueScript.flow()
        return "flowing"
    else:
        return "flow already happening"