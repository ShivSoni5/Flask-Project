#!/usr/bin/env python3

import requests
from flask import Flask, render_template, request    

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == 'POST':
        try:
            url = request.form['url']
            r = requests.get(url)
            print(r.text)
        except:
            errors.append("Unable to get URL. Please make sure it's valid and try again.")
    return render_template('index.html', errors=errors, results=results)


if __name__ == '__main__':
    app.run()
