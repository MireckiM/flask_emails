from flask import Flask, render_template, request, send_file
import emails as _emails
import analyser as _analyser
import os
from dotenv import load_dotenv
import imaplib

app = Flask(__name__)

_emails.getEmails()

def configure():
    load_dotenv()

maile = _emails.mailbox


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/emails', methods=['GET','POST'])
def about():
    return render_template('emails.html', maile=maile)

@app.route('/view_attachment', methods=['POST'])
def view_attachment():
    email_username = os.getenv('username')
    email_password = os.getenv('password')
    mail = imaplib.IMAP4_SSL("imap.dpoczta.pl")
    mail.login(email_username,email_password)

    mailbox = "INBOX"
    mail.select(mailbox)

    search_criteria='()'
    #result, message_ids = mail.search(None, search_criteria)
    result, message_ids = mail.select(mailbox)

    attachment_data = None
    attachment_filename = None

    if result == "OK":
        message_id_list = message_ids[0].split()
        if message_id_list:
            first_message_id = message_id_list[0]
            attachment_filename, attachment_data = _emails.get_attachment_content(mail, first_message_id)

    mail.logout()

    return render_template('attachment.html', attachment_filename=attachment_filename, attachment_data=attachment_data)

@app.route('/download_attachment/<filename>')
def download_attachment(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)