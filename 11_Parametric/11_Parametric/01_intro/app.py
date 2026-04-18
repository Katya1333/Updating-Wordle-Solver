from flask import Flask
app = Flask(__name__)


@app.route('/<foo_bar>')
def home(foo_bar):
    return foo_bar

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)