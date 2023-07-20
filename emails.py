import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from dotenv import load_dotenv


imap_server = "imap.dpoczta.pl"

def configure():
    load_dotenv()

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

class mail:
    def __init__(self, subject, sender, content):
        self.subject = subject
        self.sender = sender
        self.content = content

    def __str__(self):
        return f'Temat: {self.subject},Nadawca: {self.sender},Treść: {self.content}'

mailbox=[]

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
def getEmails():
    for i in range(messages, messages-N, -1):
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
                            mailbox.append(mail(subject,From,body))
                            print(mailbox[0])
                        elif "attachment" in content_disposition:
                            pass

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
                print("obiekt")
                print(mailbox[0])

    imap.close()
    imap.logout()
