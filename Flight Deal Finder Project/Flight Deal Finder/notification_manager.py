import smtplib

class NotificationManager:
    def __init__(self, email, emailpass, receiver_mail):
        self.email = email
        self.email_pass = emailpass
        self.receiver = receiver_mail
    
    def send_mail(self, subject, content):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.email_pass)
            connection.sendmail(
                from_addr=self.email, 
                to_addrs=self.receiver,
                msg= 'Subject: {}\n\n{}'.format(subject, content)
            )
        print("already send to email")

        
