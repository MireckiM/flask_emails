from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Homepage</h1>'

@app.route('/emails')
def about():
    return '<h2>Lista wiadomosci:</h2>'

if __name__ == '__main__':
    app.run()