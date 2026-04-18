import requests, re
from flask import Flask, jsonify

app = Flask(__name__)

word_list = open("enable1.txt","r").read().splitlines()

@app.route('/<grayLetters>')
def miniTask1(grayLetters):
    pattern = re.compile(rf'^[^{grayLetters}]{{5}}$')
    filtered_words = [word for word in word_list if pattern.match(word)]
    return jsonify(filtered_words)

app.debug = True
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)

quit()