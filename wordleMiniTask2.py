import requests, re
from flask import Flask, jsonify

app = Flask(__name__)

word_list = open("enable1.txt","r").read().splitlines()

@app.route('/<greenLetters>')
def miniTask2(greenLetters):
    pattern = re.compile(rf'^{greenLetters}$')
    if len(greenLetters)==5:
        filtered_words = [word for word in word_list if pattern.match(word)]
    else:
        filtered_words = "Wordle must be 5 characters :)"
    return jsonify(filtered_words)

app.debug = True
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)

quit()