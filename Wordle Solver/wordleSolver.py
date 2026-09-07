import requests, re, math
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# This creates all 243 possible feedback patterns:
# Note: B represents gray and G represents green
feedback_patterns_list = [
    a + b + c + d + e
    for a in "GYB"
    for b in "GYB"
    for c in "GYB"
    for d in "GYB"
    for e in "GYB"
]

word_list = open("enable1.txt","r").read().splitlines()
word_list.append('inbox')

# This returns a dictionary (len 243) that has a count for each pattern given that 'guess' is the
# real word:
def pattern_counts(guess, survivors):
    feedback_patterns_counts = {patternn: 0 for patternn in feedback_patterns_list}
    for w in survivors:
        pattern = get_feedback(guess, w)
        feedback_patterns_counts[pattern] += 1
    return feedback_patterns_counts

# This gives the pattern of GYB for a given word and guess:
def get_feedback(guess, answer):
    pattern = ["B"]*5
    answer_list = list(answer)

    for i in range(0,5):
        if guess[i]==answer[i]:
            pattern[i] = "G"
            answer_list[i] = None

    for i in range(5):
        if pattern[i] == "G":
            continue
        if guess[i] in answer_list:
            pattern[i] = "Y"
            answer_list[answer_list.index(guess[i])] = None

    return "".join(pattern)

# This will be used to turn the pattern_counts returned dictionary to a pattern probability 
# dictionary:
def counts_to_probabilities(counts):
    total = sum(counts.values())
    return {pattern: count/total for pattern, count in counts.items()}

# This will be used to turn the counts_to_probabilities returned dictionary to an entropy value:
def entropy(probabilities):
    H = 0
    for p in probabilities.values():
        if p>0:
            H -= p * math.log2(p)
    return H

# This code generates a list of the filtered words in order of their entropy:
def entropy_ranking(survivors, all_words=None):
    if all_words is None:
        all_words = survivors  # guess only from survivors

    ranking = []

    for guess in all_words:
        counts = pattern_counts(guess, survivors)
        probs = counts_to_probabilities(counts)
        H = entropy(probs)
        ranking.append((guess, H))

    # Sort by entropy descending
    ranking.sort(key=lambda x: x[1], reverse=True)

    return ranking

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
    entropy_ordered_words = entropy_ranking(filtered_words)
    #print(entropy_ordered_words)
    return jsonify(entropy_ordered_words)

app.debug = True
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)

quit()