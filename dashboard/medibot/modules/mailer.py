import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dashboard.models import user
from medibot.settings import HOST, passd
import random, string 

def send_mail(name, email_id):
    res = ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    mail_user = user.objects.filter(email=email_id).first()
    mail_user.verification = res
    mail_user.save()

    link = HOST+'/verify/'+ str(mail_user.id)+ '/' + str(res) 
    body = 'Hello, '+name + f"""
    
    Please click on the link below to verify your email ID:

    {link}

    Best,
    Group 16
    """
    # put your email here
    sender = 'varad.fcrit@gmail.com'
    # get the password in the gmail (manage your google account, click on the avatar on the right)
    # then go to security (right) and app password (center)
    # insert the password and then choose mail and this computer and then generate
    # copy the password generated here

    password = passd

    # put the email of the receiver here
    receiver = email_id 

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    # message['Cc'] = cc

    message['Subject'] = 'E-mail Verification from Virtual Manager'
    
    message.attach(MIMEText(body, 'plain'))
        
    #use gmail with port
    session = smtplib.SMTP('smtp.gmail.com', 587)
    
    #enable security
    session.starttls()
    
    #login with mail_id and password
    session.login(sender, password)

    text = message.as_string()
    session.sendmail(sender, message["To"].split(",") , text)
    session.quit()
