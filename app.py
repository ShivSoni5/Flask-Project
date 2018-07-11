#!/usr/bin/env python3

import re
import operator
import nltk
from nltk.corpus import stopwords
import requests
from flask import Flask, render_template, request    
from collections import Counter
from bs4 import BeautifulSoup
import mysql.connector as mysql

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == 'POST':
        try:
            url = request.form['url']
            r = requests.get(url)
        except:
            errors.append("Unable to get URL. Please make sure it's valid and try again.")
            return render_template('index.html', errors=errors)
    
        if r:
	    # Text Processing
            raw = BeautifulSoup(r.text).get_text()
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
	    # removing punctuations and numbers
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_words_count = Counter(raw_words)
	    # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stopwords.words('english')]
            no_stop_words_count = Counter(no_stop_words)
	    # save the results
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
                )[:10]
            try:
                mariadb = mysql.connect(user='raj',password='redhat',database='Flask_Project')
                cursor = mariadb.cursor()
                query = (f'insert into results values(NULL,"{url}","{raw_words_count}","{no_stop_words_count}");')
                cursor.execute(query)
                mariadb.commit()
                mariadb.close()
            except Exception as e:
                errors.append(e)

    return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
    app.run(debug=True)
