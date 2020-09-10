from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    name = 'こんにちは。私の名前は松田です。'
    return name

if __name__ == '__main__':
    app.run(debug=True)
