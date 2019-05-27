#start web
#1.bottle
'''
from bottle import route,run

@route('/hello')
def hello():
    return("hello world!")

run(host='localhost',port=8080,debug=True)
'''
#2.flask

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'HelloWorld by Flask'
