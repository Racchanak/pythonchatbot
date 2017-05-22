#!flask/bin/python
from flask import Flask, jsonify, make_response
from flask_cors import CORS, cross_origin 
from flask import render_template
from flask import request
import json
import aiml
import os

app = Flask(__name__)

kernel = aiml.Kernel()

if os.path.isfile("brain/bot_brain.brn"):
    kernel.bootstrap(brainFile="brain/bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
    kernel.saveBrain("brain/bot_brain.brn")


@app.route('/')
def index():
    return "Hello World!"

# @app.route('/signUp')
# def signUp():
#     return render_template('test.html')

@app.route('/signUp/')
@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/chatBot/')
@app.route('/chatBot')
def chatBot():
    return render_template('index.html')


@app.route('/bot/<string:chat>', methods=['GET'])
def get_task(chat):
    return make_response(jsonify({'chatData': kernel.respond(chat)}))


#@app.route('/signUpUser', methods=['POST'])
#def signUpUser():
    #user =  request.form['username']
    #password = request.form['password']
    #return json.dumps({'status':'OK','user':user,'pass':password})
    #return make_response(jsonify({'bot-reply':'hello'}))

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    return make_response(jsonify({'status':'OK','user':user,'pass':password}))



app.config.update(
    PROPAGATE_EXCEPTIONS = True
)

if __name__ == '__main__':
    app.run(debug=True)
