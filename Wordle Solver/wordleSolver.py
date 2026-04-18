import requests, re
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

word_list = open("enable1.txt","r").read().splitlines()
word_list.append('inbox')

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/<grayLetters>/<greenLetters>/<yellowLetters>')
def miniTask1(grayLetters, greenLetters, yellowLetters):
    grayRegEx = "[^"+grayLetters+"]" #grayLetters is just letters
    regEx = []
    for pd in greenLetters: #greenLetters is a string with letters and dots
        if pd==".":
            regEx.append(grayRegEx)
        else:
            regEx.append(pd)
    yellowArr = [] #list of yellow letters (letters that must be in the word)
    for j,yellow in enumerate(yellowLetters): #yellowLetters is a string with letters and dots
        if yellow!="." and "[" in regEx[j%5]:
            temp = regEx[j%5]
            regEx[j%5] = temp[:-1] + yellow + temp[-1] #add the yellow letters to the list of gray letters ONLY for that index where it is yellow
            yellowArr.append(yellow)
        elif yellow!=".":
            yellowArr.append(yellow)
    #print(regEx)
    #print(yellowArr)
    regExStr = "".join(regEx)
    pattern = re.compile(rf'^({regExStr})$')
    filtered_words = [word for word in word_list if pattern.match(word) and all(letter in word for letter in yellowArr)]
    return jsonify(filtered_words)

app.debug = True
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)

quit()