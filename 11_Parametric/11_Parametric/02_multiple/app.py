from flask import Flask
app = Flask(__name__)


@app.route('/<foo_bar>')
def home(foo_bar):
    return foo_bar

@app.route('/<foo>/<bar>')
def foo_bar(foo, bar):
    return 'parsing the route I was able to separate ------ '+ foo + ' ------ and ------ ' + bar

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)