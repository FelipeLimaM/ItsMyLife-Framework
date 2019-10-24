import smtplib


class Gmail(object):
    '''Class to send EMAIL from Gmail.com.'''
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_message(self,person_email, subject, body):
        ''' This must be removed '''
        headers = [
            "From: " + "It's My Life (Framework)",
            "Subject: " + subject,
            "To: " + person_email,
            "MIME-Version: 1.0",
           # "Content-Type: text/html"]
           "Content-Type: text"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            person_email,
            headers + "\r\n\r\n" + body)
