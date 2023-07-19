from flask import Flask, render_template
import emails as _emails

app = Flask(__name__)

_emails.getEmails()

maile = _emails.mailbox

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/emails', methods=['GET','POST'])
def about():
    return render_template('emails.html', maile=maile)

if __name__ == '__main__':
    app.run()