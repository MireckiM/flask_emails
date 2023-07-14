from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Homepage</h1>'

@app.route('/about')
def about():
    return 'podstronka'

if __name__ == '__main__':
    app.run()