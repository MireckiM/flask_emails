from flask import Flask, render_template, request, send_file, make_response, session
import emails as _emails
import livolink as _livolink
import email
from email.header import decode_header
import analyser as _analyser
import os
from dotenv import load_dotenv
import imaplib

app = Flask(__name__)
app.secret_key = os.getenv('secret_key')

_emails.getEmails()

def configure():
    load_dotenv()

#maile = _emails.mailbox
email_data = _emails.email_data


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/emails', methods=['GET','POST'])
def about():
    return render_template('emails.html', email_data=email_data)

@app.route('/emails2', methods=['GET','POST'])
def emails():
    return render_template('emails2.html', email_data=email_data)

@app.route('/view_attachment')
def view_attachment():
    email_username = os.getenv('username')
    email_password = os.getenv('password')
    mail = imaplib.IMAP4_SSL("imap.dpoczta.pl")
    mail.login(email_username,email_password)

    mailbox = "INBOX"
    mail.select(mailbox)

    search_criteria='(SEEN)'
    result, message_ids = mail.search(None, search_criteria)
    #result, message_ids = mail.select(mailbox)

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
    attachment_data = session.pop(filename, None)
    if attachment_data:
        response = make_response(attachment_data)
        response.headers.set('Content-Type', 'application/octet-stream')
        response.headers.set(
            'Content-Disposition', f'attachment; filename="{filename}'
        )
        return response
    else:
        return "Attachment not found"

@app.route('/download/<subject>')
def download(subject):
    imap_server = "imap.dpoczta.pl"
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(os.getenv('username'), os.getenv('password'))
    status, messages = imap.select("INBOX")
    subject=_emails.clean(subject)
    #search_criteria = '(SUBJECT "{subject}")'
    #result, messages = imap.search(None, search_criteria)
    N = 3
    # total number of emails
    messages = int(messages[0])
    for i in range(messages, messages-N, -1):
        email_item = {}
        email_item["attachments"] = []
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                email_subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    email_subject = email_subject.decode(encoding)
                #    decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                    
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            pass

                        elif "attachment" in content_disposition:
                            file_data = part.get_payload(decode=True)
                            if email_subject == subject:
                                # download attachment
                                filename = part.get_filename()
                                if filename:
                                    folder_name = _emails.clean(subject)
                                    if not os.path.isdir(folder_name):
                                        # make a folder for this email (named after the subject)
                                        os.mkdir(folder_name)
                                    filepath = os.path.join(folder_name, filename)
                                    # download attachment and save it
                                    open(filepath, "wb").write(part.get_payload(decode=True))
                            else:
                                pass
                            
    return file_data

@app.route('/downloadAttachment', methods=['POST'])
def downloadAttachment():    
    attach = request.form.get('argument')
    data = _emails.download(attach)
    return f'{data}'

@app.route('/sendOrder', methods=['POST'])
def sendOrder():    
    mail = request.form.get('argument')
    _livolink.inquiry(mail)
    return mail


if __name__ == '__main__':
    app.run(debug=True)
