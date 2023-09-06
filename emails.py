import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from dotenv import load_dotenv
import analyser as _analyser


imap_server = "imap.dpoczta.pl"

def configure():
    load_dotenv()

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

class mail:
    def __init__(self, subject, sender, content, filename, file_data, analysis):
        self.subject = subject
        self.sender = sender
        self.content = content
        self.filename = filename
        self.file_data = file_data
        self.analysis = analysis

    def __str__(self):
        return f'Temat: {self.subject}, Nadawca: {self.sender}, Treść: {self.content}, Nazwa plku: {self.filename}, Plik: {self.file_data}, Analiza: {self.analysis}'

mailbox=[]
email_data = []

configure()
# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL(imap_server)
# authenticate
imap.login(os.getenv('username'), os.getenv('password'))

status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 3
# total number of emails
messages = int(messages[0])

def decode_attachment_name(name):
    decoded_name = decode_header(name)[0][0]
    if isinstance(decoded_name, bytes):
        decoded_name = decoded_name.decode()
        return decoded_name

def getEmails():
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
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                #    decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                    
                email_item["subject"] = subject
                email_item["from"] = From
                #email_item["attachments"]
                print("Subject:", subject)
                print("From:", From)
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
                            # print text/plain emails and skip attachments
                            print(body)
                            email_item["body"] = body
                            email_item["analysis"] = _analyser.analyseMail(body)
                            #print(_analyser.analyseMail(body))
                            #mailbox.append(mail(subject,From,body,"", _analyser.analyseMail(body)))
                            #print(mailbox[0])
                            filename = None
                            content_type = None
                            file_data = None

                        elif "attachment" in content_disposition:
                            
                            # download attachment
                            filename = part.get_filename()
                            content_type = part.get_content_type()
                            file_data = part.get_payload(decode=True)
                            
                            if filename:
                                filename = decode_attachment_name(filename)
                                attachment_data = part.get_payload(decode=True)
                                folder_name = clean(subject)
                            #    if not os.path.isdir(folder_name):
                            #        # make a folder for this email (named after the subject)
                            #        os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                attachment_info = {
                                    "filename": filename,
                                    "data": attachment_data,
                                    "filepath": filepath
                                }
                                email_item["attachments"].append(attachment_info)
                            #    # download attachment and save it
                            #    open(filepath, "wb").write(part.get_payload(decode=True))
                            #    webbrowser.open(filepath)

                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                if content_type == "text/html":
                    pass
                print("="*100)
            
        mailbox.append(mail(subject,From,body,filename,file_data, _analyser.analyseMail(body)))
        email_data.append(email_item)
        
    imap.close()
    imap.logout()


def get_attachment_content(mail, message_id):
    result, data = mail.fetch(message_id, "(RFC822)")
    raw_email = data[0][1]

    msg = email.message_from_bytes(raw_email)

    for part in msg.walk():
        if part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is None:
            continue
        filename = part.get_filename()
        content_type = part.get_content_type()
        file_data = part.get_payload(decode=True)

        if filename and content_type:
            return filename, file_data
        
def save_attachment(file_data, filename, download_folder):
    file_path = os.path.join(download_folder, filename)
    with open(file_path, "wb") as file:
        file.write(file_data)
    return file_path
