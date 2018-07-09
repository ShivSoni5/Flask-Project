#!/usr/bin/env python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')

'''
@app.route('/<name>')
def hello_name(name):
    return (f'Hello {name}!')
'''

if __name__ == '__main__':
    app.run()
